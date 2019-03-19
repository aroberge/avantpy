"""transcode.py

Used to convert sources from one dialect into another.
"""

import os
import tokenize
from io import StringIO

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
    if not source:
        print("A valid source must be given.")
        return None

    if from_dialect is None or not state.is_dialect(from_dialect):
        print("from_dialect %s' is not a valid dialect." % from_dialect)
        return None

    if to_dialect is None or not state.is_dialect(to_dialect):
        print("to_dialect %s' is not a valid dialect." % to_dialect)
        return None

    from_lang = state.get_from_python(from_dialect)
    to_lang = state.get_from_python(to_dialect)

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

    return "".join(result)


def transcode_file(filename, from_dialect, to_dialect):
    """to be written"""

    # source_file should be provided with no extension; the extension
    # will be added based on the value for from_dialect
    assert filename is not None
    cwd = os.getcwd()
    source_path = os.path.abspath(os.path.join(cwd, filename)) + "." + from_dialect
    if not os.path.isfile(source_path):
        print("%s does not exist." % source_path)
        return
    target_path = os.path.abspath(os.path.join(cwd, filename)) + "." + to_dialect

    with open(source_path, encoding="utf8") as f:
        source = f.read()

    target = transcode(source, from_dialect, to_dialect)
    # print(target)

    # print(target_path)

    with open(target_path, "w", encoding="utf8") as f:
        f.write(target)
