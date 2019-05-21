"""Console adapted from Python's console found in code.py.

An earlier version of this code was subclassing code.InteractiveConsole.
However, as more and more changes were introduced, dealing with
code transformation and especially customized error handling,
it seemed to make sense to "rewrite" every relevant part in
this single module.
"""
import os
import platform

import friendly_traceback

from . import version
from .converter import convert
from .session import state
from .my_gettext import gettext_lang


class AvantPyInteractiveConsole(friendly_traceback.FriendlyConsole):
    """A Python console that tries to emulate the normal Python interpreter
       except that it support experimental code transformations.
       It is adapted from cPython's ``code.InteractiveConsole`` and its
       parent.

       Like the normal Python interactive console, it attempts to evaluate
       code entered one line at a time by a user.
    """

    def __init__(self, locals=None):
        self.locals = locals if locals is not None else {}
        super().__init__(locals=locals)
        self.name = "<AvantPy console>"
        self.resetbuffer()
        state.console_active = True

    def push(self, line):
        """Pushes a transformed line to the interpreter.

        The line should not have a trailing newline; it may have
        internal newlines.  The line is transformed and appended to a buffer.
        The interpreter's run_source() method is called with the
        concatenated contents of the buffer as source.  If this
        indicates that the command was executed or invalid, the buffer
        is reset; otherwise, the command is incomplete, and the buffer
        is left as it was after the line was appended.  The return
        value is True if more input is required, False if the line was dealt
        with in some way (this is the same as run_source()).
        """
        assert not line.endswith("\n"), "Forbidden trailing newline in push()."
        _ = gettext_lang.lang

        self.buffer.append(line)
        self.source = "\n".join(self.buffer)

        self.counter += 1
        self.name = "<avantpy-console:%d>" % self.counter
        friendly_traceback.cache.add(self.name, self.source)
        try:
            self.converted = convert(self.source, filename=self.name)
        except SystemExit:
            os._exit(1)
        except Exception:
            friendly_traceback.explain()
            self.resetbuffer()
            return False

        try:
            more = self.runsource(self.converted, filename=self.name)
        except SystemExit:
            os._exit(1)
        except Exception:
            friendly_traceback.explain()
            self.resetbuffer()
            return False

        if not more:
            self.resetbuffer()
        return more

    def runsource(self, source, filename="<input>", symbol="single"):
        """Compile and run some source in the interpreter.

        Arguments are as for compile_command().

        One several things can happen:

        1) The input is incorrect; compile_command() raised an
        exception (SyntaxError or OverflowError).  A syntax traceback
        will be printed by calling the showsyntaxerror() method.

        2) The input is incomplete, and more input is required;
        compile_command() returned None.  Nothing happens.

        3) The input is complete; compile_command() returned a code
        object.  The code is executed by calling self.runcode() (which
        also handles run-time exceptions, except for SystemExit).

        The return value is True in case 2, False in the other cases (unless
        an exception is raised).  The return value can be used to
        decide whether to use sys.ps1 or sys.ps2 to prompt the next
        line.

        """
        try:
            code = self.compile(source, filename, symbol)
        except (OverflowError, SyntaxError, ValueError):
            # Case 1
            friendly_traceback.explain()
            return False

        if code is None:
            # Case 2
            return True

        # Case 3
        self.runcode(code)
        return False


def start_console(local_vars=None):
    """Starts a console; modified from code.interact"""
    console_defaults = {"set_lang": state.set_lang, "set_dialect": state.set_dialect}

    if local_vars is None:
        local_vars = console_defaults
    else:
        local_vars.update(console_defaults)

    console = AvantPyInteractiveConsole(locals=local_vars)

    banner = "AvantPy version {} [Python: {}; Friendly-traceback: {}]\n".format(
        version.__version__,
        platform.python_version(),
        friendly_traceback.version.__version__,
    )
    console.interact(banner=banner)
