# Roadmap

Goals:

- version 0.1: first public release
  - a simple editor has been written
- version 0.2: all Python Errors can be caught and an explanation provided
  - Have decided on whether or not using (py) gettext
    - if yes, document how to use it
    - if no, explain why since using gettext is the standard for internationalization.
    - See, for example https://news.ycombinator.com/item?id=2095334
    - One of many references: https://docs.readthedocs.io/en/latest/i18n.html

## Enhancements

- [ ] Make it possible to show the difflib output in an interactive session without exiting;
  This could be a more useful feature in an IDE environment
   - [ ] Have the possible options:
     - [ ] Only show the diff without executing the module
     - [ ] Show the diff and execute the module
     - [ ] Show the diff for a previously imported module
        - [ ] show errors if not an AvantPy module
     - [ ] Show the diff from a source file which is not imported.
- [ ] Add check for mixed spaces and tab characters: new lines should either all start with spaces
  or tabs, but not both.
- [ ] After implementing basic exception handling, confirm that it works
  - [ ] for the console
    - [ ] for SyntaxError
    - [ ] for other types not derived from SyntaxError
  - [ ] for imported file (e.g. pyen program import other pyen program, etc.)
    - [ ] for SyntaxError
    - [ ] for other types not derived from SyntaxError
  - [ ] Add demo GUI-based editor with syntax highlighting, perhaps similar to, but simpler than [this](http://www.bitforestinfo.com/2017/05/how-to-create-python-syntax-highlighting-functions-for-python-tkinter-text-widget-python-magicstick-text-editor-last-part.html)

- [ ] Add option to limit to one dialect only

- [ ] Use .format for string interpolation everywhere - to allow full translations
- [ ] Look at having translation for open()
- [ ] Review builtins and see if translations of other functions are needed.
- [ ] add syntax check in conversion
  - [ ] Closing ]}) not matching opening
  - [ ] opening [({ never closed

- [ ] Review https://realpython.com/pypi-publish-python-package/
- [ ] Try to reorganise tests into various subtests directories
- [ ] Consider switching to writing errors using print("...", file=sys.stderr)
  - [ ] Actually, have special function, like print_error, which can be redefined by other programs
- [ ] Always indicate the dialect being used in the console.

Some useful links to use as a start for improving error analysis:

    http://inventwithpython.com/appendixd.html
    https://inventwithpython.com/blog/2012/07/09/16-common-python-runtime-errors-beginners-find/
    https://www.dropbox.com/s/cqsxfws52gulkyx/drawing.pdf
    https://www2.cs.arizona.edu/people/mccann/errors-python
    https://tobiaskohn.ch/files/Dissertation_TKohn.pdf
    http://www.felienne.com/archives/6279

    Also, use = in an if statement comparison (and others)

## Contributors

- [ ] Add templates for various types of issues
  - [x] Bug report
  - [x] Feature request or contributions
  - [ ] Others

## Developers tools

- [ ] Command line option to convert from Python to dialect
  - This could be useful to quickly create test suites in a new dialect.
- [ ] Command line option to convert from dialect to Python
- [ ] Command line option to convert from dialect_1 to dialect_2
- [ ] GUI for above

## Testing

- [ ] Create comprehensive test for given dialect
  - [ ] use automated tools to convert to other dialects

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
