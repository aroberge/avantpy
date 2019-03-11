"""translations: upper.py"""

upper = {}
upper[
    "IfnobreakError"
] = """
AVANTPY EXCEPTION: IfnobreakError

    THE AVANTPY {repeat_kwd} KEYWORD CANNOT BE USED IN AN IF/ELIF/ELSE CLAUSE
    (Python: if/elif/else).

ERROR FOUND IN FILE '{filename}'.

    LINE {if_linenumber}: {if_line}

    LINE {nobreak_linenumber}: {nobreak_line}
"""

upper[
    "RepeatMustBeFirstError"
] = """
AVANTPY EXCEPTION: RepeatMustBeFirstError

    THE AVANTPY {repeat_kwd} KEYWORD MUST BEGIN A NEW STATEMENT.

ERROR FOUND IN FILE '{filename}'.

    LINE {linenumber}: {repeat_line}
"""
