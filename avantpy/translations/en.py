"""translations: en.py"""

en = {}

en[
    "IfNobreakError"
] = """
    AVANTPY EXCEPTION: IfNobreakError\n
    Error found in file {filename} on line {nobreak_linenumber}.\n
{partial_source}

    The AvantPy {nobreak_kwd} keyword cannot be used in an if/elif/else clause.
""",

en[
    "RepeatFirstError"
] = """
AvantPy exception:RepeatFirstError

    The AvantPy {repeat_kwd} keyword must begin a new statement.

Error found in file '{filename}'.

    Line {linenumber}: {repeat_line}
"""
