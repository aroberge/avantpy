"""A custom importer making use of the import hook capability
"""
import difflib
import importlib
import os
import os.path
import sys
import webbrowser

from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_file_location

from . import conversion


def import_main(name):
    """Imports the module that is to be interpreted as the main module.

       avantpy is often invoked with a script meant to be run as the
       main module its source is transformed with the -s (or --source) option,
       as in::

           python -m avantpy -s name

       Python identifies avantpy as the main script; we artificially
       change this so that "main_script" is properly identified as ``name``.
    """
    conversion.MAIN_MODULE_NAME = name
    return importlib.import_module(name)


class AvantPyMetaFinder(MetaPathFinder):
    """A custom finder to locate modules.  The main reason for this code
       is to ensure that our custom loader, which does the code transformations,
       is used."""

    def find_spec(self, fullname, path, target=None):
        """Finds the appropriate properties (spec) of a module, and sets
           its loader."""

        if not path:
            path = [os.getcwd()]
        if "." in fullname:
            name = fullname.split(".")[-1]
        else:
            name = fullname
        for entry in path:
            for ext in conversion.FILE_EXT:
                filename = os.path.join(entry, name + "." + ext)
                if os.path.exists(filename):
                    break
            else:
                continue

            return spec_from_file_location(
                fullname,
                filename,
                loader=AvantPyLoader(filename),
                submodule_search_locations=None,
            )
        return None  # Not an AvantPy file


sys.meta_path.insert(0, AvantPyMetaFinder())


class AvantPyLoader(Loader):
    """A custom loader which will transform the source prior to its execution"""

    def __init__(self, filename):
        self.filename = filename

    def exec_module(self, module):
        """import the source code, conversion it before executing it."""

        if module.__name__ == conversion.MAIN_MODULE_NAME:
            module.__name__ = "__main__"
            conversion.MAIN_MODULE_NAME = None

        with open(self.filename, encoding="utf8") as f:
            source = f.read()
        original = source

        _path, extension = os.path.splitext(self.filename)
        extension = extension[1:]

        if extension in conversion.DICTIONARIES:
            conversion.CURRENT = extension
            source = conversion.to_python(source)

            if conversion.DIFF:
                name = os.path.basename(_path)
                html_file = self.write_html_diff(name, original, source)
                webbrowser.open_new_tab(html_file)
                sys.exit()
        else:
            raise NotImplementedError("%s: extension not found in known languages."%extension)

        exec(source, vars(module))

    def write_html_diff(self, name, original, transformed):
        """Writes an html file showing the difference between the original
           and the transformed source."""
        html_file = name + ".html"
        fromlines = original.split("\n")
        tolines = transformed.split("\n")
        print

        diff = difflib.HtmlDiff().make_file(
            fromlines, tolines, name + "." + conversion.CURRENT, name + ".py"
        )
        with open(html_file, "w", encoding="utf8") as the_file:
            the_file.write(diff)
        return html_file

