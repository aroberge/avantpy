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

dispatch = {
    'IfnobreakError': handle_IfnobreakError
}