"""translations: upper.py


This file can be used as a template for translations in other languages.
"""

# Note: as a reminder that these are the error messages from the upper(case)
# dialect, we begin them with the all-caps words AVANTPY EXCEPTION.

upper = {
    "IfNobreakError": """
    AVANTPY EXCEPTION: IfNobreakError\n
    Error found in file '{filename}' on line {nobreak_linenumber}.\n
    Dialect used: {dialect}
    \n{partial_source}

    The AvantPy {nobreak_kwd} keyword cannot be used in
    an IF/ELIF/ELSE clause (Python: if/elif/else).
""",
    "MismatchedBracketsError": """
    AVANTPY EXCEPTION: MismatchedBracketsError\n
    Error found in file '{filename}' on lines
    [{open_linenumber} - {close_linenumber}].\n
    Dialect used: {dialect}
    \n{partial_source}

    The opening {open_bracket} does not match the closing {close_bracket}.
""",
    "MissingLeftBracketError": """
    AVANTPY EXCEPTION: MissingLeftBracketError\n
    Error found in file '{filename}' on line {linenumber}.\n
    Dialect used: {dialect}
    \n{partial_source}

    The closing {bracket} does not match anything.
""",
    "MissingRepeatError": """
    AVANTPY EXCEPTION: MissingRepeatError\n
    Error found in file '{filename}' on line {linenumber}.\n
    Dialect used: {dialect}
    \n{partial_source}

    The AvantPy {keyword} keyword can be used only when preceded by
    REPEAT.
""",
    "NameError": """
    PYTHON EXCEPTION: {python_display}\n
    Error found in file '{filename}' on line {linenumber}.\n
    Dialect used: {dialect}
    \n{partial_source}

    A NameError exception indicates that a variable or
    function name is not known to Python.
    Most often, this is because there is a spelling mistake; however, sometimes
    it is because it is used before being defined or given a value.
    In your program, the unknown variable or function is '{var_name}'.
""",
    "NobreakFirstError": """
    AVANTPY EXCEPTION: NobreakFirstError\n
    Error found in file '{filename}' on line {linenumber}.\n
    Dialect used: {dialect}
    \n{partial_source}

    The AvantPy {nobreak_kwd} keyword can be used instead of ELSE (Python: else)
    only when it begins a new statement for loops.
""",
    "NobreakSyntaxError": """
    AVANTPY EXCEPTION: NobreakSyntaxError\n
    Error found in file '{filename}' on line {linenumber}.\n
    Dialect used: {dialect}
    \n{partial_source}

    The AvantPy {nobreak_kwd} keyword can only be used as a replacement
    of ELSE (Python: else) with a matching FOR or WHILE loop
    (Python: for/while).
""",
    "RepeatFirstError": """
    AVANTPY EXCEPTION: RepeatFirstError\n
    Error found in file '{filename}' on line {linenumber}.\n
    Dialect used: {dialect}
    \n{partial_source}

    The AvantPy {repeat_kwd} keyword can only be used to begin
    a new loop (Python: equivalent to 'for' or 'while' loop).
""",
    "TryNobreakError": """
    AVANTPY EXCEPTION: TryNobreakError\n
    Error found in file '{filename}' on line {nobreak_linenumber}.\n
    Dialect used: {dialect}
    \n{partial_source}

    The AvantPy {nobreak_kwd} keyword cannot be used in
    a TRY/EXCEPT/ELSE/FINALLY clause (Python: try/except/else/finally).
""",
    "UnknownLanguageError": """
    AVANTPY EXCEPTION: UnknownLanguageError\n

    The following unknown language was requested: {lang}.
    The known languages are: {all_langs}.
""",
    "UnknownDialectError": """
    AVANTPY EXCEPTION: UnknownDialectError\n

    The following unknown dialect was requested: {dialect}.
    The known dialects are: {all_dialects}.
""",
}
