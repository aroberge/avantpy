"""
invocation.py
---------------

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

The following example is run from the root folder of the AvantPy repository.
The file that is run ends with the ``pyfr`` extension which AvantPy uses
to recognize that the French dialect is to be used::

    $ python -im avantpy -s tests.pyfr.test_french
    Success.
    avantpy console version 0.0.5. [Python version: 3.7.0]

    ->> si Vrai:
    ...     afficher(bonjour)
    ...
    Bonjour tout le monde !
    ->>

"""
import argparse
import sys

from . import session
from . import exception_handling
from . import import_hook
from . import gui
from . import console


parser = argparse.ArgumentParser(
    description="""AvantPy sets up an import hook which
            makes it possible to run a file that contains modified Python syntax
            provided the relevant source transformers can be imported.
        """
)
parser.add_argument(
    "-s",
    "--source",
    help="""Source file to be transformed and executed.
            It is assumed that it can be imported.
            Format: path.to.file -- Do not include an extension.
         """,
)
parser.add_argument(
    "--lang",
    help="""This sets the language used by AvantPy.
            Usually this is a two-letter code such as 'fr' for French.
            If DIALECT is not specified, this will also sets the corresponding
            DIALECT.
         """,
)

parser.add_argument(
    "--dialect",
    help="""This sets the dialect used by AvantPy.
            Usually this is a two-letter code such as 'pyfr' for French.
            If LANG is not specified, this will also sets the corresponding
            value for LANG.
         """,
)

parser.add_argument(
    "--dev_py",
    help="""This disables the custom exception handling so that Python
            tracebacks are printed.
         """,
    action="store_true",
)


parser.add_argument(
    "--gui",
    help="""Launches a basic GUI interface, useful for some converting
            programs from one dialect into another or into Python.
         """,
    action="store_true",
)


console_dict = {}
args = parser.parse_args()

if args.lang is not None:
    session.state.set_lang(args.lang)

if args.dialect is not None:
    session.state.set_dialect(args.dialect)

if args.dev_py:
    exception_handling.disable()

if args.source is not None:
    try:
        main_module = import_hook.import_main(args.source)
        if sys.flags.interactive:
            main_dict = {}
            for var in dir(main_module):
                if var in ["__cached__", "__loader__", "__package__", "__spec__"]:
                    continue
                main_dict[var] = getattr(main_module, var)
            console.start_console(local_vars=main_dict)
    except ModuleNotFoundError:
        print("Could not find module ", args.source, "\n")
        raise
elif args.gui:
    gui.main()
else:
    console.start_console(local_vars=console_dict)
