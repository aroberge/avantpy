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


class TryNobreakError(AvantPyException):
    """Raised if ``nobreak`` is used instead of ``else`` in ``try/except`` statement"""

    pass


class NobreakFirstError(AvantPyException):
    """Raised if ``nobreak`` is used somewhere other than at the beginning of a line."""

    pass


class RepeatFirstError(AvantPyException):
    """Raised if ``repeat`` is used somewhere other than at the beginning of a line."""

    pass


class UnknownDialect(AvantPyException):
    """Raised when attempting to set ``dialect`` to unsupported value."""

    pass


class UnknownLanguage(AvantPyException):
    """Raised when attempting to set ``lang`` to unsupported value."""

    pass


class UnexpectedError(AvantPyException):
    """Raised when some unexpected condition occurs which should
       be cavered by a specific excption."""

    pass
