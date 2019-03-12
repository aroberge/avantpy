'''Custom exceptions'''

class AvantPyException(Exception):
    def __init__(self, msg, args):
        super().__init__(msg)
        self.msg = msg
        self.args = args


class IfnobreakError(AvantPyException):
    pass

class TrynobreakError(AvantPyException):
    pass

class NobreakMustBeFirstError(AvantPyException):
    pass

class NobreakSyntaxError(AvantPyException):
    pass


class RepeatMustBeFirstError(AvantPyException):
    pass