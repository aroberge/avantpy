# About these tests

For simplicity, wherever possible, I follow [pytest](https://docs.pytest.org/en/latest/contents.html)'s strategy of simply using Python's `assert` statements and naming test files and test functions within these files all starting with `test_` for easy discovery. `pytest` is not part of Python's standard library and you may have to intall it.

## Running a single test without pytest

To run a single test file `test_something.pyxx` without using pytest, we simply have to do

    python -m avantpy -s tests.test_something

also from the parent directory.
