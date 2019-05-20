"""
This module contains all the necessary functions, classes and methods
to take a file written in a given dialect and convert it into Python.
In doing so, it can identify some mistakes and raise some custom
exceptions which can be used to inform users in a way that is less
intimidating than the usual Python tracebacks.

The following can definitely be skipped unless you are interested in
(most of) the gory details.

AvantPy uses Python's ``tokenize`` module to convert a
source into a sequence of tokens. A token might be the name
of a variable, an operator, a parenthesis, a string, etc.

AvantPy analyses these tokens,
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

This could make it more difficult to compare the original
code with the converted one, as it is possible to do
using one of the utilises provided with AvantPy,
or any "diff" program.
As a result, we do not use Python's
untokenize function, and explicitly keep track of spacing
between tokens.

To understand how the conversion process works, it is useful to review
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

E. Brackets

In Python, brackets must always come in pairs: (...), [...],
{...}. In the course of processing the file, if we identify
brackets which are not paired correctly, an exception
is raised.

F. Remaining tokens

Any remaining token is left as is; it is assumed to be valid
Python.
"""
import os
import tokenize
from io import StringIO

from . import exceptions
from .session import state
from .utils import Token


# =================================
# Note: the strings in this module do not need to be translated.
# In particular, the exception 'messages' can essentially be taken
# as comments, since they will be properly processed (and translated)
# in another module.
# =================================


def get_unique_variable_names(source, repeat_kwd, all_count_names=[]):
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
        if source.count(tentative_name) == 0 and tentative_name not in all_count_names:
            var_names.append(tentative_name)
            all_count_names.append(tentative_name)
            j += 1
        i += 1
    return var_names


