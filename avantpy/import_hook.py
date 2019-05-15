"""A custom importer making use of the import hook capability
"""
import importlib
import os
import os.path
import sys

from codeop import CommandCompiler
from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_file_location

import friendly_traceback

from . import session
from . import converter
from .my_gettext import gettext_lang

MAIN_MODULE_NAME = None
COUNTER = 0


def import_main(name):
    """Imports the module that is to be interpreted as the main module.

       avantpy is often invoked with a script meant to be run as the
       main module its source is transformed with the -s (or --source) option,
       as in::

           python -m avantpy -s name

       Python identifies avantpy as the main script, which is not what we want.
    """
    global MAIN_MODULE_NAME
    _ = gettext_lang.lang
    MAIN_MODULE_NAME = name
    try:
        main = importlib.import_module(name)
        return main
    except ModuleNotFoundError:
        print(_("Cannot find main module: "), name)


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
            for ext in session.state.all_dialects():
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
        self.compile = CommandCompiler()

    def exec_module(self, module):
        """import the source code, converts it before executing it."""
        global COUNTER
        COUNTER += 1
        if module.__name__ == MAIN_MODULE_NAME:
            module.__name__ = "__main__"

        with open(self.filename, encoding="utf8") as f:
            source = f.read()
        # original = source

        _path, extension = os.path.splitext(self.filename)
        # name = os.path.basename(_path)
        # fullname = name + extension
        dialect = extension[1:]

        try:
            session.state.set_dialect(dialect)
            source = converter.convert(source, dialect, filename=self.filename)
        except Exception:
            friendly_traceback.explain()
            return

        # ------------------------
        # Ideally, instead of the following use of exec(source), we would
        # proceed in two steps:
        # 1. use a custom AST parser that could generate more detailed
        #    information when a SyntaxError is found
        # 2. If no error is found, exec the code objects produced by the AST.
        # -------------------------

        try:
            exec(source, vars(module))
        except Exception:
            # exec() always gives "<string>" as file name
            friendly_traceback.utils.cache_string_source(
                "<string>", (self.filename, source)
            )
            # We remove the first stack item because it is our own code.
            sys.last_type, sys.last_value, last_tb = sys.exc_info()
            sys.last_traceback = last_tb
            try:
                friendly_traceback._explain(
                    sys.last_type, sys.last_value, last_tb.tb_next
                )
            finally:
                last_tb = None
        return
