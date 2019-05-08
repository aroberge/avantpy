"""The goal of exception_handling.py is to display information about
exceptions being raised in a way that is much easier to understand
for beginners than normal Python tracebacks.  These "friendly" tracebacks
are written so that they can easily be translated into any human language.
"""
import sys
import traceback

from .session import state
from .my_gettext import gettext_lang

ENABLED = True

# Many strings are common to the information provided by  exceptions handlers below.
# To avoid code duplication, we define them here.
# Furthermore, note that two versions are provided: one where we assume that
# the code is standard Python, and that no dialect-based keywords are used,
# and a second version specific to dialects.


def avantpy_exception_message():
    _ = gettext_lang.lang
    return _(
        "    AvantPy exception: {exception_name}\n\n"
        "    Error found in file '{filename}' on line {linenumber}.\n\n"
        "{partial_source}\n\n"
    )


def python_exception_message():
    _ = gettext_lang.lang
    return _(
        "    Python exception: \n"
        "        {python_display}\n\n"
        "    Error found in file '{filename}' on line {linenumber}.\n\n"
        "{partial_source}\n\n"
    )


def disable():
    """Disables custom exception handling"""
    global ENABLED
    ENABLED = False


def get_partial_source(source, begin, end, marks=None, nb_digits=None):
    """Extracts a few relevant lines from a source file.

       If the number of lines would exceed a certain limit (currently 7)
       the function is called recursively to only show the a few lines
       at the beginning and at the end.
    """
    if nb_digits is None:
        nb_digits = len(str(end))
    no_mark = "       {:%d}: " % nb_digits
    with_mark = "    -->{:%d}: " % nb_digits
    continuation = "           ..."

    if marks is None:
        marks = []

    result = []
    if end - begin > 7:
        # Suppose the source spans line numbers 1 to 12. Splitting it to show
        # partial result would show lines 1 to 3, followed by 10 to 12.
        # If we want the indentation of the first part to match the indentation
        # of the second part, we must specify the length of the
        # indentation of the first part.
        # See the traceback for MismatchedBracketsError in the
        # documentation for an example.
        result.append(
            get_partial_source(
                source, begin, begin + 2, marks=marks, nb_digits=nb_digits
            )
        )
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


def extract_filename_linenumber(exc):
    """Extracting filename and linenumber where an error occurred based
       on information from traceback."""

    last_tb_line = traceback.format_tb(exc.__traceback__)[-1]

    # For last_tb_line, we expect something like
    # File "filename", line 1, in <module>
    splitted_line = last_tb_line.split(",")
    filename = splitted_line[0].replace("File ", "").replace('"', "").strip()
    if filename in ["<string>", "<tokenize>"] and state.current_filename is not None:
        filename = state.current_filename
    linenumber = int(splitted_line[1].replace("line ", ""))
    return filename, linenumber


def write_err(msg):
    """Writes a string to sys.stderr."""
    sys.stderr.write(msg)


def write_exception_info(exc, source):
    """Writes the information we have after processing the exception."""
    _ = gettext_lang.lang
    msg = handle_exception(exc, source)
    if msg is not None:
        write_err(msg)
    else:
        write_err(
            _("An exception was raised for which we have no simplified traceback:\n")
        )
        write_err("name: %s\n" % exc.__class__.__name__)
        write_err("args: " + str(exc.args) + "\n\n")
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
    _ = gettext_lang.lang
    params = exc.args[0]
    begin = params["if_linenumber"]
    end = params["linenumber"]
    marks = [end]
    partial_source = get_partial_source(source, begin, end, marks=marks)
    dialect = params["dialect"]

    message = avantpy_exception_message() + _(
        "    The AvantPy '{nobreak_kwd}' keyword cannot be used in\n"
        "    an '{if_kwd}/{elif_kwd}/{else_kwd}' clause (Python: if/elif/else).\n\n"
    )

    return message.format(
        exception_name=exc.__class__.__name__,
        filename=params["filename"],
        nobreak_kwd=params["nobreak keyword"],
        partial_source=partial_source,
        linenumber=end,
        dialect=dialect,
        if_kwd=params["if_kwd"],
        elif_kwd=params["elif_kwd"],
        else_kwd=params["else_kwd"],
    )


