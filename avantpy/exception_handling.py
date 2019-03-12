"""Exception handling

Just a stub for now.

"""
import sys

from . import translate
from . import exceptions

DEBUG = False

ENABLED = True
def disable():
    '''Disables custom exception handling'''
    global ENABLED
    ENABLED = False

def _maybe_print(msg, obj, attribute):
    try:
        print(msg, getattr(object, attribute))
    except AttributeError:
        print(msg, "does not exist")



def handle_exception(exc, original_source):
    if not ENABLED:
        # Let normal Python traceback through
        raise exc

    if DEBUG:
        print("\nInfo from sys")
        print("sys.exc_info(): ", sys.exc_info())
        _maybe_print("sys.last_type: ", sys, "last_type")
        _maybe_print("sys.last_value: ", sys, "last_value")
        _maybe_print("sys.last_traceback: ", sys, "last_traceback")

    name = exc.__class__.__name__
    if name in dispatch:
        return dispatch[name](exc, original_source)
        

    print("An exception was raised:")
    print("name: ", exc.__class__.__name__)
    print("args: ", exc.args)


def handle_IfnobreakError(exc, original_source):
    params = exc.args[0]

    if_linenumber = int(params["if_string"][1])
    nobreak_linenumber = int(params["linenumber"])
    lang = params["lang"]

    lines = original_source.split("\n")
    if_line = lines[if_linenumber - 1]
    nobreak_line = lines[nobreak_linenumber - 1]

    info = {'filename': params["source_name"],
        "nobreak_kwd": params["nobreak keyword"],
        "if_linenumber": if_linenumber,
        "if_line": if_line,
        "nobreak_linenumber": nobreak_linenumber,
        "nobreak_line": nobreak_line
    }
    return translate.get('IfnobreakError', lang).format(**info)


def handle_TrynobreakError(exc, original_source):
    params = exc.args[0]

    try_linenumber = int(params["try_string"][1])
    nobreak_linenumber = int(params["linenumber"])
    lang = params["lang"]

    lines = original_source.split("\n")
    try_line = lines[try_linenumber - 1]
    nobreak_line = lines[nobreak_linenumber - 1]

    info = {'filename': params["source_name"],
        "nobreak_kwd": params["nobreak keyword"],
        "try_linenumber": try_linenumber,
        "try_line": try_line,
        "nobreak_linenumber": nobreak_linenumber,
        "nobreak_line": nobreak_line
    }
    return translate.get('TrynobreakError', lang).format(**info)


def handle_NobreakSyntaxError(exc, original_source):
    params = exc.args[0]

    nobreak_linenumber = int(params["linenumber"])
    lang = params["lang"]

    lines = original_source.split("\n")
    nobreak_line = lines[nobreak_linenumber - 1]

    info = {'filename': params["source_name"],
        "nobreak_kwd": params["nobreak keyword"],
        "linenumber": nobreak_linenumber,
        "nobreak_line": nobreak_line
    }
    return translate.get('NobreakSyntaxError', lang).format(**info)


def handle_NobreakMustBeFirstError(exc, original_source):
    params = exc.args[0]
    linenumber = int(params["linenumber"])
    lang = params["lang"]

    lines = original_source.split("\n")
    nobreak_line = lines[linenumber - 1]

    info = {'filename': params["source_name"],
        "nobreak_kwd": params["nobreak keyword"],
        "linenumber": linenumber,
        "nobreak_line": nobreak_line
    }
    return translate.get('NobreakMustBeFirstError', lang).format(**info)


def handle_RepeatMustBeFirstError(exc, original_source):
    params = exc.args[0]
    linenumber = int(params["linenumber"])
    lang = params["lang"]

    lines = original_source.split("\n")
    repeat_line = lines[linenumber - 1]

    info = {'filename': params["source_name"],
        "repeat_kwd": params["repeat keyword"],
        "linenumber": linenumber,
        "repeat_line": repeat_line
    }
    return translate.get('RepeatMustBeFirstError', lang).format(**info)


dispatch = {
    'IfnobreakError': handle_IfnobreakError,
    'TrynobreakError': handle_TrynobreakError,
    'NobreakMustBeFirstError': handle_NobreakMustBeFirstError,
    'NobreakSyntaxError': handle_NobreakSyntaxError,
    'RepeatMustBeFirstError': handle_RepeatMustBeFirstError,
}