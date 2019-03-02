"""A custom importer making use of the import hook capability
"""
import difflib
import importlib
import os.path
import sys
import tokenize

from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_file_location
from io import StringIO

from . import config


def import_main(name):
    """Imports the module that is to be interpreted as the main module.

       avantpy is often invoked with a script meant to be run as the
       main module its source is transformed with the -s (or --source) option,
       as in::

           python -m avantpy -s name

       Python identifies avantpy as the main script; we artificially
       change this so that "main_script" is properly identified as ``name``.
    """
    config.MAIN_MODULE_NAME = name
    return importlib.import_module(name)


class AvantpyMetaFinder(MetaPathFinder):
    """A custom finder to locate modules.  The main reason for this code
       is to ensure that our custom loader, which does the code transformations,
       is used."""

    def find_spec(self, fullname, path, target=None):
        """finds the appropriate properties (spec) of a module, and sets
           its loader."""

        if not path:
            path = [os.getcwd()]
        if "." in fullname:
            name = fullname.split(".")[-1]
        else:
            name = fullname
        for entry in path:
            if os.path.isdir(os.path.join(entry, name)):
                # this module has child modules
                filename = os.path.join(entry, name, "__init__.py")
                if not os.path.exists(filename):
                    continue
                submodule_locations = [os.path.join(entry, name)]
            else:
                submodule_locations = None
                for ext in config.FILE_EXT:
                    filename = os.path.join(entry, name + "." + ext)
                    if os.path.exists(filename):
                        break
                else:
                    continue

            return spec_from_file_location(
                fullname,
                filename,
                loader=AvantpyLoader(filename),
                submodule_search_locations=submodule_locations,
            )
        return None  # we don't know how to import this


sys.meta_path.insert(0, AvantpyMetaFinder())


class AvantpyLoader(Loader):
    """A custom loader which will transform the source prior to its execution"""

    def __init__(self, filename):
        self.filename = filename

    def exec_module(self, module):
        """import the source code, transforms it before executing it so that
           it is known to Python."""

        if module.__name__ == config.MAIN_MODULE_NAME:
            module.__name__ = "__main__"
            config.MAIN_MODULE_NAME = None

        with open(self.filename) as f:
            source = f.read()
        original = source

        extension = self.filename.split(".")[-1]
        if extension in config.DICTIONARIES:
            source = translate(source, config.DICTIONARIES[extension])

        if config.CONVERT and extension in config.FILE_EXT:
            print("############### Original source: ############\n")
            print(original)
            print("\n############### Converted source: ############\n")
            print(source)
            print("=" * 50, "\n")

        exec(source, vars(module))

    def write_html_diff(self, name, original, transformed):
        """Writes an html file showing the difference between the original
           and the transformed source."""
        html = name + ".html"
        fromlines = original.split("\n")
        tolines = transformed.split("\n")

        diff = difflib.HtmlDiff().make_file(
            fromlines, tolines, name + "." + config.FILE_EXT, name + ".py"
        )
        with open(html, "w") as the_file:
            the_file.write(diff)
        print("Diff file writen to", html)


def translate(source, dictionary):
    """A dictionary with a one-to-one translation of keywords is used
    to provide the transformation.
    """
    toks = tokenize.generate_tokens(StringIO(source).readline)
    result = []
    for toktype, tokvalue, _, _, _ in toks:
        if toktype == tokenize.NAME and tokvalue in dictionary:
            result.append((toktype, dictionary[tokvalue]))
        else:
            result.append((toktype, tokvalue))
    return tokenize.untokenize(result)