def handle_IndentationError(exc, source):
    """Handles IndentationError.
    """
    _ = gettext_lang.lang
    msg = exc.args[0]
    if "unexpected indent" in msg:
        this_case = _(
            "    In this case, the line indicated by an arrow\n"
            "    is more indented than expected and does not match\n"
            "    the indentation of the previous line.\n"
        )
    elif "expected an indented block" in msg:
        this_case = _(
            "    In this case, the line indicated by an arrow\n"
            "    was expected to begin a new indented block.\n"
        )
    else:
        this_case = _(
            "    In this case, the line indicated by an arrow\n"
            "    is less indented the preceding one,\n"
            "    and is not aligned vertically with another block of code.\n"
        )

    exc_name = exc.__class__.__name__
    python_display = "{exc_name}: {msg}".format(exc_name=exc_name, msg=msg)
    filename, linenumber, _ignore, _ignore = exc.args[1]

    if filename in ["<string>", "<tokenize>"] and state.current_filename is not None:
        filename = state.current_filename

    begin = linenumber - 4
    end = linenumber + 1
    marks = [linenumber]
    partial_source = get_partial_source(source, begin, end, marks=marks)

    dialect = state.current_dialect

    message_end = _(
        "    An indentation error occurs when a given line is\n"
        "    not indented (aligned vertically) as expected.\n"
        "{this_case}\n"
    )

    message = python_exception_message() + message_end

    return message.format(
        exception_name=exc_name,
        filename=filename,
        python_display=python_display,
        partial_source=partial_source,
        dialect=dialect,
        linenumber=linenumber,
        this_case=this_case,
    )


def handle_MismatchedBracketsError(exc, source):
    """Handles situation where a bracket of one kind '([{'
       is closed with a bracket of a different kind.
    """
    _ = gettext_lang.lang
    params = exc.args[0]
    begin = params["open_linenumber"]
    end = params["linenumber"]
    marks = [begin, end]
    partial_source = get_partial_source(source, begin, end, marks=marks)

    dialect = params["dialect"]

    message_end = _(
        "    The opening {open_bracket} does not match the closing {close_bracket}.\n\n"
    )

    message = avantpy_exception_message() + message_end

    return message.format(
        exception_name=exc.__class__.__name__,
        filename=params["filename"],
        linenumber=end,
        open_bracket=params["open_bracket"],
        close_bracket=params["close_bracket"],
        partial_source=partial_source,
        dialect=dialect,
    )


def handle_MissingLeftBracketError(exc, source):
    """Handles situation where at bracket of one kind ),],}
       is closed without a corresponding open bracket.
    """
    _ = gettext_lang.lang
    params = exc.args[0]
    linenumber = params["linenumber"]
    begin = linenumber - 1
    end = linenumber + 1
    marks = [linenumber]
    partial_source = get_partial_source(source, begin, end, marks=marks)

    dialect = params["dialect"]

    message_end = _("    The closing {bracket} does not match anything.\n\n")

    message = avantpy_exception_message() + message_end

    return message.format(
        exception_name=exc.__class__.__name__,
        filename=params["filename"],
        partial_source=partial_source,
        dialect=dialect,
        linenumber=linenumber,
        bracket=params["bracket"],
    )


def handle_MissingRepeatColonError(exc, source):
    """Handles situation where a statement beginning with repeat
       does not end with a colon.
    """
    _ = gettext_lang.lang
    params = exc.args[0]
    linenumber = params["linenumber"]
    begin = linenumber - 1
    end = linenumber + 1
    marks = [linenumber]
    partial_source = get_partial_source(source, begin, end, marks=marks)

    message_end = _(
        "    A statement beginning with the '{repeat_kwd}' keyword must be on\n"
        "    a single line ending with a colon (:) that indicates the beginning of\n"
        "    an indented block of code, with no other colon appearing on that line.\n\n"
    )
    message = avantpy_exception_message() + message_end

    return message.format(
        exception_name=exc.__class__.__name__,
        filename=params["filename"],
        repeat_kwd=params["repeat_kwd"],
        partial_source=partial_source,
        linenumber=linenumber,
        dialect=params["dialect"],
    )


