"""The goal of exception_handling.py is to display information about
exceptions being raised in a way that is much easier to understand
for beginners than normal Python tracebacks.  These "friendly" tracebacks
are written so that they can easily be translated into any human language.
"""
import sys
import traceback

from .session import state

ENABLED = True


def disable():
    """Disables custom exception handling"""
    global ENABLED
    ENABLED = False


def _maybe_print(msg, obj, attribute):
    try:
        print(msg, getattr(obj, attribute))
    except AttributeError:
        print(msg, "does not exist")


def get_partial_source(source, begin, end, marks=None):
    """Extracts a few relevant lines from a source file.

       If the number of lines would exceed a certain limit (currently 7)
       the function is called recursively to only show the a few lines
       at the beginning and at the end.
    """
    nb_digits = len(str(end))
    no_mark = "       {:%d}: " % nb_digits
    with_mark = "    -->{:%d}: " % nb_digits
    continuation = "           ..."

    if marks is None:
        marks = []

    result = []
    if end - begin > 7:
        result.append(get_partial_source(source, begin, begin + 2, marks=marks))
        result.append(continuation)
        result.append(get_partial_source(source, end - 2, end, marks=marks))
    else:
        lines = source.split("\n")
        for index, line in enumerate(lines, start=1):
            if index < begin:
                continue
            if index > end:
                break
            if index in marks:
                result.append(with_mark.format(index) + line)
            else:
                result.append(no_mark.format(index) + line)

    return "\n".join(result)


def write_err(msg):
    """Writes a string to sys.stderr."""
    sys.stderr.write(msg)


def write_exception_info(exc, source):
    """Writes the information we have after processing the exception."""
    msg = handle_exception(exc, source)
    if msg is not None:
        write_err(msg)
    else:
        write_err(
            _("An exception was raised for which we have no simplified traceback:\n")
        )
        write_err("name: %s\n" % exc.__class__.__name__)
        write_err("args: " + str(exc.args) + "\n")
        write_err("Python traceback follows:\n\n")
        for item in traceback.format_tb(exc.__traceback__):
            write_err(item)
        write_err("\n")


def handle_exception(exc, source):
    """Generic function to handle exceptions and returns a
       friendlier traceback than Python.

       If the exception is not recognized as one for which a friendlier
       traceback can be provided, None is returned
    """
    if not ENABLED:
        # Let normal Python traceback through
        raise exc

    name = exc.__class__.__name__
    if name in dispatch:
        return dispatch[name](exc, source)
    else:
        return None  # just want to be explicit


# ================= Specific handlers below


def handle_IfNobreakError(exc, source):
    """Handles situation where ``nobreak`` was wrongly use as a
       replacement for ``else`` in an if/elif/else block.
    """
    params = exc.args[0]

    begin = params["if_linenumber"]
    end = params["linenumber"]
    marks = [end]

    partial_source = get_partial_source(source, begin, end, marks=marks)

    info = {
        "filename": params["source_name"],
        "nobreak_kwd": params["nobreak keyword"],
        "partial_source": partial_source,
        "nobreak_linenumber": end,
        "dialect": params["dialect"],
    }

    return _(
        """
    AVANTPY EXCEPTION: IfNobreakError

    Error found in file '{filename}' on line {nobreak_linenumber}.

    Dialect used: {dialect}

{partial_source}

    The AvantPy {nobreak_kwd} keyword cannot be used in
    an IF/ELIF/ELSE clause (Python: if/elif/else).

"""
    ).format(**info)


def handle_MismatchedBracketsError(exc, source):
    """Handles situation where a bracket of one kind '([{'
       is closed with a bracket of a different kind.
    """
    params = exc.args[0]
    begin = params["open_linenumber"]
    end = params["close_linenumber"]
    marks = [begin, end]

    partial_source = get_partial_source(source, begin, end, marks=marks)

    info = {
        "filename": params["source_name"],
        "open_bracket": params["open_bracket"],
        "close_bracket": params["close_bracket"],
        "begin": begin,
        "end": end,
        "partial_source": partial_source,
        "dialect": params["dialect"],
    }
    return _(
        """
    AVANTPY EXCEPTION: MismatchedBracketsError

    Error found in file '{filename}' on lines [{begin} - {end}].

    Dialect used: {dialect}

{partial_source}

    The opening {open_bracket} does not match the closing {close_bracket}.

"""
    ).format(**info)


