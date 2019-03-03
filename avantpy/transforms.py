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
DEBUG = False


def set_debug(val):
    """Used to set DEBUG to either True or False"""
    global DEBUG
    DEBUG = val


def set_lang(lang):
    """Sets the language (Python dialect) to be used in the console.
    
    Valid values typically are two-letter language code such as 'en' or 'fr'.
    """
    global CURRENT
    extension = "py" + lang
    if extension in FILE_EXT:
        CURRENT = extension
        if DEBUG:
            print("lang %s selected" % lang)
        return
    print("unknown dialect: ", lang)


def translate(source):
    """A dictionary with a one-to-one translation of keywords is used
    to provide the transformation.
    """
    if CURRENT not in DICTIONARIES:
        return source
    dictionary = DICTIONARIES[CURRENT]
    toks = tokenize.generate_tokens(StringIO(source).readline)
    result = []
    prev_lineno = -1
    prev_col = 0

    for tok_type, tok_str, start, end, _ in toks:
        start_line, start_col = start
        end_line, end_col = end
        # ensure spacing of original file is preserved
        if start_line > prev_lineno:
            prev_col = 0
        if start_col > prev_col and tok_str != "\n":
            result.append(" " * (start_col - prev_col))
        prev_col = end_col
        prev_lineno = end_line
        # start substitutions
        if tok_type == tokenize.NAME and tok_str in dictionary:
            result.append(dictionary[tok_str])
        else:
            result.append(tok_str)

    source = "".join(result)
    if DEBUG:
        print(source)
    return source
