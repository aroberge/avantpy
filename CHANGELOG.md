# Changelog

- Changed translations so that they are done with gettext
- Removed old way of supporting translations of human languages
- Printing information about language and dialect used in console
  when they are changed.
- console prompt now shows the py prefix to decrease potential confusion

## version 0.0.7

- Added GUI for conversion
  - Removed obsolete corresponding command line option
  - Removed --diff command line option as it is done better with the GUI.
- Tracebacks now written to stderr instead of stdout
- Simplified traceback for NameError done
- Improvement for long partial sources quoted in tracebacks
- Simple test added for transcoding
- Added tracebacks generation in French, with all pyupper examples reproduced
  - Also added corresponding pytest tests
- Console prompt is still based on dialect but does not include the py prefix.

## Version 0.0.6

- Console prompt is now based on dialect
- Transocode works.
  - Test is written, showing how to call it from user's code
  - Command line option --transcode implemented
- Properly implemented --show_converted option; it was active by default.
- Reorganized the tests by dialect, introducing new naming convention.

## Version 0.0.5

- Fixed bug in console
- Added translations of error messages in French and English

## Version 0.0.4

First recorded change log.

  - Console works
  - Diff works
  - Included dialects: pyupper, pyen, pyfr, pyes
  - Included languages: en
  - Custom exceptions implemented
  - Docs in good enough shape to have been published
  - Decent test coverage using pytest
  - etc.
