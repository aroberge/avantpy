# Roadmap

## Enhancements

- [x] Add option to restrict processing to single dialect
  - In this case, only load single dialect file; if not found, issue error message and exit.
- [x] Think of replacing `__name__ is "__main__"` by a single keyword, perhaps `NotImported`.
- [x] Change html template for html output produced by difflib
- [ ] Make it possible to show the difflib output in an interactive session without exiting;
  This could be a more useful feature in an IDE environment
   - [ ] Have the possible options:
     - [ ] Only show the diff without executing the module
     - [ ] Show the diff and execute the module
     - [ ] Show the diff for a previously imported module
        - [ ] show errors if not an AvantPy module
     - [ ] Show the diff from a source file which is not imported.
- [ ] Consider adding a check in the tokenizer to ensure that opening and closing brackets match.
- [ ] Add check for mixed spaces and tab characters: new lines should either all start with spaces
  or tabs, but not both.
- [ ] After implementing basic exception handling, confirm that it works 
  - [ ] for the console
    - [ ] for SyntaxError
    - [ ] for other types not derived from SyntaxError
  - [ ] for imported file (e.g. pyen program import other pyen program, etc.)
    - [ ] for SyntaxError
    - [ ] for other types not derived from SyntaxError
  - [ ] Add demo GUI-based editor with syntax highlighting, perhaps similar to,but simpler than [this](http://www.bitforestinfo.com/2017/05/how-to-create-python-syntax-highlighting-functions-for-python-tkinter-text-widget-python-magicstick-text-editor-last-part.html)

- [ ] Use .format for string interpolation everywhere.

## Documentation

- [x] Create simple GitHub Pages site
  - [x] Get inspiration from what I did for pyextension.
  - [x] Add section about invocation
  - [ ] Explain various choices for addition to syntax
    - [x] Explain why **repeat** and other loops
    - [ ] Explain why `function` instead of `lambda`
    - [x] If replacing `if __name__ == "__main__"`, explain
    - [x] Explain why not `else` in `for` and `while` loops
      - Actually, it might be possible to replace this by keeping track of loop or if indentation level
  - [ ] Explain how to use pytest
    - [ ] Explain how to create new tests
  - [ ] Explain how to run a single test without using pytest

## Contributors

- [ ] Add code of conduct
- [ ] Add templates for various types of issues
  - [x] Bug report
  - [x] Feature request or contributions
  - [ ] Others
- [ ] Add info about contributors and refer to documentation

## Developers tools

- [ ] Command line option to convert from Python to dialect
  - This could be useful to quickly create test suites in a new dialect.
- [ ] Command line option to convert from dialect to Python
- [x] Command line option to show code in dialect and Python side by side, highlighting differences
- [ ] GUI for above

## Syntax analysis and feedback

- [ ] Add hook to replace standard Python tracebacks
  - [ ] Implement one or two simple error analysis
  - [ ] Add more in future phase
- [ ] Use gettext to provide translations

## Testing

- [x] Add test for console
- [ ] Create comprehensive test for given dialect
- [x] Add UPPERCASE English dialect
  - [ ] Add test for this

## Integrating with other programs

While AvantPy works as a standalone application, it should be possible
to integrate it with other programs.  

- [ ] Can it be integrated with Idle ?
- [ ] Can a tool be written to easily enable syntax highlighting for a given dialect in some text editor?
  - It should be possible to take an existing file for Python, process it to add the keywords from a `xx.py` dialect file, and save it as a new syntax file. Ideally this process should be documented with a complete example showing
      1. how to find the existing Python file
      2. how to use the tool to create the new file (say pyfr)
      3. how to add the newly created file so that it is recognized by the editor.

    I would like to know how to do this for SublimeText and Visual Studio Code..
- [ ] Can it be integrated with Mu?
- [ ] Can it be integrated with Thonny?