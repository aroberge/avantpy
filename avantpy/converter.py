"""
New version of previous converter
This time, class-based to make it more readable
"""

import tokenize
from io import StringIO

from . import exceptions
from . import session

state = session.state


class Token:
    """Token as generated from tokenize.generate_tokens written here in
       a more convenient form for our purpose.
    """

    def __init__(self, token):
        self.type = token[0]
        self.string = token[1]
        self.start_line, self.start_col = token[2]
        self.end_line, self.end_col = token[3]
        # ignore last parameter which is the logical line


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
    """To be written"""

    def convert(self, source, dialect=None, source_name=None):
        "to be written"
        if dialect is not None:
            self.dialect = state.set_dialect(dialect)
        else:
            self.dialect = state.get_dialect()
            if self.dialect is None:
                return source

        self.source = source
        self.source_name = source_name
        self.init_dialect_vars()
        self.init_bookkeeping_vars()
        tokens = tokenize.generate_tokens(StringIO(source).readline)

        for tok in tokens:
            token = Token(tok)
            self.process_token(token)

        if self.brackets:
            raise exceptions.MissingRightBracketError(
                "One or more bracket was never closed.",
                (
                    {
                        "brackets": self.brackets,
                        "source_name": self.source_name,
                        "source": self.source,
                        "dialect": self.dialect,
                    },
                ),
            )

        return "".join(self.result)

    def init_dialect_vars(self):
        "to be written"

        self.lang_to_py = state.get_to_python(self.dialect)
        py_to_lang = state.get_from_python(self.dialect)

        self.repeat_kwd = py_to_lang["repeat"]
        self.while_kwd = py_to_lang["while"]
        self.until_kwd = py_to_lang["until"]
        self.forever_kwd = py_to_lang["forever"]
        self.loops_with_else = [
            "for",
            "while",
            py_to_lang["for"],
            self.while_kwd,
            self.repeat_kwd,
        ]
        self.if_blocks = ["if", py_to_lang["if"]]
        self.try_blocks = ["try", py_to_lang["try"]]
        self.blocks_with_else = self.if_blocks + self.try_blocks + self.loops_with_else
        self.nobreak_kwd = py_to_lang["else"][1]

    def init_bookkeeping_vars(self):
        "to be written"
        self.brackets = []  # keeps track where (), [], {} occur

        # variable names to be used in
        #    for variable_name in range(...):
        self.count_names = get_unique_variable_names(self.source, self.repeat_kwd)

        # some book-keeping variables used in the for-loop below
        self.result = []
        self.prev_lineno = -1
        self.prev_col = 0
        self.just_processed_repeat_kwd = False
        self.repeat_n = False
        self.begin_new_line = True

        # In order to determine what to do with the nobreak keyword,
        # we keep track of which one among if/while/for and their translation
        # in a given dialect last appeared in a given column
        # format: indentation[column] = keyword
        self.indentations = {}

    def process_token(self, token):

        if not token.string.strip(" \t"):  # we keep track of spacing elsewhere
            return

        self.begin_new_line = token.start_line != self.prev_lineno

        if token.string in "()[]{}":
            self.preprocess_bracket(token)

        if not self.just_processed_repeat_kwd:
            self.preserve_repeat_spacing(token)
            self.prevent_until_forever_misuses(token)

        self.prev_col = token.end_col
        self.prev_lineno = token.end_line

        # keeping track of beginning of for/while/if block so that
        # we can tell if replacing 'nobreak' by 'else' makes sense.
        if self.begin_new_line:
            if token.string in self.blocks_with_else:
                self.indentations[token.start_col] = [token.string, token.start_line]

        if token.string == self.nobreak_kwd:
            self.identify_potential_nobreak_first_errors(token)

        if token.string == self.repeat_kwd:
            self.process_repeat(token)
        elif self.just_processed_repeat_kwd:
            self.process_after_repeat(token)
        elif self.repeat_n and token.string == ":":
            self.result.append("):")
            self.repeat_n = False
        elif token.string == self.nobreak_kwd:
            self.process_nobreak(token)
        elif token.string in self.lang_to_py:
            self.result.append(self.lang_to_py[token.string])
        else:
            self.result.append(token.string)

    def preprocess_bracket(self, token):
        """Keep track of matching brackets so that errors can be flagged"""
        if token.string in "([{":
            self.brackets.append((token.string, token.start_line))
        elif token.string in ")]}":
            try:
                previous_bracket = self.brackets.pop()
            except IndexError:
                raise exceptions.MissingLeftBracketError(
                    "Closing bracket found with no matching opening one",
                    (
                        {
                            "bracket": token.string,
                            "linenumber": token.start_line,
                            "source_name": self.source_name,
                            "source": self.source,
                            "dialect": self.dialect,
                        },
                    ),
                )
            else:
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
                                "open_bracket": open_bracket,
                                "close_linenumber": token.start_line,
                                "open_linenumber": previous_bracket[1],
                                "source_name": self.source_name,
                                "source": self.source,
                                "dialect": self.dialect,
                            },
                        ),
                    )
        return

    def preserve_repeat_spacing(self, token):
        """ We ensure spacing of original file is preserved,
            including space between tokens.
            When self.just_processed_repeat_kwd is True, it means we just saw
            the repeat keyword which can simply be dropped;
            we don't need add the space between "repeat" and the next token.
        """
        if token.start_line > self.prev_lineno:
            self.prev_col = 0
        if token.start_col > self.prev_col and token.string != "\n":
            self.result.append(" " * (token.start_col - self.prev_col))

    def prevent_until_forever_misuses(self, token):
        """If self.just_processed_repeat_kwd is true, this means that we just saw a
           the keywords 'until' or 'forever'
        """
        if token.string in [self.forever_kwd, self.until_kwd]:
            raise exceptions.MissingRepeatError(
                "until and forever must be preceeded by repeat",
                (
                    {
                        "keyword": token.string,
                        "linenumber": token.start_line,
                        "source_name": self.source_name,
                        "source": self.source,
                        "dialect": self.dialect,
                    },
                ),
            )
        return

    def process_after_repeat(self, token):
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
        if (
            token.start_col in self.indentations
            and self.indentations[token.start_col][0] in self.loops_with_else
        ):
            self.result.append("else")
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
                        "linenumber": token.start_line,
                        "source_name": self.source_name,
                        "dialect": self.dialect,
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
                        "linenumber": token.start_line,
                        "source_name": self.source_name,
                        "dialect": self.dialect,
                    },
                ),
            )
        else:
            raise exceptions.NobreakSyntaxError(
                "Keyword nobreak not matching a valid block",
                (
                    {
                        "nobreak keyword": token.string,
                        "linenumber": token.start_line,
                        "source_name": self.source_name,
                        "source": self.source,
                        "dialect": self.dialect,
                    },
                ),
            )

    def process_repeat(self, token):
        if not self.begin_new_line:  # this is not allowed to happen
            raise exceptions.RepeatFirstError(
                "repeat must be first statement on a line",
                (
                    {
                        "repeat keyword": token.string,
                        "linenumber": token.start_line,
                        "source_name": self.source_name,
                        "source": self.source,
                        "dialect": self.dialect,
                    },
                ),
            )
        self.just_processed_repeat_kwd = True

    def identify_potential_nobreak_first_errors(self, token):
        """Identifies potential misuse of nobreak keyword."""
        if not self.begin_new_line:  # this is not allowed to happen
            raise exceptions.NobreakFirstError(
                "nobreak must be first statement on a line",
                (
                    {
                        "nobreak keyword": token.string,
                        "linenumber": token.start_line,
                        "source_name": self.source_name,
                        "source": self.source,
                        "dialect": self.dialect,
                    },
                ),
            )
        return


def convert(source, dialect=None, source_name=None):
    converter = Converter()
    return converter.convert(source=source, dialect=dialect, source_name=source_name)