def handle_MissingRepeatError(exc, source):
    """Handles situation where either ``until`` or ``forever`` was
       used without being preceeded by ``repeat``.
    """
    _ = gettext_lang.lang
    params = exc.args[0]
    linenumber = params["linenumber"]
    begin = linenumber - 1
    end = linenumber + 1
    marks = [linenumber]
    partial_source = get_partial_source(source, begin, end, marks=marks)

    message_end = _(
        "    The AvantPy '{keyword}'' keyword can be used only when"
        " preceded by '{repeat_kwd}'.\n\n"
    )

    message = avantpy_exception_message() + message_end
    return message.format(
        exception_name=exc.__class__.__name__,
        filename=params["filename"],
        keyword=params["keyword"],
        partial_source=partial_source,
        linenumber=linenumber,
        dialect=params["dialect"],
        repeat_kwd=params["repeat_kwd"],
    )


def handle_NameError(exc, source):
    """Handles situation where a NameError is raise."""
    _ = gettext_lang.lang
    msg = exc.args[0]
    var_name = msg.split("'")[1]
    exc_name = exc.__class__.__name__
    python_display = "{exc_name}: {msg}".format(exc_name=exc_name, msg=msg)

    filename, linenumber = extract_filename_linenumber(exc)

    begin = linenumber - 1
    end = linenumber + 1
    marks = [linenumber]
    partial_source = get_partial_source(source, begin, end, marks=marks)

    message_end = _(
        "    A NameError exception indicates that a variable or\n"
        "    function name is not known to Python.\n"
        "    Most often, this is because there is a spelling mistake; however,\n"
        "    sometimes it is because it is used before being defined\n"
        "    or given a value. In your program, the unknown name is '{var_name}'.\n\n"
    )
    message = python_exception_message() + message_end

    return message.format(
        exception_name=exc.__class__.__name__,
        filename=filename,
        python_display=python_display,
        var_name=var_name,
        partial_source=partial_source,
        linenumber=linenumber,
        dialect=state.current_dialect,
    )


def handle_NobreakFirstError(exc, source):
    """Handles situation where ``nobreak`` was wrongly use as a
       replacement for ``else`` in statements like
       var = x if condition else y.
    """
    _ = gettext_lang.lang
    params = exc.args[0]
    linenumber = params["linenumber"]
    begin = linenumber - 1
    end = linenumber + 1
    marks = [linenumber]
    partial_source = get_partial_source(source, begin, end, marks=marks)

    message_end = _(
        "    The AvantPy '{nobreak_kwd}' keyword can be used instead of '{else_kwd}'\n"
        "    (Python: else) only when it begins a new statement in\n"
        "    '{for_kwd}/{while_kwd}' loops (Python: for/while).\n\n"
    )
    message = avantpy_exception_message() + message_end

    return message.format(
        exception_name=exc.__class__.__name__,
        filename=params["filename"],
        nobreak_kwd=params["nobreak keyword"],
        partial_source=partial_source,
        linenumber=linenumber,
        for_kwd=params["for_kwd"],
        while_kwd=params["while_kwd"],
        else_kwd=params["else_kwd"],
    )


def handle_NobreakSyntaxError(exc, source):
    """Handles situation where ``nobreak`` is used without a matching
       ``for`` or ``while`` loop and not already raised.
    """
    _ = gettext_lang.lang
    params = exc.args[0]
    linenumber = params["linenumber"]
    begin = linenumber - 1
    end = linenumber + 1
    marks = [linenumber]
    partial_source = get_partial_source(source, begin, end, marks=marks)

    message_end = _(
        "    The AvantPy '{nobreak_kwd}' keyword can only be used as a replacement\n"
        "    of '{else_kwd}' (Python: else) with a matching '{for_kwd}' or\n"
        "    '{while_kwd}' loop (Python: for/while).\n\n"
    )
    message = avantpy_exception_message() + message_end

    return message.format(
        exception_name=exc.__class__.__name__,
        filename=params["filename"],
        nobreak_kwd=params["nobreak keyword"],
        partial_source=partial_source,
        linenumber=linenumber,
        for_kwd=params["for_kwd"],
        while_kwd=params["while_kwd"],
        else_kwd=params["else_kwd"],
    )


def handle_RepeatFirstError(exc, source):
    """Handles situation where ``repeat`` was uses wrongly as
       it did not appear as the first keyword of a given statement.
    """
    _ = gettext_lang.lang
    params = exc.args[0]
    linenumber = params["linenumber"]
    begin = linenumber - 1
    end = linenumber + 1
    marks = [linenumber]
    partial_source = get_partial_source(source, begin, end, marks=marks)

    message_end = _(
        "    The AvantPy '{repeat_kwd}' keyword can only be used to begin\n"
        "    a new loop (Python: equivalent to 'for' or 'while' loop).\n\n"
    )
    message = avantpy_exception_message() + message_end

    return message.format(
        exception_name=exc.__class__.__name__,
        filename=params["filename"],
        repeat_kwd=params["repeat keyword"],
        partial_source=partial_source,
        linenumber=linenumber,
    )


