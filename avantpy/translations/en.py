"""translations: en.py"""

en = {
    "IfNobreakError": """
    AvantPy exception: IfNobreakError\n
    Error found in file {filename} on line {nobreak_linenumber}.\n
    Dialect used: {dialect}\n
{partial_source}

    The AvantPy {nobreak_kwd} keyword cannot be used in
    an if/elif/else clause.
""",
    "NobreakFirstError": """
    AvantPy exception: NobreakFirstError\n
    Error found in file {filename} on line {linenumber}.\n
    Dialect used: {dialect}\n
{partial_source}

    The AvantPy {nobreak_kwd} keyword can be used instead else
    only when it begins a new statement for loops.
""",
    "NobreakSyntaxError": """
    AvantPy exception: NobreakSyntaxError\n
    Error found in file {filename} on line {linenumber}.\n
    Dialect used: {dialect}\n
{partial_source}

    The AvantPy {nobreak_kwd} keyword can only be used as a replacement
    of else with a matching for or while loop
    (Python: for/while).
""",
    "MissingRepeatError": """
    AvantPy exception: MissingRepeatError\n
    Error found in file {filename} on line {linenumber}.\n
    Dialect used: {dialect}\n
{partial_source}

    The AvantPy {keyword} keyword can be used only when preceded by
    repeat.
""",
    "RepeatFirstError": """
    AvantPy exception: RepeatFirstError\n
    Error found in file {filename} on line {linenumber}.\n
    Dialect used: {dialect}\n
{partial_source}

    The AvantPy {repeat_kwd} keyword can only be used to begin
    a new for or while loop.
""",
    "TryNobreakError": """
    AvantPy exception: TryNobreakError\n
    Error found in file {filename} on line {nobreak_linenumber}.\n
    Dialect used: {dialect}\n
{partial_source}

    The AvantPy {nobreak_kwd} keyword cannot be used in
    a try/except/else/finally.
""",
    "MismatchedBracketsError": """
    AvantPy exception: MismatchedBracketsError\n
    Error found in file {filename} on lines [{open_linenumber} - {close_linenumber}].\n
    Dialect used: {dialect}\n
{partial_source}

    The opening {open_bracket} does not match the closing {close_bracket}.
""",
    "MissingLeftBracketError": """
    AvantPy exception: MissingLeftBracketError\n
    Error found in file {filename} on line {linenumber}.\n
    Dialect used: {dialect}\n
{partial_source}

    The closing {bracket} does not match anything.
""",
    "UnknownLanguage": """
    AvantPy exception: UnknownLanguage\n

    The following unknown language was requested: {lang}.
    The known languages are: {all_langs}.
""",
    "UnknownDialect": """
    AvantPy exception: UnknownDialect\n

    The following unknown dialect was requested: {dialect}.
    The known dialects are: {all_dialects}.
""",
}
