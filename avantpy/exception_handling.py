"""Exception handling

Just a stub for now.

"""
import sys

from . import translate

ENABLED = True


def disable():
    """Disables custom exception handling"""
    global ENABLED
    ENABLED = False


def _maybe_print(msg, obj, attribute):
    try:
        print(msg, getattr(object, attribute))
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
            "An exception was raised for which we have no simplified traceback:\n"
        )
        write_err("name: %s\n" % exc.__class__.__name__)
        write_err("args: " + str(exc.args) + "\n")


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
        return None


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
    return translate.get("IfNobreakError").format(**info)


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
    return translate.get("TryNobreakError").format(**info)


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
    return translate.get("NobreakSyntaxError").format(**info)


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
    return translate.get("NobreakFirstError").format(**info)


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
    return translate.get("RepeatFirstError").format(**info)


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
    return translate.get("MissingRepeatError").format(**info)


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
        "open_linenumber": begin,
        "close_linenumber": end,
        "partial_source": partial_source,
        "dialect": params["dialect"],
    }
    return translate.get("MismatchedBracketsError").format(**info)


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
    return translate.get("MissingLeftBracketError").format(**info)


def handle_UnknownLanguageError(exc, *args):
    """Handles error raised when an unknown language is requested
    """
    lang = exc.args[0]
    all_langs = exc.args[1]

    info = {"lang": lang, "all_langs": all_langs}
    return translate.get("UnknownLanguageError").format(**info)


def handle_UnknownDialectError(exc, *args):
    """Handles error raised when an unknown dialect is requested
    """
    dialect = exc.args[0]
    all_dialects = exc.args[1]

    info = {"dialect": dialect, "all_dialects": all_dialects}
    return translate.get("UnknownDialectError").format(**info)


dispatch = {
    "IfNobreakError": handle_IfNobreakError,
    "TryNobreakError": handle_TryNobreakError,
    "NobreakFirstError": handle_NobreakFirstError,
    "NobreakSyntaxError": handle_NobreakSyntaxError,
    "RepeatFirstError": handle_RepeatFirstError,
    "MissingRepeatError": handle_MissingRepeatError,
    "MismatchedBracketsError": handle_MismatchedBracketsError,
    "MissingLeftBracketError": handle_MissingLeftBracketError,
    "UnknownLanguageError": handle_UnknownLanguageError,
    "UnknownDialectError": handle_UnknownDialectError,
}
