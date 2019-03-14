"""translations: upper.py


This file can be used as a template for translations in other languages.
"""

# Note: as a reminder that these are the error messages from the upper(case)
# dialect, we begin them with the all-caps words AVANTPY EXCEPTION or
# PYTHON EXCEPTION

upper = {
    "IfNobreakError": """
    AVANTPY EXCEPTION: IfNobreakError\n
    Error found in file {filename} on line {nobreak_linenumber}.\n
{partial_source}

    The AvantPy {nobreak_kwd} keyword cannot be used in an IF/ELIF/ELSE clause
    (Python: if/elif/else).
""",

    "NobreakFirstError": """
        AVANTPY EXCEPTION: NobreakFirstError\n
        The AvantPy {nobreak_kwd} keyword must begin a new statement.\n
        Error found in file {filename} on line {linenumber}.\n
            Line {linenumber}: {nobreak_line}
    """,

    "NobreakSyntaxError": """
        AVANTPY EXCEPTION: NobreakSyntaxError\n
        The AvantPy {nobreak_kwd} keyword must begin a new statement
        matching a FOR or WHILE loop.\n
        Error found in file {filename} on line {linenumber}.\n
            Line {linenumber}: {nobreak_line}
    """,

    "RepeatFirstError": """
        AVANTPY EXCEPTION: RepeatFirstError\n
        The AvantPy {repeat_kwd} keyword must begin a new statement.\n
        Error found in file {filename} on line {linenumber}.\n
            Line {linenumber}: {repeat_line}
    """,

    "TryNobreakError": """
        AVANTPY EXCEPTION: TryNobreakError\n
        The AvantPy {nobreak_kwd} keyword cannot be used in a TRY/EXCEPT/ELSE
        clause (Python: try/except/else).\n
        Error found in file {filename} on line {nobreak_linenumber}.\n
            Line {try_linenumber}: {try_line}\n
            Line {nobreak_linenumber}: {nobreak_line}
    """,
}
