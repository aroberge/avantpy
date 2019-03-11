"""translations: en.py"""

en = {}

en[
    "IfnobreakError"
] = """
AvantPy exception: IfnobreakError

    The AvantPy {nobreak_kwd} keyword cannot be used in an if/elif/else clause.

Error found in file '{filename}':

    Line {if_linenumber}: {if_line}

    Line {nobreak_linenumber}: {nobreak_line}
"""

en[
    "RepeatMustBeFirstError"
] = """
AvantPy exception:RepeatMustBeFirstError

    The AvantPy {repeat_kwd} keyword must begin a new statement.

Error found in file '{filename}'.

    Line {linenumber}: {repeat_line}
"""
