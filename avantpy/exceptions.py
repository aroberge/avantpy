'''Custom exceptions'''

class AvantPyException(Exception):
    def __init__(self, msg, args):
        super().__init__(msg)
        self.msg = msg
        self.args = args


class IfNobreakError(AvantPyException):
    pass

class TryNobreakError(AvantPyException):
    pass

class NobreakFirstError(AvantPyException):
    pass

class NobreakSyntaxError(AvantPyException):
    pass


class RepeatFirstError(AvantPyException):
    pass