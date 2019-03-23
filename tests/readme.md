# About these tests

For simplicity, wherever possible, I follow
[pytest](https://docs.pytest.org/en/latest/contents.html)'s strategy of
simply using Python's `assert` statements and naming test functions within
these files all starting with `test_` for easy discovery.

`pytest` is not part of Python's standard library and you may have to install it.

## File naming convention

All test files begin with either `test_`, `raise_`, or `catch_`.
In addition, you may find some files that begin with `tb_`.

- Files beginning with `test_`

   These files are meant to be run directly using Pytest and should be
   files that contain valid syntax - within a given dialect.
   Most should end with a `.pyxx` extension and be located in the
   corresponding `pyxx/` sub-directory.

   These files can be run without pytest by running them from the
   parent directory.  As a concrete example, you can try:

       python -m avantpy -s tests.pyen.test_repeat

   Note that the file `test_repeat.pyen` exists in `tests/pyen/`.

   A few standard Python test files, ending with `.py` can possibly be included.

- Files beginning with `raise_`

   These files will raise an exception. They too can be run individually,
   like the following:

       python -m avantpy -s tests.pyen.raise_if_nobreak

   However, they cannot be use directly by Pytest.
   They should end with a `.pyxx` extension and be located in the
   corresponding `pyxx/` sub-directory.

- Files beginning with `catch_`.

   These files will be run by Pytest and will typically import a file
   with a similar name, but beginning with `raise_`. Files beginning
   with `catch_` should end with a standard `.py` extension.

   Because of the way AvantPy works, we cannot use Pytest's standard
   way of capturing exceptions.
   Instead, upon importing the file, we catch the output and add it as
   an attribute to the file being tested.

   After importing and collecting all the tests, Pytest executes the test
   functions. At this stage, no further error is raise; however, we test
   to see if the file that was imported contains the captured exception.
   Here's an example file:

        def test_if_nobreak(capsys):                        # 1
            from . import raise_if_nobreak                  # 2
            if not hasattr(raise_if_nobreak, "err"):        # 3
                info = str(capsys.readouterr())             # 4
                raise_if_nobreak.err = info
            assert "IfNobreakError" in raise_if_nobreak.err # 5

    1. A function begins with test_, thus recognized as a test function by Pytest

    2. As we import the file, an exception is going to be raised. When it will
       be executed by Pytest, no new exception will be raised.

    3. After importing the file, it does not have an "err" attribute. When it
       will be executed by Pytest, it will have such an attribute and the
       code block (4, 5) will be ignored.

    4. We capture the output generated, using Pytest's capsys.

    5. This should be obvious :-)

- Files beginning with `tb_`.

   If such files are found, they are used to generate a record of
   tracebacks as they appear after processing by AvantPy. This can be used
   as a reference for different languages.  These files should be normal
   Python files, ending with the `.py` extension.
