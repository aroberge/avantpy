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

When using the console, one can see the transformed code,
if it is different from the code entered, by using the
``--show_converted`` option.


Transcoding from one dialect into another
-----------------------------------------

It is possible to transcode a file from one dialect to another.
This is done using the --transcode option, together with two
other flags: --from_path and --to_path.

For example, assuming test_french.pyfr exists (it does), we can
obtain a corresponding english version by the following::

    python -m avantpy --transcode --from_path tests/test_french.pyfr
          --to_path tests/test_english.pyen
"""
import argparse
import sys

from . import session
from . import console
from . import exception_handling
from . import import_hook
from . import converter

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
        help="""Source file to be transformed and executed.
                It is assumed that it can be imported.
                Format: path.to.file -- Do not include an extension.""",
    )
    parser.add_argument(
        "--lang",
        help="""This sets the language used by AvantPy.
                Usually this is a two-letter code such as 'fr' for French.
                If no dialect is specified, this will also sets the corresponding
                dialect""",
    )

    parser.add_argument(
        "--dialect",
        help="""This sets the dialect used by AvantPy.
                Usually this is a two-letter code such as 'pyfr' for French.
                If 'lang' is not specified, this will also sets the corresponding
                value for lang.""",
    )

    parser.add_argument(
        "--diff",
        help="""Creates an html file containing a showing
                how the original source differs from the transformed one,
                opens a tab in the default browser showing this html file,
                and exits without executing the code from the source.""",
        action="store_true",
    )

    parser.add_argument(
        "--dev_py",
        help="""This disables the custom exception handling so that Python
                tracebacks are printed""",
        action="store_true",
    )

    parser.add_argument(
        "--show_converted",
        help="""When using the console, if this flag is set, each time the
                code entered is compaeed with the code transformed. If the
                two are not identical, the converted code is printed in
                the console.""",
        action="store_true",
    )

    parser.add_argument(
        "--transcode",
        help="""Indicates that a file is to be transcoded from one dialect
                to another. If -s or --source is specified, this is ignored.
            """,
        action="store_true",
    )
    parser.add_argument(
        "--from_path",
        help="""This is used together with the --transcode option to specify the
                 relative path of the file to be transcoded.
                 The dialect is determined from the extension.
             """,
    )
    parser.add_argument(
        "--to_path",
        help="""This is used together with the --transcode option to specify the
                 relative path of the file to be transcoded.
                 The dialect is determined from the extension.
                 """,
    )

    args = parser.parse_args()

    if args.diff:
        import_hook.show_diff()

    if args.lang is not None:
        session.state.set_lang(args.lang)

    if args.dialect is not None:
        session.state.set_dialect(args.dialect)

    if args.show_converted:
        show_python = True

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
                start_console(local_vars=main_dict, show_python=show_python)
        except ModuleNotFoundError:
            print("Could not find module ", args.source, "\n")
            raise
    elif args.transcode:
        if args.from_path is None:
            print("--from_path must be specified with --transcode.")
            sys.exit()
        if args.to_path is None:
            print("--to_path must be specified with --transcode.")
            sys.exit()
        converter.transcode_file(args.from_path, args.to_path)
    else:
        start_console(local_vars=console_dict, show_python=show_python)