def handle_MissingLeftBracketError(exc, source):
    """Handles situation where at bracket of one kind ),],}
       is closed without a corresponding open bracket.
    """
    params = exc.args[0]
    linenumber = params["linenumber"]
    begin = linenumber - 1
    end = linenumber + 1
    marks = [linenumber]

    partial_source = get_partial_source(source, begin, end, marks=marks)

    info = {
        "filename": params["source_name"],
        "partial_source": partial_source,
        "dialect": params["dialect"],
        "linenumber": linenumber,
        "bracket": params["bracket"],
    }
    return _(
        """
    AVANTPY EXCEPTION: MissingLeftBracketError

    Error found in file '{filename}' on line {linenumber}.

    Dialect used: {dialect}

{partial_source}

    The closing {bracket} does not match anything.

"""
    ).format(**info)


def handle_MissingRepeatError(exc, source):
    """Handles situation where either ``until`` or ``forever`` was
       used without being preceeded by ``repeat``.
    """
    params = exc.args[0]
    linenumber = params["linenumber"]
    begin = linenumber - 1
    end = linenumber + 1
    marks = [linenumber]

    partial_source = get_partial_source(source, begin, end, marks=marks)

    info = {
        "filename": params["source_name"],
        "keyword": params["keyword"],
        "partial_source": partial_source,
        "linenumber": linenumber,
        "dialect": params["dialect"],
    }
    return _(
        """
    AVANTPY EXCEPTION: MissingRepeatError

    Error found in file '{filename}' on line {linenumber}.

    Dialect used: {dialect}

{partial_source}

    The AvantPy {keyword} keyword can be used only when preceded by REPEAT.

"""
    ).format(**info)


def handle_NameError(exc, source):
    """Handles situation where a NameError is raise."""
    msg = exc.args[0]
    var_name = msg.split("'")[1]
    exc_name = exc.__class__.__name__
    python_display = "{exc_name}: {msg}".format(exc_name=exc_name, msg=msg)

    last_tb_line = traceback.format_tb(exc.__traceback__)[-1]
    # For last_tb_line, we expect something like
    # File "filename", line 1, in <module>
    splitted_line = last_tb_line.split(",")
    filename = last_tb_line[0].replace("File ", "").replace('"', "").strip()
    if filename == "<string>" and state.current_filename is not None:
        filename = state.current_filename

    linenumber = int(splitted_line[1].replace("line ", ""))
    begin = linenumber - 1
    end = linenumber + 1
    marks = [linenumber]

    partial_source = get_partial_source(source, begin, end, marks=marks)

    info = {
        "filename": filename,
        "python_display": python_display,
        "var_name": var_name,
        "partial_source": partial_source,
        "linenumber": linenumber,
        "dialect": state.current_dialect,
    }
    return _(
        """
    PYTHON EXCEPTION: {python_display}

    Error found in file '{filename}' on line {linenumber}.

    Dialect used: {dialect}

{partial_source}

    A NameError exception indicates that a variable or
    function name is not known to Python.
    Most often, this is because there is a spelling mistake; however,
    sometimes it is because it is used before being defined or given a value.
    In your program, the unknown variable or function is '{var_name}'.

"""
    ).format(**info)


def handle_NobreakFirstError(exc, source):
    """Handles situation where ``nobreak`` was wrongly use as a
       replacement for ``else`` in statements like
       var = x if condition else y.
    """
    params = exc.args[0]
    linenumber = params["linenumber"]
    begin = linenumber - 1
    end = linenumber + 1
    marks = [linenumber]

    partial_source = get_partial_source(source, begin, end, marks=marks)

    info = {
        "filename": params["source_name"],
        "nobreak_kwd": params["nobreak keyword"],
        "partial_source": partial_source,
        "linenumber": linenumber,
        "dialect": params["dialect"],
    }
    return _(
        """
    AVANTPY EXCEPTION: NobreakFirstError

    Error found in file '{filename}' on line {linenumber}.

    Dialect used: {dialect}

{partial_source}

    The AvantPy {nobreak_kwd} keyword can be used instead of ELSE
    (Python: else) only when it begins a new statement in FOR/WHILE loops.

"""
    ).format(**info)