class Converter:
    """This class uses Python's ``tokenize`` module to convert a
    source into a sequence of tokens. A token might be the name
    of a variable, an operator, a parenthesis, a string, etc.

    It processes one token at a time, identifying potential misuses,
    replacing some tokens written into a different dialect until all
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

    This could make it more difficult to compare the original
    code with the converted one, as it is possible to do
    using one of the utilises provided with AvantPy,
    or any "diff" program.
    As a result, we do not use Python's
    untokenize function, and explicitly keep track of spacing
    between tokens."""

    def __init__(self, source, dialect=None, filename=None):
        """Initializes variables that are used to convert a program
           written in a given dialect into Standard Python.
        """
        if dialect is not None:
            state.set_dialect(dialect)
        self.dialect = state.get_dialect()
        self.source = source

        if self.dialect is not None:
            self.filename = filename
            self.init_dialect_vars()
            self.init_bookkeeping_vars()

    def convert(self):
        """Uses Python's tokenize module to generate tokens from a source.

           It calls a function to process each token in turn, and combine
           the results to returned a transformed source.
        """
        if self.dialect is None:
            return self.source
        tokens = tokenize.generate_tokens(StringIO(self.source).readline)
        for tok in tokens:
            token = Token(tok)
            self.process_token(token)

        return "".join(self.result)

    def init_dialect_vars(self):
        """Initialises variables that are dependent on a given dialect."""

        self.lang_to_py = state.get_to_python(self.dialect)
        py_to_lang = state.get_from_python(self.dialect)

        self.if_kwd = py_to_lang["if"]
        self.elif_kwd = py_to_lang["elif"]
        self.else_kwd = py_to_lang["else"][0]
        self.nobreak_kwd = py_to_lang["else"][1]
        self.repeat_kwd = py_to_lang["repeat"]
        self.for_kwd = py_to_lang["for"]
        self.while_kwd = py_to_lang["while"]
        self.until_kwd = py_to_lang["until"]
        self.forever_kwd = py_to_lang["forever"]
        self.loops_with_else = [
            "for",
            "while",
            self.for_kwd,
            self.while_kwd,
            self.repeat_kwd,
        ]
        self.if_blocks = ["if", self.if_kwd]
        self.try_kwd = py_to_lang["try"]
        self.except_kwd = py_to_lang["except"]
        self.finally_kwd = py_to_lang["finally"]
        self.try_blocks = ["try", self.try_kwd]
        self.blocks_with_else = self.if_blocks + self.try_blocks + self.loops_with_else

    def init_bookkeeping_vars(self):
        """Initialises variables that are used for bookkeeping"""
        self.brackets = []  # keeps track where (), [], {} occur
        self.indentations = {}  # keeps track of indentation levels of some blocks

        # variable names to be used in
        #    for variable_name in range(...):
        self.count_names = get_unique_variable_names(self.source, self.repeat_kwd)

        self.result = []  # accumulates transformed tokens
        self.prev_lineno = -1
        self.prev_col = 0
        self.just_processed_repeat_kwd = False
        self.repeat_n = False
        self.repeat_line = False
        self.begin_new_line = True
        self.last_col = 0

    def process_token(self, token):
        """Determines what to do for each individual token."""

        # including indentation as a token can mess up the determination
        # of whether or not a keyword appears at the beginning of a new
        # line. Thus, we discard such spaces, and keep track of the required
        # spacing elsewhere.
        if not token.string.strip(" \t"):
            return

        self.begin_new_line = token.start_line != self.prev_lineno

        self.preserve_repeat_spacing(token)

        if token.string == self.repeat_kwd:
            self.process_repeat(token)

        elif self.just_processed_repeat_kwd:
            self.process_after_repeat(token)

        elif self.repeat_n and token.string == ":":
            if self.brackets:
                self.raise_missing_repeat_colon(token.start_line, token.last_col)
            self.result.append("):")
            self.repeat_line = False
            self.repeat_n = False

        elif self.begin_new_line and self.repeat_line:
            self.raise_missing_repeat_colon(token.start_line - 1, self.last_col)

        elif self.repeat_line and token.string == ":":
            if self.brackets:  # Inside a slice or other construct with colon
                self.raise_missing_repeat_colon(token.start_line, self.last_col)
            self.repeat_line = False
            self.result.append(":")

        elif not self.just_processed_repeat_kwd and token.string in [
            self.forever_kwd,
            self.until_kwd,
        ]:
            self.do_until_forever_error(token)

        elif token.string in self.blocks_with_else:
            if self.begin_new_line:
                # keeping track of beginning of for/while/if block so that
                # we can tell if replacing 'nobreak' by 'else' makes sense
                self.indentations[token.start_col] = [token.string, token.start_line]
            if token.string in self.lang_to_py:
                self.result.append(self.lang_to_py[token.string])
            else:
                self.result.append(token.string)

        elif token.string in "([{":
            self.brackets.append((token.string, token.start_line))
            self.result.append(token.string)

        elif token.string in ")]}":
            self.do_close_bracket(token)

        elif token.string == self.nobreak_kwd:
            self.process_nobreak(token)

        elif token.string in self.lang_to_py:
            self.result.append(self.lang_to_py[token.string])

        else:
            self.result.append(token.string)

    def raise_missing_repeat_colon(self, linenumber, last_col):
        """Raised if a repeat statement does not end with a colon on the same
           line with no other colon appearing on that line.
        """
        raise exceptions.MissingRepeatColonError(
            "Missing colon on line beginning with repeat",
            (
                {
                    "repeat_kwd": self.repeat_kwd,
                    "linenumber": linenumber,
                    "filename": self.filename,
                    "source": self.source,
                    "offset": last_col,
                },
            ),
        )

    def do_close_bracket(self, token):
        """Determines if a closing bracket ), ], or }, matches a previously
           opened one, and raises an error if that is not the case.
        """
        try:
            previous_bracket = self.brackets.pop()
        except IndexError:
            raise exceptions.MissingLeftBracketError(
                "Closing bracket found with no matching opening one",
                (
                    {
                        "bracket": token.string,
                        "linenumber": token.start_line,
                        "offset": token.end_col,
                        "filename": self.filename,
                        "source": self.source,
                    },
                ),
            )

        open_bracket = previous_bracket[0]
        if (
            (open_bracket == "(" and token.string != ")")
            or (open_bracket == "[" and token.string != "]")
            or (open_bracket == "{" and token.string != "}")
        ):
            raise exceptions.MismatchedBracketsError(
                "Closing bracket found matching a different opening one.",
                (
                    {
                        "close_bracket": token.string,
                        "offset": token.end_col,
                        "open_bracket": open_bracket,
                        "open_linenumber": previous_bracket[1],
                        "linenumber": token.start_line,
                        "filename": self.filename,
                        "source": self.source,
                    },
                ),
            )
        else:
            self.result.append(token.string)

    def preserve_repeat_spacing(self, token):
        """ We ensure spacing of original file is preserved,
            including space between tokens.
            When self.just_processed_repeat_kwd is True, it means we just saw
            the repeat keyword which can simply be dropped;
            we don't need add the space between "repeat" and the next token.
        """
        if not self.just_processed_repeat_kwd:
            if token.start_line > self.prev_lineno:
                self.last_col = self.prev_col
                self.prev_col = 0
            if token.start_col > self.prev_col and token.string != "\n":
                self.result.append(" " * (token.start_col - self.prev_col))
        self.prev_col = token.end_col
        self.prev_lineno = token.end_line

    def do_until_forever_error(self, token):
        """This function is called when we see a keyword equivalent to
           ``until`` or ``forever`` in a given dialect without them
           being preceeded by the keyword ``repeat``. This is not allowed.
        """
        assert not self.just_processed_repeat_kwd
        raise exceptions.MissingRepeatError(
            "until and forever must be preceeded by repeat",
            (
                {
                    "keyword": token.string,
                    "linenumber": token.start_line,
                    "offset": token.end_col,
                    "filename": self.filename,
                    "source": self.source,
                    "repeat_kwd": self.repeat_kwd,
                },
            ),
        )

    def process_after_repeat(self, token):
        """After we see the ``repeat`` keyword, there are four possibilities:

               1. the keyword ``until`` follows

               2. the keyword ``until`` follows

               3. the keyword ``forever`` follows

               4. it is meant to be followed by some_expression which evaluates
                  to an integer.
        """
        self.just_processed_repeat_kwd = False
        if token.string in [self.while_kwd, self.until_kwd, self.forever_kwd]:
            if token.string == self.while_kwd:
                self.result.append("while")
            elif token.string == self.until_kwd:
                self.result.append("while not")
            else:
                self.result.append("while True")
        else:
            self.repeat_n = True
            self.result.append("for %s in range(" % self.count_names.pop())
            self.result.append(token.string)

    def process_nobreak(self, token):
        """The ``nobreak`` keyword is allowed to replace ``else`` in
           a ``while`` or ``for`` loop only.
        """
        if (
            self.begin_new_line
            and token.start_col in self.indentations
            and self.indentations[token.start_col][0] in self.loops_with_else
        ):
            self.result.append("else")
        else:
            self.handle_nobreak_error(token)

    def process_repeat(self, token):
        """This identifies if ``repeat`` begins a new line; if so, we
           simply set up a flag to indicate that we just saw this keyword,
           and otherwise drop it.

           If it does not begin a new line, we raise an exception.
        """
        if not self.begin_new_line:  # this is not allowed to happen
            raise exceptions.RepeatFirstError(
                "repeat must be first statement on a line",
                (
                    {
                        "repeat keyword": token.string,
                        "offset": token.end_col,
                        "linenumber": token.start_line,
                        "filename": self.filename,
                        "source": self.source,
                    },
                ),
            )
        self.just_processed_repeat_kwd = True
        self.repeat_line = True

    def handle_nobreak_error(self, token):
        """Deals with identified misuses of the ``nobreak`` keyword."""
        if not self.begin_new_line:
            raise exceptions.NobreakFirstError(
                "nobreak must be first statement on a line",
                (
                    {
                        "nobreak keyword": token.string,
                        "offset": token.end_col,
                        "linenumber": token.start_line,
                        "filename": self.filename,
                        "source": self.source,
                        "dialect": self.dialect,
                        "for_kwd": self.for_kwd,
                        "while_kwd": self.while_kwd,
                        "else_kwd": self.else_kwd,
                    },
                ),
            )
        elif (
            token.start_col in self.indentations
            and self.indentations[token.start_col][0] in self.if_blocks
        ):
            raise exceptions.IfNobreakError(
                "Keyword nobreak found matching if/elif",
                (
                    {
                        "if_string": self.indentations[token.start_col][0],
                        "if_linenumber": self.indentations[token.start_col][1],
                        "nobreak keyword": token.string,
                        "offset": token.end_col,
                        "linenumber": token.start_line,
                        "filename": self.filename,
                        "if_kwd": self.if_kwd,
                        "elif_kwd": self.elif_kwd,
                        "else_kwd": self.else_kwd,
                    },
                ),
            )
        elif (
            token.start_col in self.indentations
            and self.indentations[token.start_col][0] in self.try_blocks
        ):
            raise exceptions.TryNobreakError(
                "Keyword nobreak found matching try/except",
                (
                    {
                        "try_string": self.indentations[token.start_col][0],
                        "try_linenumber": self.indentations[token.start_col][1],
                        "nobreak keyword": token.string,
                        "offset": token.end_col,
                        "linenumber": token.start_line,
                        "filename": self.filename,
                        "try_kwd": self.try_kwd,
                        "except_kwd": self.except_kwd,
                        "else_kwd": self.else_kwd,
                        "finally_kwd": self.finally_kwd,
                    },
                ),
            )
        else:
            raise exceptions.NobreakSyntaxError(
                "Keyword nobreak not matching a valid block",
                (
                    {
                        "nobreak keyword": token.string,
                        "offset": token.end_col,
                        "linenumber": token.start_line,
                        "filename": self.filename,
                        "source": self.source,
                        "for_kwd": self.for_kwd,
                        "while_kwd": self.while_kwd,
                        "else_kwd": self.else_kwd,
                    },
                ),
            )


