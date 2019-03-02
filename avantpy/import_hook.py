"""A custom importer making use of the import hook capability
"""
import difflib
import os.path
import sys

import importlib
from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_file_location

from . import config
from . import transforms


def import_main(name):
    """Imports the module that is to be interpreted as the main module.

       pyextensions is often invoked with a script meant to be run as the
       main module its source is transformed with the -s (or --source) option,
       as in::

           python -m pyextensions -s name

       Python identifies pyextensions as the main script; we artificially
       change this so that "main_script" is properly identified as ``name``.
    """
    config.MAIN_MODULE_NAME = name
    return importlib.import_module(name)


class ExtensionMetaFinder(MetaPathFinder):
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
                submodule_locations = [os.path.join(entry, name)]
            else:
                filename = os.path.join(entry, name + "." + config.FILE_EXT)
                submodule_locations = None

            if not os.path.exists(filename):
                continue

            return spec_from_file_location(
                fullname,
                filename,
                loader=ExtensionLoader(filename),
                submodule_search_locations=submodule_locations,
            )
        return None  # we don't know how to import this


sys.meta_path.insert(0, ExtensionMetaFinder())


class ExtensionLoader(Loader):
    """A custom loader which will transform the source prior to its execution"""

    def __init__(self, filename):
        self.filename = filename

    def exec_module(self, module):
        """import the source code, transforma it before executing it so that
           it is known to Python."""

        if not self.filename.endswith(config.FILE_EXT) and not self.filename.endswith(
            "__init__.py"
        ):
            print("Fatal error: ExtensionLoader is asked to load a normal file.")
            print("filename:", self.filename)
            print("Expected extension:", config.FILE_EXT)
            raise SystemExit

        name = module.__name__
        if module.__name__ == config.MAIN_MODULE_NAME:
            module.__name__ = "__main__"
            config.MAIN_MODULE_NAME = None

        with open(self.filename) as f:
            source = f.read()

        transforms.identify_requested_transformers(source)

        if config.TRANSFORMERS:
            original = source
            source = transforms.add_all_imports(source)
            source = transforms.apply_source_transformations(source)

            if config.DIFF and original != source:
                self.write_html_diff(name, original, source)

        if config.CONVERT and self.filename.endswith(config.FILE_EXT):
            print("############### Original source: ############\n")
            print(original)
            print("\n############### Converted source: ############\n")
            print(source)
            print("=" * 50, "\n")

        source = transforms.apply_ast_transformations(source)
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
