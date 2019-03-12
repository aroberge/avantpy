"""translations: upper.py"""

upper = {}

upper[
    "IfnobreakError"
] = """
AVANTPY EXCEPTION: IfnobreakError

    THE AVANTPY {nobreak_kwd} KEYWORD CANNOT BE USED IN AN IF/ELIF/ELSE CLAUSE
    (Python: if/elif/else).

ERROR FOUND IN FILE '{filename}'.

    LINE {if_linenumber}: {if_line}

    LINE {nobreak_linenumber}: {nobreak_line}
"""

upper[
    "TrynobreakError"
] = """
AVANTPY EXCEPTION: TrynobreakError

    THE AVANTPY {nobreak_kwd} KEYWORD CANNOT BE USED IN A TRY/EXCEPT/ELSE CLAUSE
    (Python: try/except/else).

ERROR FOUND IN FILE '{filename}'.

    LINE {try_linenumber}: {try_line}

    LINE {nobreak_linenumber}: {nobreak_line}
"""

upper[
    "NobreakMustBeFirstError"
] = """
AVANTPY EXCEPTION: NobreakMustBeFirstError

    THE AVANTPY {nobreak_kwd} KEYWORD MUST BEGIN A NEW STATEMENT.

ERROR FOUND IN FILE '{filename}'.

    LINE {linenumber}: {nobreak_line}
"""

upper[
    "NobreakSyntaxError"
] = """
AVANTPY EXCEPTION: NobreakSyntaxError

    THE AVANTPY {nobreak_kwd} KEYWORD MUST BEGIN A NEW STATEMENT WHICH 
    DOES NOT MATCH A VALID BLOCK.

ERROR FOUND IN FILE '{filename}'.

    LINE {linenumber}: {nobreak_line}
"""

upper[
    "RepeatMustBeFirstError"
] = """
AVANTPY EXCEPTION: RepeatMustBeFirstError

    THE AVANTPY {repeat_kwd} KEYWORD MUST BEGIN A NEW STATEMENT.

ERROR FOUND IN FILE '{filename}'.

    LINE {linenumber}: {repeat_line}
"""