def convert(source, dialect=None, filename=None):
    """Normally used from other functions to call for a conversion
       of a Python source from a given dialect into Python.
    """
    if dialect is not None and not state.is_dialect(dialect):
        # we don't know how to convert this
        return source

    converter = Converter(source, dialect=dialect, filename=filename)
    return converter.convert()


def transcode(source, from_dialect, to_dialect):
    """Transforms a source (string) written in a known dialect into
       an equivalent version written in a different dialect.
       Spacing between tokens is preserved. This means that if a source
       is transformed from dialect xx to dialect yy, and that the result
       is transformed back to dialect xx, the original source should be
       recovered.

       Returns either the transformed source as a string, or None
       if something prevented the transformation to be successful.
    """
    # In many ways, this is a simplified version of Convert, but where
    # we assume that the syntax of the source is valid.
    if from_dialect == to_dialect:
        return source

    if to_dialect == "py":
        return convert(source, dialect=from_dialect, filename="<transcode>")

    if from_dialect == "py":
        from_python = True
        from_dialect = "pyen"
    else:
        from_python = False

    from_lang = state.get_from_python(from_dialect)
    to_lang = state.get_from_python(to_dialect)

    if from_python:
        from_lang["lambda"] = "lambda"  # intead of "function" in pyen

    new_dict = {}
    for key, from_value in from_lang.items():
        to_value = to_lang[key]
        if isinstance(from_value, str):
            new_dict[from_value] = to_value
        else:
            for f, t in zip(from_value, to_value):
                new_dict[f] = t

    result = []  # accumulates transformed tokens
    prev_lineno = -1
    prev_col = 0

    tokens = tokenize.generate_tokens(StringIO(source).readline)
    for tok in tokens:
        token = Token(tok)
        if not token.string.strip(" \t"):
            continue
        if token.start_line > prev_lineno:
            prev_col = 0
        if token.start_col > prev_col and token.string != "\n":
            result.append(" " * (token.start_col - prev_col))
        prev_col = token.end_col
        prev_lineno = token.end_line

        if token.string in new_dict:
            result.append(new_dict[token.string])
        else:
            result.append(token.string)

    result = "".join(result)

    if from_python:
        result = "".join(result)
        result.replace('__name__ == "__main__"', to_lang['__name__ == "__main__"'])

    return result


def transcode_file(from_path, to_path):
    """Convenience function to be used from the command line."""

    cwd = os.getcwd()
    source_path = os.path.normpath(os.path.abspath(os.path.join(cwd, from_path)))
    if not os.path.isfile(source_path):
        print("%s does not exist." % source_path)
        return
    target_path = os.path.normpath(os.path.abspath(os.path.join(cwd, to_path)))

    _, extension = os.path.splitext(source_path)
    from_dialect = extension[1:]

    _, extension = os.path.splitext(target_path)
    to_dialect = extension[1:]

    with open(source_path, encoding="utf8") as f:
        source = f.read()

    target = transcode(source, from_dialect, to_dialect)

    with open(target_path, "w", encoding="utf8") as f:
        f.write(target)
