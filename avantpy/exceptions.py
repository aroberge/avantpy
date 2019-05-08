"""Custom exceptions"""

from .my_gettext import gettext_lang


class AvantPyException(Exception):
    """Base class for custom exceptions."""

    def __init__(self, msg, args):
        _ = gettext_lang.lang
        self.msg = msg
        self.args = args
        self.params = args[0]
        self.friendly = {"header": _("AvantPy exception:")}
        self.add_cause()

    def __str__(self):
        return f"{self.__class__.__name__}: {self.msg}"

    def add_cause(self):
        self.friendly["generic"] = None


class AvantPySyntaxError(AvantPyException, SyntaxError):
    """Base class for custom exceptions that are SyntaxErrors"""

    def __init__(self, msg, args):
        super().__init__(msg, args)
        _ = gettext_lang.lang
        self.friendly["header"] = _("AvantPy syntax error:")
        self.filename = self.params["filename"]
        self.lineno = self.params["linenumber"]
        if "offset" in self.params:
            self.offset = self.params["offset"]
        else:
            self.offset = 1


class IfNobreakError(AvantPySyntaxError):
    """Raised if ``nobreak`` is used instead of ``else`` in an ``if`` statement"""

    def add_cause(self):
        _ = gettext_lang.lang
        self.friendly["generic"] = _(
            "The AvantPy '{nobreak_kwd}' keyword cannot be used in\n"
            "an '{if_kwd}/{elif_kwd}/{else_kwd}' clause (Python: if/elif/else).\n"
        ).format(
            nobreak_kwd=self.params["nobreak keyword"],
            if_kwd=self.params["if_kwd"],
            elif_kwd=self.params["elif_kwd"],
            else_kwd=self.params["else_kwd"],
        )


class MismatchedBracketsError(AvantPySyntaxError):
    """Raised if a left parenthesis '(', or square bracket '['
       or curly bracket '{', is closed by a right 'bracket' of a different type.

       In standard Python, this would be indicated as::

           SyntaxError: invalid syntax
    """

    def add_cause(self):
        _ = gettext_lang.lang
        self.friendly["generic"] = _(
            "The opening {open_bracket} does not match the closing {close_bracket}.\n"
        ).format(
            open_bracket=self.params["open_bracket"],
            close_bracket=self.params["close_bracket"],
        )


class MissingLeftBracketError(AvantPySyntaxError):
    """Raised if a right parenthesis ')', or square bracket ']'
       or curly bracket '}', is found without having a matching left bracket
       found previously.

       In standard Python, this would be indicated as::

           SyntaxError: invalid syntax
    """

    def add_cause(self):
        _ = gettext_lang.lang
        self.friendly["generic"] = _(
            "The closing {bracket} does not match anything.\n"
        ).format(bracket=self.params["bracket"])


class MissingRepeatColonError(AvantPySyntaxError):
    """Raised if a line beginning with ``repeat`` does not end with a colon.
    """

    def add_cause(self):
        _ = gettext_lang.lang
        self.friendly["generic"] = _(
            "A statement beginning with the '{repeat_kwd}' keyword must be on\n"
            "a single line ending with a colon (:) that indicates the beginning of\n"
            "an indented block of code, with no other colon appearing on that line.\n"
        ).format(repeat_kwd=self.params["repeat_kwd"])


class MissingRepeatError(AvantPySyntaxError):
    """Raised if ``until`` or ``forever`` is used without being preceeded by
       ``repeat``.
    """

    def add_cause(self):
        _ = gettext_lang.lang
        self.friendly["generic"] = _(
            "The AvantPy '{keyword}'' keyword can be used only when"
            "preceded by '{repeat_kwd}'.\n"
        ).format(keyword=self.params["keyword"], repeat_kwd=self.params["repeat_kwd"])


class NobreakFirstError(AvantPySyntaxError):
    """Raised if ``nobreak`` is used somewhere other than at the beginning of a line."""

    def add_cause(self):
        _ = gettext_lang.lang
        self.friendly["generic"] = _(
            "The AvantPy '{nobreak_kwd}' keyword can be used instead of '{else_kwd}'\n"
            "(Python: else) only when it begins a new statement in\n"
            "'{for_kwd}/{while_kwd}' loops (Python: for/while).\n\n"
        ).format(
            nobreak_kwd=self.params["nobreak keyword"],
            for_kwd=self.params["for_kwd"],
            while_kwd=self.params["while_kwd"],
            else_kwd=self.params["else_kwd"],
        )


class NobreakSyntaxError(AvantPySyntaxError):
    """Raised if ``nobreak`` is without a matching block."""

    def add_cause(self):
        _ = gettext_lang.lang
        self.friendly["generic"] = _(
            "The AvantPy '{nobreak_kwd}' keyword can only be used as a replacement\n"
            "of '{else_kwd}' (Python: else) with a matching '{for_kwd}' or\n"
            "'{while_kwd}' loop (Python: for/while).\n"
        ).format(
            nobreak_kwd=self.params["nobreak keyword"],
            for_kwd=self.params["for_kwd"],
            while_kwd=self.params["while_kwd"],
            else_kwd=self.params["else_kwd"],
        )


class RepeatFirstError(AvantPySyntaxError):
    """Raised if ``repeat`` is used somewhere other than at the beginning of a line."""

    def add_cause(self):
        _ = gettext_lang.lang
        self.friendly["generic"] = _(
            "The AvantPy '{repeat_kwd}' keyword can only be used to begin\n"
            "a new loop (Python: equivalent to 'for' or 'while' loop).\n"
        ).format(repeat_kwd=self.params["repeat keyword"])


class TryNobreakError(AvantPySyntaxError):
    """Raised if ``nobreak`` is used instead of ``else`` in ``try/except`` statement"""

    def add_cause(self):
        _ = gettext_lang.lang
        self.friendly["generic"] = _(
            "The AvantPy '{nobreak_kwd}' keyword cannot be used in\n"
            "a '{try_kwd}/{except_kwd}/{else_kwd}/{finally_kwd}' clause\n"
            "(Python: try/except/else/finally).\n"
        ).format(
            nobreak_kwd=self.params["nobreak keyword"],
            try_kwd=self.params["try_kwd"],
            except_kwd=self.params["except_kwd"],
            else_kwd=self.params["else_kwd"],
            finally_kwd=self.params["finally_kwd"],
        )


class UnknownDialectError(AvantPyException):
    """Raised when attempting to set ``dialect`` to unsupported value."""

    def add_cause(self):
        _ = gettext_lang.lang
        dialect = self.args[0]
        all_dialects = self.args[1]

        self.friendly["generic"] = _(
            "The following unknown dialect was requested: {dialect}.\n\n"
            "The known dialects are: {all_dialects}.\n"
        ).format(dialect=dialect, all_dialects=all_dialects)


class UnknownLanguageError(AvantPyException):
    """Raised when attempting to set ``lang`` to unsupported value."""

    def add_cause(self):
        _ = gettext_lang.lang
        lang = self.args[0]
        all_langs = self.args[1]

        self.friendly["generic"] = _(
            "The following unknown languages was requested: {lang}.\n\n"
            "The known dialects are: {all_langs}.\n"
        ).format(lang=lang, all_langs=all_langs)
