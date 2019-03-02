"""transforms.py

Keeps track of available dialects, and perform require code transformations.

"""
import tokenize
from io import StringIO

MAIN_MODULE_NAME = None
FILE_EXT = []
CONVERT = False
DIFF = False
DICTIONARIES = {}
CURRENT = None


def translate(source):
    """A dictionary with a one-to-one translation of keywords is used
    to provide the transformation.
    """
    if CURRENT not in DICTIONARIES:
        return source
    dictionary = DICTIONARIES[CURRENT]
    toks = tokenize.generate_tokens(StringIO(source).readline)
    result = []
    for toktype, tokvalue, _, _, _ in toks:
        if toktype == tokenize.NAME and tokvalue in dictionary:
            result.append((toktype, dictionary[tokvalue]))
        else:
            result.append((toktype, tokvalue))
    return tokenize.untokenize(result)