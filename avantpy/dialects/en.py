"""en.py
You can use this file as a template.

Inside a file named xx.py, create a dictionaries copied from
the example below, and name it 'xx' instead of 'en'.
The keys should be identical to those of 'en';
the values should be translated into the target language.
As an example, we provide a new English Python dialect where
we use 'function' as a synonym for 'lambda'.
"""

en = {
    "False": "False",
    "None": "None",
    "True": "True",
    "and": "and",
    "as": "as",
    "assert": "assert",
    #'async': 'async',  # do not translate
    #'await': 'await',  # as these are not for beginners
    "break": "break",
    "class": "class",
    "continue": "continue",
    "def": "def",
    "del": "del",
    "elif": "elif",
    "else": ["else", "nobreak"],  # Special case
    "except": "except",
    "finally": "finally",
    "for": "for",
    "from": "from",
    "global": "global",
    "if": "if",
    "import": "import",
    "in": "in",
    "is": "is",
    "lambda": "function",  # Clearer for beginners
    "nonlocal": "nonlocal",
    "not": "not",
    "or": "or",
    "pass": "pass",
    "raise": "raise",
    "return": "return",
    "try": "try",
    "while": "while",
    "with": "with",
    "yield": "yield",
    # Special loop keywords
    "repeat": "repeat",
    "forever": "forever",
    "until": "until",
    # a few builtins useful for beginners
    "input": "input",
    "print": "print",
    "range": "range",
    "exit": "exit",  # useful for console
    # a well-known python expression
    '__name__ == "__main__"': "notimported",
}
