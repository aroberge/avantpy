import code
import os
import platform
import sys
from tokenize import TokenError

from . import session
from . import conversion
from . import version
from . import exception_handling
from . import exceptions


# define banner and prompt here so that they can be imported in tests
banner = "avantpy console version {}. [Python version: {}]\n".format(
    version.__version__, platform.python_version()
)
prompt = "->> "


class AvantPyInteractiveConsole(code.InteractiveConsole):
    """A Python console that tries to emulate the normal Python interpreter
       except that it support experimental code transformations.
       It inherits from cPython's ``code.InteractiveConsole``.

       Like the normal Python's interactive console, it attempts to evaluate
       code entered one line at a time by a user.
    """

    def __init__(self, locals=None, show_python=False):
        self.show_python = show_python
        super().__init__(locals=locals)

    def push(self, line):
        """Pushes a transformed line to the interpreter.

        The line should not have a trailing newline; it may have
        internal newlines.  The line is transformed and appended to a buffer.
        The interpreter's runsource() method is called with the
        concatenated contents of the buffer as source.  If this
        indicates that the command was executed or invalid, the buffer
        is reset; otherwise, the command is incomplete, and the buffer
        is left as it was after the line was appended.  The return
        value is 1 if more input is required, 0 if the line was dealt
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
            return
        except TokenError as exc:
            exc.args[0].startswith("EOF")
            return True
        except Exception as exc:
            print("UNHANDLED EXCEPTION in console.py. This should not happen.")
            raise exc

        if newsource != source:
            self.identical = False

        try:
            more = self.runsource(newsource, self.filename)
        except SystemExit:
            os._exit(1)
        except Exception as exc:
            print(exception_handling.handle_exception(exc, source))

        if not more:
            self.resetbuffer()
            if self.show_python and not self.identical:
                self.show_converted(newsource)
        return more

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
        if not self.identical:
            self.show_converted(self._source)
        super().showsyntaxerror(filename=filename)

    def do_transformations(self, source):
        """Performs the source transformations on the current content.

           Returns the transformed source.
        """
        source = conversion.to_python(source, source_name="REPL")
        source = self.fix_ending(source)

        self._source = source  # saved in case we need it if we want to show
        # a syntax error.See showsyntaxerror() above
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

    sys.ps1 = prompt
    console = AvantPyInteractiveConsole(locals=local_vars, show_python=show_python)
    console.locals.update(console_defaults)
    console.interact(banner=banner)
