"""conversion.py

Keeps track of available dialects, and perform require code transformations.

"""
import glob
import os.path
import runpy
import tokenize
from io import StringIO

from . import exceptions

DEBUG = False


def set_debug(val=True):
    """Used to set DEBUG to either True or False,
       with True being the default value.

       Returns: The current value of DEBUG
    """
    global DEBUG
    DEBUG = val
    return DEBUG


class _State:
    """Keeping track of parameters which control some of the
       behaviour of AvantPy."""

    def __init__(self):
        self.dictionaries = {}
        self.all_count_names = []
        self.current_dialect = None
        self.current_lang = None
        self.collect_dialects()
        self.only_one_dialect = False
        self.only_one_lang = False

    def all_dialects(self):
        """Returns a list of all known dialects."""
        if self.only_one_dialect:
            return [self.only_one_dialect]
        return [k for k in self.dictionaries.keys() if k.startswith("py")]

    def collect_dialects(self):
        """Find known dialects and create corresponding dictionaries"""
        dialects = glob.glob(os.path.dirname(__file__) + "/dialects/*.py")
        for f in dialects:
            if os.path.isfile(f) and not f.endswith("__init__.py"):

                lang = os.path.basename(f).split(".")[0]
                dialect = "py" + lang

                _module = runpy.run_path(f)
                from_py = _module[lang]
                self.add_translation(lang, from_py)

                to_py = {}
                for k, v in from_py.items():
                    if isinstance(v, str):
                        to_py[v] = k
                    else:
                        for val in v:
                            to_py[val] = k
                self.add_translation(dialect, to_py)

    def is_dialect(self, dialect):
        """Returns True if `dialect` is a known dialect, False otherwise."""
        if self.only_one_dialect:
            return dialect == self.only_one_dialect
        return dialect.startswith("py") and dialect in self.dictionaries

    def is_lang(self, lang):
        """Returns True if `lang` is known as part of a dialect, False otherwise"""
        if self.only_one_lang:
            return lang == self.only_one_lang
        return (not lang.startswith("py")) and lang in self.dictionaries

    def add_translation(self, name, translation_dict):
        """Adds a translation dict either from a dialect to Python
           or from Python to a given dialect.
        """
        self.dictionaries[name] = translation_dict

    def get_to_python(self, dialect):
        """Returns a dict providing translation from a dialect into Python"""
        assert self.is_dialect(dialect)
        return self.dictionaries[dialect]

    def get_from_python(self, dialect):
        """Returns a dict providing translation from Python into a dialect"""
        lang = dialect[2:]
        assert self.is_lang(lang)
        return self.dictionaries[lang]

    def get_unique_variable_names(self, source, repeat_kwd):
        """Returns a list of possible variables names that
           are not found in the original source and have not been used
           anywhere.
           These variables will be used in expressions such as

               for _COUNT_42 in range(n):

           which will replace

               repeat n:
        """
        nb = source.count(repeat_kwd)
        if nb == 0:
            return []

        base_name = "_COUNT_"
        var_names = []
        i = 0
        j = 0
        while j < nb:
            tentative_name = base_name + str(i)
            if (
                source.count(tentative_name) == 0
                and tentative_name not in self.all_count_names
            ):
                var_names.append(tentative_name)
                self.all_count_names.append(tentative_name)
                j += 1
            i += 1
        return var_names


__state = _State()


def all_dialects():
    """Returns a list of all known dialects."""
    return __state.all_dialects()


def is_dialect(dialect):
    """Returns True if `dialect` is a known dialect, False otherwise."""
    return __state.is_dialect(dialect)


def get_dialect():
    """Returns the current dialect being used."""
    return __state.current_dialect


def set_dialect(dialect=None):
    """Sets the dialect to be used.

    Valid values are of the form "pyXX" where XX denotes a valid two-letter
    language code.  
    If `dialect` is not recognized as being valid, an error message is
    printed.
    """
    if dialect is None:
        return __state.current_dialect
    elif is_dialect(dialect):
        __state.current_dialect = dialect
    else:
        print("Unknown dialect: ", dialect)


def set_lang(lang, only=False):
    """Sets the language and/or Python dialect to be used.
    
    Valid values are typically two-letter language code such as 'en' or 'fr'.

    If `lang` is not a recognized language, an error message is printed.


    If the ``only`` argument is set to ``True``, and ``lang`` is a valid
    value, no other language/dialect will be allowed.
    """
    # Since this function can be used in the console, in order to make it
    # more user friendly, we accept values that start with 'py' such as
    # 'pyfr' as being equivalent to their two-letter language counterpart

    if lang.startswith("py"):
        dialect = lang
        lang = dialect[2:]
    else:
        dialect = "py" + lang

    if is_dialect(dialect):
        set_dialect(dialect)
        __state.current_lang = lang
        if only:
            __state.only_one_dialect = dialect
            __state.only_one_lang = lang
        if DEBUG:
            print("lang %s selected" % lang)
        return
    print("Unknown language: ", lang)


