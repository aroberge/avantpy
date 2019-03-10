'''Custom exceptions'''

class AvantPyException(Exception):
    def __init__(self, msg, args):
        super().__init__(msg)
        self.args = args


class IfnobreakError(AvantPyException):
    pass

