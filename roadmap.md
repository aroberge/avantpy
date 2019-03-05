# Roadmap

## Documentation

- [x] Create simple GitHub Pages site
  - [x] Get inspiration from what I did for pyextension.
  - [x] Add section about invocation
  - [ ] Explain various choices for addition to syntax
    - [ ] Explain why **repeat** and other loops
    - [ ] Explain why `function` instead of `lambda`
    - [ ] If replacing `if __name__ == "__main__"`, explain
    - [ ] Explain why not `else` in `for` and `while` loops
      - Actually, it might be possible to replace this by keeping track of loop or if indentation level
  - [ ] Explain how to use pytest
    - [ ] Explain how to create new tests
  - [ ] Explain how to run a single test without using pytest

## Contributors

- [ ] Add code of conduct
- [ ] Add templates for various types of issues
  - [ ] Bug report
  - [ ] Feature request or contributions
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

- [ ] Add tests for console
- [ ] Create comprehensive test for given dialect
- [ ] Add UPPERCASE English dialect

## Enhancements

- [ ] Consider using `colorama` as optional dependencies for the console
- [ ] Add option to restrict processing to single dialect
  - In this case, only load single dialect file; if not found, issue error message and exit.
- [x] Think of replacing `__name__ is "__main__"` by a single keyword, perhaps `NotImported`.

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