def handle_NobreakSyntaxError(exc, source):
    """Handles situation where ``nobreak`` is used without a matching
       ``for`` or ``while`` loop and not already raised.
    """
    params = exc.args[0]

    linenumber = params["linenumber"]
    begin = linenumber - 1
    end = linenumber + 1
    marks = [linenumber]

    partial_source = get_partial_source(source, begin, end, marks=marks)

    info = {
        "filename": params["source_name"],
        "nobreak_kwd": params["nobreak keyword"],
        "partial_source": partial_source,
        "linenumber": linenumber,
        "dialect": params["dialect"],
    }
    return _(
        """
    AVANTPY EXCEPTION: NobreakSyntaxError

    Error found in file '{filename}' on line {linenumber}.

    Dialect used: {dialect}

{partial_source}

    The AvantPy {nobreak_kwd} keyword can only be used as a replacement
    of ELSE (Python: else) with a matching FOR or WHILE loop
    (Python: for/while).

"""
    ).format(**info)


def handle_RepeatFirstError(exc, source):
    """Handles situation where ``repeat`` was uses wrongly as
       it did not appear as the first keyword of a given statement.
    """
    params = exc.args[0]
    linenumber = params["linenumber"]
    begin = linenumber - 1
    end = linenumber + 1
    marks = [linenumber]

    partial_source = get_partial_source(source, begin, end, marks=marks)

    info = {
        "filename": params["source_name"],
        "repeat_kwd": params["repeat keyword"],
        "partial_source": partial_source,
        "linenumber": linenumber,
        "dialect": params["dialect"],
    }
    return _(
        """
    AVANTPY EXCEPTION: RepeatFirstError

    Error found in file '{filename}' on line {linenumber}.

    Dialect used: {dialect}

{partial_source}

    The AvantPy {repeat_kwd} keyword can only be used to begin
    a new loop (Python: equivalent to 'for' or 'while' loop).

"""
    ).format(**info)


def handle_TryNobreakError(exc, source):
    """Handles situation where ``nobreak`` was wrongly use as a
       replacement for ``else`` in an try/except/else/finally block.
    """
    params = exc.args[0]

    begin = params["try_linenumber"]
    end = params["linenumber"]
    marks = [end]

    partial_source = get_partial_source(source, begin, end, marks=marks)

    info = {
        "filename": params["source_name"],
        "nobreak_kwd": params["nobreak keyword"],
        "partial_source": partial_source,
        "nobreak_linenumber": end,
        "dialect": params["dialect"],
    }
    return _(
        """
    AVANTPY EXCEPTION: TryNobreakError

    Error found in file '{filename}' on line {nobreak_linenumber}.

    Dialect used: {dialect}

{partial_source}

    The AvantPy {nobreak_kwd} keyword cannot be used in
    a TRY/EXCEPT/ELSE/FINALLY clause (Python: try/except/else/finally).

"""
    ).format(**info)


def handle_UnknownDialectError(exc, *args):
    """Handles error raised when an unknown dialect is requested
    """
    dialect = exc.args[0]
    all_dialects = exc.args[1]

    info = {"dialect": dialect, "all_dialects": all_dialects}
    return _(
        """
    AVANTPY EXCEPTION: UnknownDialectError

    The following unknown dialect was requested: {dialect}.

    The known dialects are: {all_dialects}.

"""
    ).format(**info)


def handle_UnknownLanguageError(exc, *args):
    """Handles error raised when an unknown language is requested
    """
    lang = exc.args[0]
    all_langs = exc.args[1]

    info = {"lang": lang, "all_langs": all_langs}

    return _(
        """
    AVANTPY EXCEPTION: UnknownLanguageError

    The following unknown language was requested: {lang}.

    The known languages are: {all_langs}.

"""
    ).format(**info)


dispatch = {
    "IfNobreakError": handle_IfNobreakError,
    "NameError": handle_NameError,
    "MismatchedBracketsError": handle_MismatchedBracketsError,
    "MissingLeftBracketError": handle_MissingLeftBracketError,
    "MissingRepeatError": handle_MissingRepeatError,
    "NobreakFirstError": handle_NobreakFirstError,
    "NobreakSyntaxError": handle_NobreakSyntaxError,
    "RepeatFirstError": handle_RepeatFirstError,
    "TryNobreakError": handle_TryNobreakError,
    "UnknownLanguageError": handle_UnknownLanguageError,
    "UnknownDialectError": handle_UnknownDialectError,
}
