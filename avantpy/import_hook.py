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

friendly_traceback.exclude_file_from_traceback(__file__)


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

        friendly_traceback.cache.add(self.filename, source)
        friendly_traceback.clear_traceback()
        try:
            session.state.set_dialect(dialect)
            source = converter.convert(source, dialect, filename=self.filename)
        except Exception:
            friendly_traceback.explain()
            return

        # ------------------------
        # Previously, we did the following essentially in one step:
        #
        #     exec(source, vars(module))
        #
        # The problem with that approach is that exec() records '<string>'
        # as the filename, for every file thus loaded; in some cases, the
        # prevented the traceback from having access to the source of the file.
        # By doing it in two steps, as we do here by first using compile()
        # and then exec(), we ensure that the correct filename is attached
        # to the code objects.
        # -------------------------

        try:
            code_obj = compile(source, self.filename, "exec")
        except Exception:
            friendly_traceback.explain()

        try:
            exec(code_obj, vars(module))
        except Exception:
            friendly_traceback.explain()
        return
