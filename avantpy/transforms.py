"""transforms.py

Keeps track of available dialects, and perform require code transformations.

"""
import glob
import os.path
import runpy
import tokenize
from io import StringIO

MAIN_MODULE_NAME = None
FILE_EXT = []
CONVERT = False
DIFF = False
DICTIONARIES = {}
CURRENT = None
DEBUG = False

def init_dialects():
    '''Find known dialects and create corresponding dictionaries'''
    dialects = glob.glob(os.path.dirname(__file__) + "/dialects/*.py")
    for f in dialects:
        if os.path.isfile(f) and not f.endswith("__init__.py"):
            name = os.path.basename(f)[:-3]
            FILE_EXT.append("py" + name)
            dialect = runpy.run_path(f)
            dialect_dict = {v: k for k, v in dialect[name].items()}
            DICTIONARIES["py" + name] = dialect_dict
            DICTIONARIES[name] = dialect[name]

init_dialects()



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

    reverse_dict = DICTIONARIES[CURRENT[2:]]
    repeat_keyword = reverse_dict["repeat"]
    while_keyword = reverse_dict["while"]
    until_keyword = reverse_dict["until"]
    forever_keyword = reverse_dict["forever"]

    nb = source.count(repeat_keyword)
    if nb != 0:
        var_names = get_unique_variable_names(source, nb)
    else:
        var_names = []

    toks = tokenize.generate_tokens(StringIO(source).readline)
    result = []
    prev_lineno = -1
    prev_col = 0
    repeat_loop = False
    repeat_n = False

    for tok_type, tok_str, start, end, _ in toks:
        start_line, start_col = start
        end_line, end_col = end
        # ensure spacing of original file is preserved
        if not repeat_loop:
            if start_line > prev_lineno:
                prev_col = 0
            if start_col > prev_col and tok_str != "\n":
                result.append(" " * (start_col - prev_col))
        prev_col = end_col
        prev_lineno = end_line
        # start substitutions

        if tok_type == tokenize.NAME and tok_str == repeat_keyword:
            repeat_loop = True
        elif repeat_loop and tok_str in [while_keyword, until_keyword, forever_keyword]:
            if tok_str == while_keyword:
                result.append('while')
            elif tok_str == until_keyword:
                result.append('while not')
            else:
                result.append('while True')
            repeat_loop = False
        elif repeat_loop:
            result.append('for %s in range(' % var_names.pop())
            result.append(tok_str)
            repeat_loop = False
            repeat_n = True
        elif repeat_n and tok_str ==':':
            result.append("):")
            repeat_n = False
        elif tok_type == tokenize.NAME and tok_str in dictionary:
            result.append(dictionary[tok_str])
        else:
            result.append(tok_str)
    source = "".join(result)
    if DEBUG:
        print(source)
    return source

ALL_NAMES = []

def get_unique_variable_names(source, nb):
    '''returns a list of possible variables names that
       are not found in the original text.'''
    base_name = 'COUNT_'
    var_names = []
    i = 0
    j = 0
    while j < nb:
        tentative_name = base_name + str(i)
        if source.count(tentative_name) == 0 and tentative_name not in ALL_NAMES:
            var_names.append(tentative_name)
            ALL_NAMES.append(tentative_name)
            j += 1
        i += 1
    return var_names