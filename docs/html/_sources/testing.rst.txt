Testing
==================

AvantPy uses assertion-based tests, best run with `pytest <https://docs.pytest.org>`_.

In what follows, we assume you start from the root directory of the code repository.

Running tests
-------------

To run all the tests, you simply need to do::

    $ pytest

Here, the dollar sign ($) indicates the prompt in your terminal (command line); 
some other symbol or combination of symbol may be used on your computer.

If you want to run a single test, you don't need to use pytest, and can use AvantPy directly.
As an explicit exemple, you can try this:

    $ python -m avantpy -s test.test_french

If the test is successful, you should see a single line, something like::

    Success.

Writing tests
-------------

To take advantage of pytest's ease of use for test discovery, you should write your
test in the ``tests`` directory.  This directory includes an ``__init__.py`` file
which ensures that avantpy's import hook is properly activated when running tests
using pytest.

To ensure test discovery, (most of )your file names should also begin with ``test_``.
I will explain below when not to follow this convention.

As an example, here's the content of a simple test that should be in the
tests directory, named ``test_assert.pyupper``::

    DEF test_assert():
        ASSERT TRUE

    IF __name__ == '__main__':
        test_assert()
        PRINT('Success.')

The ``pyupper`` extension of the filename identifies
this as the dialect where all Python's keywords are written in uppercase; this
dialect is intended to be used only for testing purpose.

The way that pytest works (by default) is to collect all files whose name
starts with ``test_``, import them, and run all functions whose names also
begin with ``test_``.

When ``test_assert.pyupper`` is imported, AvantPy's import mechanism gets invoked
before the normal Python import mechanism does, identify the file with the ``.pyupper``
extension as being valid, and transforms its source into valid Python code
before executing it.

.. warning::

    If more than one file has the same base name, but different extension, AvantPy
    will only import one of them. 

Testing exceptions
-------------------

Imagine we have a ``pyenv`` test file with the following content::

    def test_if_nobreak():
        if True:
            pass
        nobreak:
            pass 

A ``nobreak`` keyword can only be used with a ``for`` or a ``while`` loop.
As a result, AvantPy would transforms this into something like::

    def test_if_nobreak():
        if True:
            pass
        # nobreak
    raise SyntaxError("nobreak is not allowed as a block with an if statement)")

Upon executing this file, a syntax error would be raised which would not be caught
properly by pytest.  If this file has a name that does not start with ``test_``,
pytest will ignore it.  In the tests directory, there is a similar file
named ``if_nobreak.pyen``.  There is another file named ``test_if_nobreak.py`` 
whose content is the following::

    import pytest

    def test_if_nobreak():
        with pytest.raises(SyntaxError):
            from . import if_nobreak

    if __name__ == '__main__':
        test_if_nobreak()
        print("Success.")

As you can see, this file imports the file which will include a ``raise SyntaxError``
statement, once processed by AvantPy.  This tests the transformation of ``if_break.pyen``
indirectly, in such a way that pytest can do its test correctly.