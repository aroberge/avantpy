"""Console adapted from Python's console found in code.py.

An earlier version of this code was subclassing code.InteractiveConsole.
However, as more and more changes were introduced, dealing with
code transformation and especially customized error handling,
it seemed to make sense to "rewrite" every relevant part in
this single module.
"""
import os
import platform
import sys

from codeop import CommandCompiler
from tokenize import TokenError

from . import version
from .converter import convert
from .session import state
from .exception_handling import write_exception_info
from .exceptions import AvantPyException
from .my_gettext import gettext_lang


class AvantPyInteractiveConsole:
    """A Python console that tries to emulate the normal Python interpreter
       except that it support experimental code transformations.
       It is adapted from cPython's ``code.InteractiveConsole`` and its
       parent.

       Like the normal Python interactive console, it attempts to evaluate
       code entered one line at a time by a user.
    """

    def __init__(self, locals=None, show_python=False):
        self.show_python = show_python
        self.locals = locals if locals is not None else {}
        self.compile = CommandCompiler()
        self.name = "<AvantPy console>"
        self.reset_buffer()
        state.console_active = True

    def interact(self, banner=None):
        """Emulates the interactive Python console.
        """
        self.write("%s\n" % str(banner))
        more = False
        while True:
            try:
                if more:
                    prompt = state.prompt2
                else:
                    prompt = state.prompt1
                try:
                    line = input(prompt)
                except EOFError:
                    self.write("\n")
                    break
                else:
                    more = self.push(line)
            except KeyboardInterrupt:
                self.write("\nKeyboardInterrupt\n")
                self.reset_buffer()
                more = False

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

        try:
            self.converted = convert(self.source, filename=self.name)
            self.identical = self.converted == self.source
        except SystemExit:
            os._exit(1)
        except AvantPyException as exc:
            write_exception_info(exc, self.source)
            self.reset_buffer()
            return False
        except TokenError as exc:
            exc.args[0].startswith("EOF")
            return True
        except Exception as exc:
            print(_("UNHANDLED EXCEPTION in console.py. This should not happen."))
            raise exc

        try:
            more = self.run_source(self.converted)
        except SystemExit:
            os._exit(1)
        except Exception as exc:
            write_exception_info(exc, self.source)
            self.reset_buffer()
            return False

        if not more:
            self.reset_buffer()
            if self.show_python and not self.identical:
                self.show_converted()
        return more

    def reset_buffer(self):
        """Reset the input buffer."""
        self.buffer = []

    def run_source(self, source, symbol="single"):
        """Compile and run some source in the interpreter.

        Arguments are as for compile_command().

        One several things can happen:

        1) The input is incorrect; compile_command() raised an
        exception (SyntaxError or OverflowError).

        2) The input is incomplete, and more input is required;
        compile_command() returned None.  Nothing happens.

        3) The input is complete; compile_command() returned a code
        object.  The code is executed by calling self.runcode() (which
        also handles run-time exceptions, except for SystemExit).

        The return value is True in case 2, False in the other cases (unless
        an exception is raised).  The return value can be used to
        decide which prompt to use next line.
        """

        try:
            code = self.compile(source, self.name, symbol)
        except (OverflowError, SyntaxError, ValueError) as exc:
            # Case 1
            if self.show_python and not self.identical:
                self.show_converted(self.converted)
            write_exception_info(exc, source)
            return False

        if code is None:  # Case 2
            return True

        # Case 3
        self.runcode(code)
        return False

    def runcode(self, code):
        """Execute a code object.

        All exceptions are caught except SystemExit, which is reraised.

        A note about KeyboardInterrupt: this exception may occur
        elsewhere in this code, and may not always be caught.  The
        caller should be prepared to deal with it.
        """
        try:
            exec(code, self.locals)
        except SystemExit:
            raise
        except Exception as exc:
            write_exception_info(exc, self.source)

    def show_converted(self):
        """Prints the converted source"""
        print()
        for line in self.converted.split("\n"):
            print("|", line)
        print()
        self.identical = True  # prevent from showing again

    def write(self, data):
        """Write a string.

        The base implementation writes to sys.stderr; a subclass may
        replace this with a different implementation.

        """
        sys.stderr.write(data)


def start_console(local_vars=None, show_python=False):
    """Starts a console; modified from code.interact"""
    console_defaults = {"set_lang": state.set_lang, "set_dialect": state.set_dialect}

    if local_vars is None:
        local_vars = console_defaults
    else:
        local_vars.update(console_defaults)

    console = AvantPyInteractiveConsole(locals=local_vars, show_python=show_python)

    banner = "AvantPy version {}. [Python version: {}]\n".format(
        version.__version__, platform.python_version()
    )
    console.interact(banner=banner)
