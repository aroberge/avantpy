"""session.py

Keeps track of and updates the state of the session: language and dialect used.
"""
import glob
import os.path
import runpy


import friendly_traceback

from . import exceptions
from .my_gettext import gettext_lang


# MonkeyPatching
_old_shorten_path = friendly_traceback.utils.shorten_path
this_dir = os.path.dirname(__file__)
AVANTPY = os.path.abspath(os.path.join(this_dir, "..")).lower()
AVANTPY_TESTS = os.path.join(AVANTPY, "tests").lower()


def shorten_path(path):
    path_lower = path.lower()
    if path_lower.startswith(AVANTPY_TESTS):
        path = "AVANTPY-TESTS:" + path[len(AVANTPY_TESTS) :]  # noqa
    elif path_lower.startswith(AVANTPY):
        path = "AVANTPY:" + path[len(AVANTPY) :]  # noqa
    else:
        path = _old_shorten_path(path)
    return path


friendly_traceback.utils.shorten_path = shorten_path


class _State:
    """Keeps track of dialect and lang parameters which control some of the
       behaviour of AvantPy.
    """

    def __init__(self):
        self.dict_to_py = {}
        self.dict_from_py = {}
        self.languages = set(["en"])
        self.current_dialect = None
        self.current_lang = None
        self.current_filename = None
        self.prompt1 = ">>> "  # can be reset based on dialect
        self.prompt2 = "... "
        self.console_active = False
        self.collect_dialects()
        self.collect_languages()
        self.install_gettext("xx")

    def collect_dialects(self):
        """Find known dialects and create corresponding dictionaries."""
        dialects = glob.glob(os.path.dirname(__file__) + "/dialects/*.py")
        for f in dialects:
            if os.path.isfile(f) and not f.endswith("__init__.py"):

                dialect = os.path.basename(f).split(".")[0]
                friendly_traceback.exclude_file_from_traceback(runpy.__file__)

                _module = runpy.run_path(f)
                from_py = _module[dialect]
                self.dict_from_py[dialect] = from_py

                to_py = {}
                for k, v in from_py.items():
                    if isinstance(v, str):
                        to_py[v] = k
                    else:
                        for val in v:
                            to_py[val] = k
                self.dict_to_py[dialect] = to_py

    def collect_languages(self):
        """Creates a set of known languages."""
        languages = glob.glob(os.path.dirname(__file__) + "/locales/*")
        for f in languages:
            if os.path.isdir(f):
                lang = os.path.basename(f)
                self.languages.add(lang)

    def all_dialects(self):
        """Returns a list of all known dialects."""
        return [k for k in self.dict_from_py.keys()]

    def is_dialect(self, dialect):
        """Returns True if `dialect` is a known dialect, False otherwise."""
        return dialect in self.dict_from_py

    def is_lang(self, lang):
        """Returns True if `lang` is known as part of a dialect,
                   False otherwise
        """
        return lang in self.languages

    def get_dialect(self):
        """Returns the current dialect."""
        return self.current_dialect

    def get_lang(self):
        """Returns the current language."""
        return self.current_lang

    def get_to_python(self, dialect=None):
        """Returns a dict providing translation from a dialect into Python.
        """
        # to_py uses the language code instead of the dialect as key.
        if dialect is None:
            dialect = self.current_dialect
        return self.dict_to_py[dialect]

    def get_from_python(self, dialect=None):
        """Returns a dict providing translation from Python into a dialect."""
        if dialect is None:
            dialect = self.current_dialect
        return self.dict_from_py[dialect]

    def set_dialect(self, dialect):
        """Sets the current dialect.

           Raises an exception if the dialect is unknown.

           If current language is set to None, an attempt will be made
           to set language to the value corresponding to dialect.

           Also sets the default prompt.
        """
        if not self.is_dialect(dialect):
            raise exceptions.UnknownDialectError(
                "Unknown dialect %s" % dialect, (dialect, self.all_dialects())
            )
        else:
            lang = dialect[2:]
            self.current_dialect = dialect
            if self.current_lang is None:
                try:
                    self.set_lang(lang)
                except exceptions.UnknownLanguageError:
                    pass
            elif self.console_active:
                self.print_lang_info()
        self.prompt1 = dialect + "> "
        self.prompt2 = "..." + " " * (len(dialect) - 1)

    def set_lang(self, lang):
        """Sets the current language.

           Raises an exception if the language is unknown.

           If current dialect is set to None, an attempt will be made
           to set dialect to the value corresponding to language.
        """
        if not self.is_lang(lang):
            raise exceptions.UnknownLanguageError(
                "Unknown language %s" % lang, (lang, self.languages)
            )
        else:
            self.current_lang = lang
            self.install_gettext(lang)
            if self.current_dialect is None:
                try:
                    self.set_dialect("py" + lang)
                except exceptions.UnknownDialectError:
                    pass
            elif self.console_active:
                self.print_lang_info()
            friendly_traceback.set_lang(lang)

    def install_gettext(self, lang):
        """Sets the current language for gettext."""
        gettext_lang.install(lang)

    def print_lang_info(self):
        """Prints language and dialect selected.

           Intended to be used in the console.
        """
        _ = gettext_lang.lang
        print(
            _("    ==> Language: {lang} | AvantPy dialect: {dialect}").format(
                lang=self.current_lang, dialect=self.current_dialect
            )
        )


state = _State()
