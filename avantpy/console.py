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
import traceback

from codeop import CommandCompiler
from tokenize import TokenError

from . import session
from . import converter
from . import version
from . import exception_handling
from . import exceptions


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
        self.filename = "<AvantPy console>"
        self.resetbuffer()

    def do_transformations(self, source):
        """Performs the source transformations on the current content.

           Returns the transformed source.
        """
        source = converter.convert(source, source_name="REPL")
        source = self.fix_ending(source)

        self._source = source  # saved in case we need it if we want to show
        # a syntax error. See showsyntaxerror() above
        return source

    def fix_ending(self, source):
        """Ensures that the last blank lines of the transformed source are
        consistent with what was provided by the user."""

        # Some transformations may add or strip an empty line meant to
        # end a block, or strip non-empty lines (but with spaces) at the end
        # mean to continue a block, etc.
        # We ensure that the transformed source has the same combination
        # of white spaces and \n characters at the end as the original

        last_lines = reversed(self.buffer)
        blank_lines = []
        for line in last_lines:
            if not line.strip():
                blank_lines.append(line)
            else:
                break
        blank_lines = reversed(blank_lines)

        source = source.rstrip()
        if source:
            lines = source.split("\n")
        else:
            lines = []
        lines.extend(blank_lines)
        source = "\n".join(lines)
        return source

    def interact(self, banner=None):
        """Emulates the interactive Python console.
        """
        self.write("%s\n" % str(banner))
        more = False
        while True:
            try:
                if more:
                    prompt = session.state.prompt2
                else:
                    prompt = session.state.prompt1
                try:
                    line = input(prompt)
                except EOFError:
                    self.write("\n")
                    break
                else:
                    more = self.push(line)
            except KeyboardInterrupt:
                self.write("\nKeyboardInterrupt\n")
                self.resetbuffer()
                more = False

    def push(self, line):
        """Pushes a transformed line to the interpreter.

        The line should not have a trailing newline; it may have
        internal newlines.  The line is transformed and appended to a buffer.
        The interpreter's runsource() method is called with the
        concatenated contents of the buffer as source.  If this
        indicates that the command was executed or invalid, the buffer
        is reset; otherwise, the command is incomplete, and the buffer
        is left as it was after the line was appended.  The return
        value is True if more input is required, False if the line was dealt
        with in some way (this is the same as runsource()).
        """
        assert not line.endswith(
            "\n"
        ), "Forbidden trailing newline in console's push method."
        self.buffer.append(line)
        source = "\n".join(self.buffer)
        self.identical = True
        try:
            newsource = self.do_transformations(source)
        except SystemExit:
            os._exit(1)
        except exceptions.AvantPyException as exc:
            print(exception_handling.handle_exception(exc, source))
            self.resetbuffer()
            return False
        except TokenError as exc:
            exc.args[0].startswith("EOF")
            return True
        except Exception as exc:
            print("UNHANDLED EXCEPTION in console.py. This should not happen.")
            raise exc

        if newsource != source:
            self.identical = False

        try:
            more = self.runsource(newsource)
        except SystemExit:
            os._exit(1)
        except Exception as exc:
            print(exception_handling.handle_exception(exc, source))
            self.resetbuffer()
            return False

        if not more:
            self.resetbuffer()
            if self.show_python and not self.identical:
                self.show_converted(newsource)
        return more

    def resetbuffer(self):
        """Reset the input buffer."""
        self.buffer = []

    def runsource(self, source, symbol="single"):
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
        decide which prompt to use next line.
        """

        try:
            code = self.compile(source, self.filename, symbol)
        except (OverflowError, SyntaxError, ValueError):
            # Case 1
            self.showsyntaxerror(self.filename)
            return False

        if code is None:
            # Case 2
            return True

        # Case 3
        self.runcode(code)
        return False

    def runcode(self, code):
        """Execute a code object.

        When an exception occurs, self.showtraceback() is called to
        display a traceback.  All exceptions are caught except
        SystemExit, which is reraised.

        A note about KeyboardInterrupt: this exception may occur
        elsewhere in this code, and may not always be caught.  The
        caller should be prepared to deal with it.

        """
        try:
            exec(code, self.locals)
        except SystemExit:
            raise
        except Exception:
            self.showtraceback()

    def show_converted(self, source):
        """Prints the converted source"""
        print()
        for line in source.split("\n"):
            print("|", line)
        print()
        self.identical = True  # prevent from showing again

    def showsyntaxerror(self, filename=None):
        """Shows the converted source if different than the original
           and the syntax error"""
        if self.show_python and not self.identical:
            self.show_converted(self._source)
        self.showsyntaxerror_(filename=filename)

    def showsyntaxerror_(self, filename=None):
        """Display the syntax error that just occurred.

        This doesn't display a stack trace because there isn't one.

        If a filename is given, it is stuffed in the exception instead
        of what was there before (because Python's parser always uses
        "<string>" when reading from a string).

        The output is written by self.write(), below.

        """
        type, value, tb = sys.exc_info()
        sys.last_type = type
        sys.last_value = value
        sys.last_traceback = tb
        if filename and type is SyntaxError:
            # Work hard to stuff the correct filename in the exception
            try:
                msg, (dummy_filename, lineno, offset, line) = value.args
            except ValueError:
                # Not the format we expect; leave it alone
                pass
            else:
                # Stuff in the right filename
                value = SyntaxError(msg, (filename, lineno, offset, line))
                sys.last_value = value
        if sys.excepthook is sys.__excepthook__:
            lines = traceback.format_exception_only(type, value)
            self.write("".join(lines))
        else:
            # If someone has set sys.excepthook, we let that take precedence
            # over self.write
            sys.excepthook(type, value, tb)

    def showtraceback(self):
        """Display the exception that just occurred.

        We remove the first stack item because it is our own code.

        The output is written by self.write(), below.

        """
        sys.last_type, sys.last_value, last_tb = ei = sys.exc_info()
        sys.last_traceback = last_tb
        try:
            lines = traceback.format_exception(ei[0], ei[1], last_tb.tb_next)
            if sys.excepthook is sys.__excepthook__:
                self.write("".join(lines))
            else:
                # If someone has set sys.excepthook, we let that take precedence
                # over self.write
                sys.excepthook(ei[0], ei[1], last_tb)
        finally:
            last_tb = ei = None

    def write(self, data):
        """Write a string.

        The base implementation writes to sys.stderr; a subclass may
        replace this with a different implementation.

        """
        sys.stderr.write(data)


def start_console(local_vars=None, show_python=False):
    """Starts a console; modified from code.interact"""
    console_defaults = {
        "set_lang": session.state.set_lang,
        "set_dialect": session.state.set_dialect,
    }

    if local_vars is None:
        local_vars = console_defaults
    else:
        local_vars.update(console_defaults)

    console = AvantPyInteractiveConsole(locals=local_vars, show_python=show_python)

    banner = "AvantPy version {}. [Python version: {}]\n".format(
        version.__version__, platform.python_version()
    )
    console.interact(banner=banner)
