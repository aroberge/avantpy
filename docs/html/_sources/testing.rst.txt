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

    $ python -m avantpy -s tests.pyfr.test_french

If the test is successful, you should see a single line, something like::

    Success.

Writing tests
-------------

.. warning::

    Please consult the **readme.md** file in the tests directory.
