"""
avantpy sets up an import hook which
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

    python -m avantpy -s name
    python -m avantpy --source name

where ``name`` refers to a file named ``name.notpy``.  Any subsequent
``import`` statement will first look for file whose extension is ``notpy`` before
looking for normal ``py`` or ``pyc`` files. Any file with the ``notpy`` extension
that is imported will also be processed by the relevant source transformers.
Normal Python files will bypass the transformations.

A different extension that ``notpy`` can be specified as follows::

    python -m avantpy -s name -x EXTENSION
    python -m avantpy -s name --file_extension EXTENSION

Note that you really should not choose "py" and most definitely not "pyc"
as the file extension for files to be processed by ``avantpy``.

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
    and code explorations. avantpy includes a console which works
    reasonably well in most situations but can fail unexpectedly.
    To understand why, please console the documentation.

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
import glob
import runpy
import sys
import os.path

from . import config
from . import console
from . import import_hook

start_console = console.start_console

dialects = glob.glob(os.path.dirname(__file__) + "/dialects/*.py")
for f in dialects:
    if os.path.isfile(f) and not f.endswith("__init__.py"):
        name = os.path.basename(f)[:-3]
        config.FILE_EXT.append("py" + name)
        dialect = runpy.run_path(f)
        dialect_dict = {v: k for k, v in dialect[name].items()}
        config.DICTIONARIES["py" + name] = dialect_dict
        config.DICTIONARIES[name] = dialect[name]


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
        config.CONVERT = True
    else:
        show_python = False

    if args.diff:
        config.DIFF = True

    if args.file_extension is not None:
        config.FILE_EXT = args.file_extension

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
