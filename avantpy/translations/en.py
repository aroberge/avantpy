"""translations: en.py"""

en = {}

en[
    "IfNobreakError"
] = """
AvantPy exception: IfNobreakError

    The AvantPy {nobreak_kwd} keyword cannot be used in an if/elif/else clause.

Error found in file '{filename}':

    Line {if_linenumber}: {if_line}

    Line {nobreak_linenumber}: {nobreak_line}
"""

en[
    "RepeatFirstError"
] = """
AvantPy exception:RepeatFirstError

    The AvantPy {repeat_kwd} keyword must begin a new statement.

Error found in file '{filename}'.

    Line {linenumber}: {repeat_line}
"""
