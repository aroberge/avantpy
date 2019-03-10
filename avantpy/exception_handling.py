"""Exception handling

Just a stub for now.

"""
import sys


ENABLED = False
def enable():
    '''Enables custom exception handling'''
    global ENABLED
    ENABLED = True

def maybe_print(msg, obj, attribute):
    try:
        print(msg, getattr(object, attribute))
    except AttributeError:
        print(msg, "does not exist")

def handle_exception(exc):
    if not ENABLED:
        # Let normal Python traceback through
        raise exc
    print("An exception was raised:")
    print("name: ", exc.__class__.__name__)
    print("args: ", exc.args)
    print("\nInfo from sys")
    print("sys.exc_info(): ", sys.exc_info())
    maybe_print("sys.last_type: ", sys, "last_type")
    maybe_print("sys.last_value: ", sys, "last_value")
    maybe_print("sys.last_traceback: ", sys, "last_traceback")


