# Roadmap

Goals:

- version 0.1: first public release
  - Consider having a simplified and translated turtle module included
    - perhaps do this via a special `magicturtle` keyword to be use on its own,
      which would set everything up and make a small subset of turtle
      functions available.
- version 0.2: all Python Errors can be caught and an explanation provided
  - Have decided on whether or not using (py) gettext
    - if yes, document how to use it
    - if no, explain why since using gettext is the standard for internationalization.
    - See, for example https://news.ycombinator.com/item?id=2095334
    - One of many references: https://docs.readthedocs.io/en/latest/i18n.html
  - a simple tkinter-based IDE has been written


## Enhancements

- [ ] Review scratch and blockly for alternative to "continue"
- [ ] Simple localizable turtle module https://docs.python.org/dev/library/cmd.html#cmd-example

- [ ] Make it possible to show the difflib output in an interactive session without exiting;
  This could be a more useful feature in an IDE environment
   - [ ] Have the possible options:
     - [ ] Only show the diff without executing the module
     - [ ] Show the diff and execute the module
     - [ ] Show the diff for a previously imported module
        - [ ] show errors if not an AvantPy module
     - [ ] Show the diff from a source file which is not imported.

  - [ ] Add demo GUI-based editor with syntax highlighting, perhaps similar to, but simpler than [this](http://www.bitforestinfo.com/2017/05/how-to-create-python-syntax-highlighting-functions-for-python-tkinter-text-widget-python-magicstick-text-editor-last-part.html)

- [ ] Use .format for string interpolation everywhere - to allow full translations
- [ ] Review builtins and see if translations of other functions are needed.

- [ ] Consider switching to writing errors using print("...", file=sys.stderr)
  - [ ] Actually, have special function, like print_error, which can be redefined by other programs

- [ ] thread about international turtle module https://mail.python.org/pipermail/python-ideas/2015-September/035672.html
  - [ ] Perhaps add a function, say tortue() in French, and turtle() in English,
    that loads up the turtle module, and activate some translations, providing some
    additional help...  Perhaps display the help whenever tortue() is typed in.

Some useful links to use as a start for improving error analysis:

    http://inventwithpython.com/appendixd.html
    https://inventwithpython.com/blog/2012/07/09/16-common-python-runtime-errors-beginners-find/
    https://www.dropbox.com/s/cqsxfws52gulkyx/drawing.pdf
    https://www2.cs.arizona.edu/people/mccann/errors-python
    https://tobiaskohn.ch/files/Dissertation_TKohn.pdf
    http://www.felienne.com/archives/6279

    Also, use = in an if statement comparison (and others)

    https://mail.python.org/pipermail/python-ideas/2012-August/015989.html

    http://www.python.org.ar/wiki/MensajesExcepcionales

## Contributors

- [ ] Add templates for various types of issues
  - [x] Bug report
  - [x] Feature request or contributions
  - [ ] Others

## Developers tools

- [ ] Command line option to convert from dialect to Python
- [x] Command line option to convert from dialect_1 to dialect_2
- [ ] GUI for above
- [ ] Combine --diff option with these

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