def handle_TabError(exc, source):
    """Handles TabError.
    """
    _ = gettext_lang.lang
    msg = exc.args[0]

    exc_name = exc.__class__.__name__
    python_display = "{exc_name}: {msg}".format(exc_name=exc_name, msg=msg)
    filename, linenumber, _ignore, _ignore = exc.args[1]

    if filename in ["<string>", "<tokenize>"] and state.current_filename is not None:
        filename = state.current_filename

    begin = linenumber - 4
    end = linenumber + 1
    marks = [linenumber]
    partial_source = get_partial_source(source, begin, end, marks=marks)

    message_end = _(
        "    A TabError indicates that you have used both spaces\n"
        "    and tab characters to indent your code.\n"
        "    This is not allowed in Python.\n"
        "    Python's recommendation is to always use spaces to indent your code.\n\n"
    )

    message = python_exception_message() + message_end

    return message.format(
        exception_name=exc_name,
        filename=filename,
        python_display=python_display,
        partial_source=partial_source,
        linenumber=linenumber,
    )


def handle_TryNobreakError(exc, source):
    """Handles situation where ``nobreak`` was wrongly use as a
       replacement for ``else`` in an try/except/else/finally block.
    """
    _ = gettext_lang.lang
    params = exc.args[0]
    begin = params["try_linenumber"]
    end = params["linenumber"]
    marks = [end]
    partial_source = get_partial_source(source, begin, end, marks=marks)

    message_end = _(
        "    The AvantPy '{nobreak_kwd}' keyword cannot be used in\n"
        "    a '{try_kwd}/{except_kwd}/{else_kwd}/{finally_kwd}' clause\n"
        "    (Python: try/except/else/finally).\n\n"
    )
    message = avantpy_exception_message() + message_end

    return message.format(
        exception_name=exc.__class__.__name__,
        filename=params["filename"],
        nobreak_kwd=params["nobreak keyword"],
        partial_source=partial_source,
        linenumber=end,
        try_kwd=params["try_kwd"],
        except_kwd=params["except_kwd"],
        else_kwd=params["else_kwd"],
        finally_kwd=params["finally_kwd"],
    )


def handle_UnknownDialectError(exc, *args):
    """Handles error raised when an unknown dialect is requested
    """
    _ = gettext_lang.lang
    dialect = exc.args[0]
    all_dialects = exc.args[1]

    message = _(
        "    AvantPy exception: UnknownDialectError\n\n"
        "    The following unknown dialect was requested: {dialect}.\n\n"
        "    The known dialects are: {all_dialects}.\n\n"
    )
    return message.format(
        exception_name=exc.__class__.__name__,
        dialect=dialect,
        all_dialects=all_dialects,
    )


def handle_UnknownLanguageError(exc, *args):
    """Handles error raised when an unknown language is requested
    """
    _ = gettext_lang.lang
    lang = exc.args[0]
    all_langs = exc.args[1]

    message = _(
        "    AvantPy exception: UnknownLanguageError\n\n"
        "    The following unknown language was requested: {lang}.\n\n"
        "    The known languages are: {all_langs}.\n\n"
    )

    return message.format(
        exception_name=exc.__class__.__name__, lang=lang, all_langs=all_langs
    )


dispatch = {
    "IfNobreakError": handle_IfNobreakError,
    "IndentationError": handle_IndentationError,
    "NameError": handle_NameError,
    "MismatchedBracketsError": handle_MismatchedBracketsError,
    "MissingLeftBracketError": handle_MissingLeftBracketError,
    "MissingRepeatColonError": handle_MissingRepeatColonError,
    "MissingRepeatError": handle_MissingRepeatError,
    "NobreakFirstError": handle_NobreakFirstError,
    "NobreakSyntaxError": handle_NobreakSyntaxError,
    "RepeatFirstError": handle_RepeatFirstError,
    "TabError": handle_TabError,
    "TryNobreakError": handle_TryNobreakError,
    "UnknownLanguageError": handle_UnknownLanguageError,
    "UnknownDialectError": handle_UnknownDialectError,
}
