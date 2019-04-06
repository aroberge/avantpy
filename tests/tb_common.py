"""Common information so that all traceback generating scripts
   create files in the same format.

   IMPORTANT: this assumes that all tests files with names of the form

       raise_something.dialect

"""
import sys
from contextlib import redirect_stderr


def write(text):
    sys.stderr.write(text + "\n")


def make_title(text):
    write("\n" + text)
    write("-" * len(text) + "\n")
    write("Example::\n")


all_imports = {
    "IfNobreakError": "raise_if_nobreak",
    "IndentationError: expected an indented block": "raise_indentation_error1",
    "IndentationError: unexpected indent": "raise_indentation_error2",
    "IndentationError - no match": "raise_indentation_error3",
    "MismatchedBracketsError": "raise_mismatched_brackets",
    "MissingLeftBracketError": "raise_missing_left_bracket",
    "MissingRepeatColonError": "raise_missing_repeat_colon",
    "MissingRepeatError": "raise_missing_repeat",
    "NameError": "raise_name_error",
    "NobreakFirstError": "raise_nobreak_first",
    "NobreakSyntaxError": "raise_nobreak_syntax",
    "RepeatFirstError": "raise_repeat_first",
    "TabError": "raise_tab_error",
    "TryNobreakError": "raise_try_nobreak",
    "UnknownDialectError": "raise_unknown_dialect",
    "UnknownLanguageError": "raise_unknown_language",
}


def create_tracebacks(target, intro_text):
    with open(target, "w", encoding="utf8") as out:
        with redirect_stderr(out):
            write(intro_text)

            for title in all_imports:
                make_title(title)
                __import__(all_imports[title])
