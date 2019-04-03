"""pyupper.py
You can use this file as a template.

Inside a file named xx.py, create a dictionaries copied from
the example below, and name it 'xx' instead of 'upper'.
The keys should be identical to those of this file;
the values should be translated into the target language.
As an example, we provide a new English Python dialect where
we use 'function' as a synonym for 'lambda'.
"""

pyupper = {
    "False": "FALSE",
    "None": "NONE",
    "True": "TRUE",
    "and": "AND",
    "as": "AS",
    "assert": "ASSERT",
    "async": "async",  # do not translate
    "await": "await",  # as these are not for beginners
    "break": "BREAK",
    "class": "CLASS",
    "continue": "CONTINUE",
    "def": "DEF",
    "del": "DEL",
    "elif": "ELIF",
    "else": ["ELSE", "NOBREAK"],  # Special case
    "except": "EXCEPT",
    "finally": "FINALLY",
    "for": "FOR",
    "from": "FROM",
    "global": "GLOBAL",
    "if": "IF",
    "import": "IMPORT",
    "in": "IN",
    "is": "IS",
    "lambda": "FUNCTION",  # Clearer for beginners
    "nonlocal": "NONLOCAL",
    "not": "NOT",
    "or": "OR",
    "pass": "PASS",
    "raise": "RAISE",
    "return": "RETURN",
    "try": "TRY",
    "while": "WHILE",
    "with": "WITH",
    "yield": "YIELD",
    # Special loop keywords
    "repeat": "REPEAT",
    "forever": "FOREVER",
    "until": "UNTIL",
    # a few builtins useful for beginners
    "input": "INPUT",
    "print": "PRINT",
    "range": "RANGE",
    "exit": "EXIT",  # useful for console
    # a well-known python expression
    '__name__ == "__main__"': "NOTIMPORTED",
}
