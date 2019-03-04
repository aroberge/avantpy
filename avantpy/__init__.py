"""
AvantPy sets up an import hook which
makes it possible to run a file that contains modified Python syntax,
provided the relevant source transformers can be imported.

.. warning::

    It is always a good idea to not confirm that what follows below is
    still accurate. You can confirm this by running one of the following
    two alternatives::

        python -m avantpy -h
        python -m avantpy --help

.. note::

    Every relevant flag specific to avantpy has a short form and a
    long form. In what follows we always show both alternatives.

Basic invocation
----------------

The primary role of avantpy is to run programs that have a modified syntax.
This is done by one of the two following alternatives::

    python -m avantpy -s path.to.file
    python -m avantpy --source path.to.file

Note: do not include the extension in path.to.file.

A different extension that ``notpy`` can be specified as follows::

    python -m avantpy -s name -x EXTENSION
    python -m avantpy -s name --file_extension EXTENSION

Additional utilities
--------------------

If you want to view how avantpy transformed an input file,
you can use the ``-d`` or ``--diff`` option::

    python -m avantpy -s name -d
    python -m avantpy --source name --diff

This will use Python's ``difflib`` module and write the result in a
file named ``name.html`` in the current directory.

.. todo::

   * document ``-c`` (``--convert``)
   * Implement ``-o [filename]`` (``--output``) and document

Quirky console
---------------

.. note::

    Python's interpreter console (REPL) is a useful tool for quick demos
    and code explorations. AvantPy includes a console which appears
    to work reasonably well.  Please, feel free to file issues for any
    unexpected behaviour.

The simplest way to invoke pyextension's console is as follows::

    python -m avantpy

.. todo::

    * document ``-c`` when using the console
    * document ``-d`` when using the console
    * document ``-t`` when using the console

Python's interactive mode
-------------------------

.. todo::

    Document Python's ``-i`` flag (interactive mode)

"""
import argparse
import sys

from . import transforms
from . import console
from . import import_hook

start_console = console.start_console

if "-m" in sys.argv:
    console_dict = {}
    parser = argparse.ArgumentParser(
        description="""
        avantpy sets up an import hook which
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
        "-x",
        "--file_extension",
        help="The file extension of the module to load; default=notpy",
    )

    parser.add_argument(
        "-c",
        "--convert",
        help="Show the original code and the code transformed into standard Python.",
        action="store_true",
    )

    parser.add_argument(
        "-d",
        "--diff",
        help="""Creates an html file containing a showing
                how the original source differs from the transformed one.""",
        action="store_true",
    )

    args = parser.parse_args()

    if args.convert:
        show_python = True
        transforms.CONVERT = True
    else:
        show_python = False

    if args.diff:
        transforms.DIFF = True

    if args.file_extension is not None:
        transforms.FILE_EXT = args.file_extension

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