def to_python(source, dialect=None, source_name=None):
    """Converts a source in a known dialect into standard Python.

    This function uses Python's ``tokenize`` module to convert a
    source into a sequence of tokens. A token might be the name
    of a variable, an operator, a parenthesis, a string, etc.

    This function analyses these tokens,
    replacing some written into a different dialect until all
    are converted into standard Python tokens.  Then, these
    are recombined into a string which is the source to be 
    executed.

    Python's tokenize module includes a function, called
    untokenize, which can be used to combine a series of tokens
    into a valid program.  With a normal Python program, doing
    something similar to::

        new_source = untokenize(tokenize(source))

    would be such that executing ``new_source`` would be the same
    as executing ``source``.  However, the spacing between tokens
    would not necessarily be the same for both ``new_source``
    and the original program.  For example, the original program
    may include a line like::

        variable = function( argument )

    which might be converted into::

        variable =function(argument)

    One possibility that AvantPy offers is to run program with the 
    --diff option to show the difference 
    between the code written and standard Python. The difflib
    module, used to do this, shows all differences including
    differences in spaces between tokens.  Since the primary
    goal of the --diff option is to allow users to learn the
    differences between their dialect and standard Python, it is
    important to restrict differences shown to only those that
    are meaningful.  As a result, we do not use Python's
    untokenize function, and explicitly keep track of spacing
    between tokens.

    To understand how this function works, it is useful to review
    all possible cases, from some of the most complex, ending
    with the simplest ones.

    A. ``nobreak``

    AvantPy has an additional keyword, named ``nobreak`` in the
    English dialect, which can be used in ``for`` or ``while``
    loops instead of the standard ``else``, as in::

        while condition:
            # code
        nobreak:
            # code

    However, ``nobreak`` cannot be used in an ``if/elif/else``
    blocks to replace ``else``.  

    Furthermore, ``nobreak`` cannot be used instead of ``else``
    in an assignment such as::

        a = 1 if True else 2

    To identify if a program includes a ``nobreak`` keyword
    mistakenly, every time we see a leading ``for``, ``while``,
    ``if`` or ``elif`` keyword (or their equivalent in a
    given dialect), we note the indentation (column where the
    first character is written) and the corresponding keyword.
    A list containing these keywords is called ``blocks_with_else``
    in this function.

    Later, when we encounter a ``nobreak`` keyword at a given
    indentation, we check to see if the last ``blocks_with_else``
    keyword found at that same indentation was one for which
    it made sense to use ``nobreak`` or not.  If it was a
    loop, we simply replace ``nobreak`` by ``else``. If not,
    we raise a custom exception which is handled elsewhere.

    B. ``repeat``

    In addition to the standard Python loops constructs, AvantPy
    support four additional idioms::

        repeat forever:           # while True:
            pass
        repeat while condition:   # while condition:
            pass
        repeat until condition:   # while not condition:
            pass
        repeat n:                 # for some_var in range(n):
            pass

    For this last case, ``n`` could be an expression, possibly
    spanning multiple lines.

    When we encounter the equivalent to the "repeat" keyword in
    the selected dialect, we must make sure that it is the first
    keyword occurring on a logical line; if not, we raise a
    custom exception.

    If ``repeat`` is the first keyword on a line, we set a flag
    (repeat_loop) to True, preparing to look at the next token.

    a) If the next token is one of ``forever``, ``until``, ``while``,
    or their equivalent in the target dialect
    (remember that including normal Python keywords in a program written
    in a different dialect is allowed)
    we can proceed with the rest in a straightforward manner.

    b) if that is not the case, we set a different flag (repeat_n)
    to True so that we can deal with the relevant for loop.

    For this last case, the variable in the for loop is a dummy
    variable; we must ensure that its name is chosen such that
    it does not occur anywhere else in the source code.
    This is accomplished using a method called
    ``get_unique_variable_names``.

    C. ``nobreak`` and ``repeat``

    A ``repeat`` loop is essentially a ``for`` or a ``while``
    loop. As such, it could have an ``else`` clause which
    has a clearer meaning if the keyword ``nobreak`` is used
    instead.  Thus, just like we mentioned before, we also
    keep track of where a leading ``repeat`` is used.

    D. Direct translation

    If a token does not match one of the cases described above,
    we need to see if it is a term used in the dialect; if
    so, we simply translate it into standard Python.

    E. Remaining tokens

    Any remaining token is left as is; it is assumed to be valid
    Python.
    """
    dialect = set_dialect(dialect)
    if not is_dialect(dialect):
        return source

    lang_to_py = __state.get_to_python(dialect)
    py_to_lang = __state.get_from_python(dialect)

    repeat_kwd = py_to_lang["repeat"]
    while_kwd = py_to_lang["while"]
    until_kwd = py_to_lang["until"]
    forever_kwd = py_to_lang["forever"]
    loops_with_else = ["for", "while", py_to_lang["for"], while_kwd, repeat_kwd]
    if_blocks = ["if", py_to_lang["if"]]
    try_blocks = ["try", py_to_lang["try"]]
    blocks_with_else =  if_blocks + try_blocks + loops_with_else
    nobreak_kwd = py_to_lang["else"][1]

    # variable names to be used in
    #    for variable_name in range(...):
    var_names = __state.get_unique_variable_names(source, repeat_kwd)

    # some book-keeping variables used in the for-loop below
    result = []
    prev_lineno = -1
    prev_col = 0
    repeat_loop = False
    repeat_n = False
    begin_new_line = True

    # In order to determine what to do with the nobreak keyword,
    # we keep track of which one among if/while/for and their translation
    # in a given dialect last appeared in a given column
    # format: indentation[column] = keyword
    indentations = {}

    tokens = tokenize.generate_tokens(StringIO(source).readline)

    for _, tok_str, start, end, _ in tokens:
        if not tok_str.strip(" \t"):  # we keep track of spacing elsewhere
            continue

        # ============
        # Bookkeeping
        # ============

        start_line, start_col = start
        end_line, end_col = end
        begin_new_line = start_line != prev_lineno

        # We ensure spacing of original file is preserved,
        # including space between tokens.
        # When repeat_loop is True, it means we just saw the repeat keyword
        # which can simply be dropped; we don't need add the space
        # between "repeat" and the next token.
        if not repeat_loop:
            if start_line > prev_lineno:
                prev_col = 0
            if start_col > prev_col and tok_str != "\n":
                result.append(" " * (start_col - prev_col))
        prev_col = end_col
        prev_lineno = end_line

        # keeping track of beginning of for/while/if block so that
        # we can tell if replacing 'nobreak' by 'else' makes sense.
        if begin_new_line:
            if tok_str in blocks_with_else:
                indentations[start_col] = [tok_str, start_line]

        if tok_str == nobreak_kwd:
            if not begin_new_line:  # this is not allowed to happen
                raise exceptions.NobreakMustBeFirstError(
                    "nobreak must be first",
                    (
                        {
                            "nobreak keyword": tok_str,
                            "linenumber": start_line,
                            "source_name": source_name,
                            "source": source,
                            "lang": dialect[2:],
                        },
                    ),
                )

        # ========================

        if tok_str == repeat_kwd:
            if not begin_new_line:  # this is not allowed to happen
                raise exceptions.RepeatMustBeFirstError(
                    "repeat must be first",
                    (
                        {
                            "repeat keyword": tok_str,
                            "linenumber": start_line,
                            "source_name": source_name,
                            "source": source,
                            "lang": dialect[2:],
                        },
                    ),
                )
            repeat_loop = True
        elif repeat_loop:
            repeat_loop = False
            if tok_str in [while_kwd, until_kwd, forever_kwd]:
                if tok_str == while_kwd:
                    result.append("while")
                elif tok_str == until_kwd:
                    result.append("while not")
                else:
                    result.append("while True")
            else:
                repeat_n = True
                result.append("for %s in range(" % var_names.pop())
                result.append(tok_str)

        elif repeat_n and tok_str == ":":
            result.append("):")
            repeat_n = False

        elif tok_str in lang_to_py:
            if tok_str == nobreak_kwd:
                if (
                    start_col in indentations
                    and indentations[start_col][0] in loops_with_else
                ):
                    result.append("else")
                elif (
                    start_col in indentations
                    and indentations[start_col][0] in if_blocks
                ):
                    raise exceptions.IfnobreakError(
                        "Keyword nobreak found matching if/elif",
                        (
                            {
                                "if_string": indentations[start_col],
                                "nobreak keyword": tok_str,
                                "linenumber": start_line,
                                "source_name": source_name,
                                "source": source,
                                "lang": dialect[2:],
                            },
                        ),
                    )
                elif (
                    start_col in indentations
                    and indentations[start_col][0] in try_blocks
                ):
                    raise exceptions.TrynobreakError(
                        "Keyword nobreak found matching try/except",
                        (
                            {
                                "try_string": indentations[start_col],
                                "nobreak keyword": tok_str,
                                "linenumber": start_line,
                                "source_name": source_name,
                                "source": source,
                                "lang": dialect[2:],
                            },
                        ),
                    )
                else:
                    raise exceptions.NobreakSyntaxError(
                        "Keyword nobreak not matching a valid block",
                        (
                            {
                                "nobreak keyword": tok_str,
                                "linenumber": start_line,
                                "source_name": source_name,
                                "source": source,
                                "lang": dialect[2:],
                            },
                        ),
                    )
            else:
                result.append(lang_to_py[tok_str])
        else:
            result.append(tok_str)

    source = "".join(result)
    # if DEBUG:
    #     print(source)
    return source
