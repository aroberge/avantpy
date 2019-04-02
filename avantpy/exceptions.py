"""Custom exceptions"""


class AvantPyException(Exception):
    """Base class for custom exceptions."""

    def __init__(self, msg, args):
        super().__init__(msg)
        self.msg = msg
        self.args = args


class IfNobreakError(AvantPyException):
    """Raised if ``nobreak`` is used instead of ``else`` in an ``if`` statement"""

    pass


class MismatchedBracketsError(AvantPyException):
    """Raised if a left parenthesis '(', or square bracket '['
       or curly bracket '{', is closed by a right 'bracket' of a different type.

       In standard Python, this would be indicated as::

           SyntaxError: invalid syntax
    """

    pass


class MissingLeftBracketError(AvantPyException):
    """Raised if a right parenthesis ')', or square bracket ']'
       or curly bracket '}', is found without having a matching left bracket
       found previously.

       In standard Python, this would be indicated as::

           SyntaxError: invalid syntax
    """

    pass


class MissingRepeatError(AvantPyException):
    """Raised if ``until`` or ``forever`` is used without being preceeded by
       ``repeat``.
    """

    pass


class MissingRepeatColonError(AvantPyException):
    """Raised if a line beginning with ``repeat`` does not end with a colon.
    """

    pass


class MissingRightBracketError(AvantPyException):
    """Raised if a left parenthesis '(', or square bracket '['
       or curly bracket '{', is never closed by a corresponding bracket.

       In standard Python, this would be indicated as::

           SyntaxError: unexpected EOF while parsing
    """

    pass


class NobreakFirstError(AvantPyException):
    """Raised if ``nobreak`` is used somewhere other than at the beginning of a line."""

    pass


class NobreakSyntaxError(AvantPyException):
    """Raised if ``nobreak`` is without a matching block."""

    pass


class RepeatFirstError(AvantPyException):
    """Raised if ``repeat`` is used somewhere other than at the beginning of a line."""

    pass


class TryNobreakError(AvantPyException):
    """Raised if ``nobreak`` is used instead of ``else`` in ``try/except`` statement"""

    pass


class UnknownDialectError(AvantPyException):
    """Raised when attempting to set ``dialect`` to unsupported value."""

    pass


class UnknownLanguageError(AvantPyException):
    """Raised when attempting to set ``lang`` to unsupported value."""

    pass
