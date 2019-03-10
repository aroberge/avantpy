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
    if exc.__class__.__name__ == 'IfnobreakError':
        return 'IfnobreakError'
    print("An exception was raised:")
    print("name: ", exc.__class__.__name__)
    print("args: ", exc.args)
    if DEBUG:
        print("\nInfo from sys")
        print("sys.exc_info(): ", sys.exc_info())
        _maybe_print("sys.last_type: ", sys, "last_type")
        _maybe_print("sys.last_value: ", sys, "last_value")
        _maybe_print("sys.last_traceback: ", sys, "last_traceback")

