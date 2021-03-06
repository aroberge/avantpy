# Roadmap

- version 0.1:
  - all standard Python Errors can be caught and an explanation provided
    - a simple tkinter-based IDE has been written as a demo
  - Consider having a simplified and translated turtle module included
    - perhaps do this via a special `magicturtle` keyword to be use on its own,
      which would set everything up and make a small subset of turtle
      functions available.

## TODO

- [ ] Write a script to prepare a new release. This script should ensure that
      all the traceback pages are updated.

- [ ] Add explanation about unusual spacing of translation files.

- GUI
  - [ ] Add screen capture of GUI to docs
  - [x] Add error handling in GUI
  - [x] Improve appearance of main GUI window by using grid manager
  - [ ] Look into creating GUI for REPL
  - [ ] Translate GUI

- [ ] Change error handling to pass original and transformed source so as
      to compare with Python's info about line of code when it is provided
      as a confirmation that we are not making a mistake in the processing.
    - [ ] Pass the name of the source as well, rather than storing it in
      a global state.

- [ ] Review builtins and see if translations of other functions are needed.

- [ ] thread about international turtle module https://mail.python.org/pipermail/python-ideas/2015-September/035672.html
  - [ ] Perhaps add a function, say tortue() in French, and turtle() in English,
    that loads up the turtle module, and activate some translations, providing some
    additional help...  Perhaps display the help whenever tortue() is typed in.
    - [ ] Idea: use a keyword like `magicturtle` that would enable all turtle functions.
  - [ ] Simple localizable turtle module https://docs.python.org/dev/library/cmd.html#cmd-example
  - [ ] If so, add basic translations of basic colors.
  - [ ] If so, perhaps add a page in the documentation like https://ecsdtech.com/8-pages/121-python-turtle-colors but adding rgb and hex code for colors

Some useful links to use as a start for improving error analysis:

    http://inventwithpython.com/appendixd.html
    https://inventwithpython.com/blog/2012/07/09/16-common-python-runtime-errors-beginners-find/
    https://www.dropbox.com/s/cqsxfws52gulkyx/drawing.pdf
    https://www2.cs.arizona.edu/people/mccann/errors-python
    https://tobiaskohn.ch/files/Dissertation_TKohn.pdf
    http://www.felienne.com/archives/6279
    https://swcarpentry.github.io/python-novice-inflammation/07-errors/index.html

    Also, use = in an if statement comparison (and others)

    https://mail.python.org/pipermail/python-ideas/2012-August/015989.html

    http://www.python.org.ar/wiki/MensajesExcepcionales

## Contributors

- [ ] Add templates for various types of issues
  - [x] Bug report
  - [x] Feature request or contributions
  - [ ] Others

## Integrating with other programs

While AvantPy works as a standalone application, it should be possible
to integrate it with other programs.

- [ ] Can it be integrated with Idle ?
- [ ] Can a tool be written to easily enable syntax highlighting for a given dialect in some text editor?
  - It should be possible to take an existing file for Python, process it to add the keywords from a `pyxx.py` dialect file, and save it as a new syntax file. Ideally this process should be documented with a complete example showing
      1. how to find the existing Python file
      2. how to use the tool to create the new file (say pyfr)
      3. how to add the newly created file so that it is recognized by the editor.

    I would like to know how to do this for SublimeText and Visual Studio Code..
- [ ] Can it be integrated with Mu?
- [ ] Can it be integrated with Thonny?

## Reference: known exceptions

In the following, those that are followed by an * have been implemented.

BaseException
 +-- SystemExit
 +-- KeyboardInterrupt
 +-- GeneratorExit
 +-- Exception
      +-- StopIteration
      +-- StopAsyncIteration
      +-- ArithmeticError
      |    +-- FloatingPointError
      |    +-- OverflowError
      |    +-- ZeroDivisionError
      +-- AssertionError
      +-- AttributeError
      +-- BufferError
      +-- EOFError
      +-- ImportError
      |    +-- ModuleNotFoundError
      +-- LookupError
      |    +-- IndexError
      |    +-- KeyError
      +-- MemoryError
      +-- NameError  *
      |    +-- UnboundLocalError
      +-- OSError
      |    +-- BlockingIOError
      |    +-- ChildProcessError
      |    +-- ConnectionError
      |    |    +-- BrokenPipeError
      |    |    +-- ConnectionAbortedError
      |    |    +-- ConnectionRefusedError
      |    |    +-- ConnectionResetError
      |    +-- FileExistsError
      |    +-- FileNotFoundError
      |    +-- InterruptedError
      |    +-- IsADirectoryError
      |    +-- NotADirectoryError
      |    +-- PermissionError
      |    +-- ProcessLookupError
      |    +-- TimeoutError
      +-- ReferenceError
      +-- RuntimeError
      |    +-- NotImplementedError
      |    +-- RecursionError
      +-- SyntaxError
      |    +-- IndentationError *
      |         +-- TabError *
      +-- SystemError
      +-- TypeError
      +-- ValueError
      |    +-- UnicodeError
      |         +-- UnicodeDecodeError
      |         +-- UnicodeEncodeError
      |         +-- UnicodeTranslateError
      +-- Warning
           +-- DeprecationWarning
           +-- PendingDeprecationWarning
           +-- RuntimeWarning
           +-- SyntaxWarning
           +-- UserWarning
           +-- FutureWarning
           +-- ImportWarning
           +-- UnicodeWarning
           +-- BytesWarning
           +-- ResourceWarning
