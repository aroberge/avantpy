"""
AvantPy sets up an import hook which
makes it possible to run a file that contains modified Python syntax,
provided the relevant source transformers can be imported.

Basic invocation
----------------

The simplest invocation of AvantPy sets up the import hook,
collect all existing dialects, and leaves the user in a custom REPL::

    python -m avantpy

This custom REPL should work in a way similar to Python's own.
Please, feel free to file issues for any unexpected behaviour.

If you want to select a particular dialect/language to be available in the
console, you can use the ``--lang`` flag::

    python -m avantpy --lang fr

If a source program is to be run, as described below, the ``--lang`` flag
is ignored.

Running programs
----------------

.. sidebar:: Duplicate flags

    Many flags specific to avantpy 
    have a short form and a long form.
    In what follows we always show both alternatives.

The primary role of AvantPy is to run programs that have a modified syntax.
This is done by one of the two following alternatives::

    python -m avantpy -s path.to.file
    python -m avantpy --source path.to.file

.. warning::

    Do not include the extension in path.to.file.

You can use Python's interactive flag, either separately,
as in ``python -i -m ...`` or combined with the ``-m`` flag
as done below, to execute a program to be run as "main" and
continue with the console.

The following example is run from the rood folder of the AvantPy repository.
The file that is run ends with the ``pyfr`` extension which AvantPy uses
to recognize that the French dialect is to be used::

    $ python -im avantpy -s tests.test_french
    Success.
    avantpy console version 0.0.3. [Python version: 3.7.0]

    ->> si Vrai:
    ...     imprime(bonjour)
    ...
    Bonjour tout le monde !
    ->>


Showing the corresponding Python code
--------------------------------------

If you want to view how avantpy transformed an input file,
you can use the ``--diff`` option::

    python -m avantpy --source name --diff

This will use Python's ``difflib`` module to write the result in a
file named ``name.html`` in the current directory, open a new tab
in the default web browser and display the result.
This will also end the current execution.
The code in the source file will not be executed.

Debug flag
----------

By using the ``--debug`` flag, one can see how the code is translated.
For example, one can try::

    python -m avantpy --debug

"""
import argparse
import sys

from . import conversion
from . import console
from . import exception_handling
from . import import_hook

start_console = console.start_console
show_python = False

if "-m" in sys.argv:
    console_dict = {}
    parser = argparse.ArgumentParser(
        description="""
        AvantPy sets up an import hook which
        makes it possible to run a file that contains modified Python syntax
        provided the relevant source transformers can be imported.
        """
    )
    parser.add_argument(
        "-s",
        "--source",
        help="""Source file to be transformed.
                Format: path.to.file -- Do not include an extension.""",
    )
    parser.add_argument(
        "--lang",
        help="""This restricts AvantPy to using a single language.
                Usually this is a two-letter code such as 'fr' for French.""",
    )

    parser.add_argument(
        "-d",
        "--diff",
        help="""Creates an html file containing a showing
                how the original source differs from the transformed one,
                opens a tab in the default browser showing this html file,
                and exits without executing the code from the source.""",
        action="store_true",
    )

    parser.add_argument(
        "--debug",
        help="""In the debug mode, various information is printed as files
                and input in console are processed.""",
        action="store_true",
    )

    parser.add_argument(
        "--dev_py",
        help="""This disables the custom exception handling so that Python 
                tracebacks are printed""",
        action="store_true",
    )

    args = parser.parse_args()

    if args.diff:
        import_hook.show_diff()

    if args.lang is not None:
        conversion.set_lang(args.lang, only=True)

    if args.debug:
        show_python = True
        conversion.set_debug(True)

    if not args.dev_py:
        exception_handling.enable()

    if args.source is not None:
        try:
            main_module = import_hook.import_main(args.source)
            if sys.flags.interactive:
                main_dict = {}
                for var in dir(main_module):
                    if var in ["__cached__", "__loader__", "__package__", "__spec__"]:
                        continue
                    main_dict[var] = getattr(main_module, var)
                start_console(local_vars=main_dict, show_python=show_python)
        except ModuleNotFoundError:
            print("Could not find module ", args.source, "\n")
            raise
    else:
        start_console(local_vars=console_dict, show_python=show_python)
