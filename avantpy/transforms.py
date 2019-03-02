"""This module takes care of identifying, importing and adding source
code transformers. It also contains a function, `transform`, which
takes care of invoking all known transformers to convert a source code.
"""
import ast
import sys

from . import config
from .unparse import my_unparse


class NullTransformer:
    """NullTransformer is a convenience class which can generate instances
    to be used when a given transformer cannot be imported."""

    def transform_source(self, source):
        return source


def add_transformers(line):
    """Extract the transformers names from a line of code of the form
       #ext transformer1 [transformer2]
       and adds them to the globally known dict
    """
    assert line.startswith("#ext ")
    line = line[5:]

    for trans in line.split(" "):
        import_transformer(trans.strip())


def import_transformer(name):
    """If needed, import a transformer, and adds it to the globally known dict
       The code inside a module where a transformer is defined should be
       standard Python code, which does not need any transformation.
       So, we disable the import hook, and let the normal module import
       do its job - which is faster and likely more reliable than our
       custom method.
    """
    if name in config.TRANSFORMERS:
        if name not in config.AST_TRANSFORMERS:
            if hasattr(config.TRANSFORMERS[name], "transform_ast"):
                config.AST_TRANSFORMERS.append(name)
        return config.TRANSFORMERS[name]

    # We are adding a transformer built from normal/standard Python code.
    # As we are not performing transformations, we temporarily disable
    # our import hook, both to avoid potential problems AND because we
    # found that this resulted in much faster code.
    hook = sys.meta_path[0]
    sys.meta_path = sys.meta_path[1:]
    try:
        config.TRANSFORMERS[name] = __import__(name)
        # Some transformers are not allowed in the console.
        # If an attempt is made to activate one of them in the console,
        # we replace it by a transformer that does nothing and print a
        # message specific to that transformer as written in its module.
        if hasattr(config.TRANSFORMERS[name], "transform_ast"):
            config.AST_TRANSFORMERS.append(name)
    except ImportError:
        sys.stderr.write(
            "Warning: Import Error in add_transformers: %s not found\n" % name
        )
        config.TRANSFORMERS[name] = NullTransformer()
    except Exception as e:
        sys.stderr.write(
            "\nUnexpected exception in transforms.import_transformer %s\n "
            % e.__class__.__name__
        )
        sys.stderr.write(str(e.args))
        sys.stderr.write(f"\nname = {name}\n")
    finally:
        sys.meta_path.insert(0, hook)  # restore import hook

    return config.TRANSFORMERS[name]


def identify_requested_transformers(source):
    """
    Scan a source for lines of the form::

        #ext transformer1 [transformer2 ...]

    identifying transformers to be used and ensure that they are imported.
    """
    lines = source.split("\n")
    clear = False
    for number, line in enumerate(lines):
        if line.startswith("#ext "):
            if not clear:
                config.TRANSFORMERS.clear()
                config.AST_TRANSFORMERS.clear()
                clear = True
            add_transformers(line)
    return None


def add_all_imports(source):
    """Some transformers may require that other modules be imported
    in the source code for it to work properly.
    """
    for name in config.TRANSFORMERS:
        tr_module = import_transformer(name)
        if hasattr(tr_module, "add_import"):
            source = tr_module.add_import() + source

    return source


def apply_source_transformations(source):
    """Used to convert the source code, making use of known transformers.

       "transformers" are modules which must contain a function

           transform_source(source)

       which returns a tranformed source.
       Some transformers (for example, those found in the standard library
       module lib2to3) cannot cope with non-standard syntax; as a result, they
       may fail during a first attempt. We keep track of all failing
       transformers and keep retrying them until either they all succeeded
       or a fixed set of them fails twice in a row.
    """
    # Some transformer fail when multiple non-Python constructs
    # are present. So, we loop multiple times keeping track of
    # which transformations have been unsuccessfully performed.
    not_done = config.TRANSFORMERS
    first_exception = None
    while True:
        failed = {}
        for name in not_done:
            tr_module = import_transformer(name)
            if hasattr(tr_module, "transform_source"):
                try:
                    source = tr_module.transform_source(source)
                except Exception as e:
                    failed[name] = tr_module
                    if first_exception is None:
                        first_exception = e

        if not failed:
            break

        # If the exact same set of transformations are not performed
        # twice in a row, there is no point in trying out again.
        if failed == not_done:
            # add verbose option
            # print("Warning: the following source transformations could not be done:")
            # for key in failed:
            #     print(key)
            raise first_exception
        not_done = failed  # attempt another pass

    return source


def apply_ast_transformations(source):
    """Used to convert the source code into an AST tree and applying
       all AST transformer specified in the source code. It returns
       a (potentially transformed) AST tree.

       "AST transformers" are modules which must contain a function

           transform_ast(tree)

       which return another AST tree.
    """
    if not config.AST_TRANSFORMERS:
        return source
    tree = ast.parse(source)
    for name in config.AST_TRANSFORMERS:
        tr_module = config.TRANSFORMERS[name]
        try:
            tree = tr_module.transform_ast(tree)
        except Exception as e:
            pass
            # add verbose option
            # print(f"Warning: the {name} AST transformation could not be done.")

    return my_unparse(tree)
