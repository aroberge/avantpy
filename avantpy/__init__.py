"""
pyextensions sets up an import hook which
makes it possible to run a file that contains modified Python syntax,
provided the relevant source transformers can be imported.

.. warning::

    It is always a good idea to not confirm that what follows below is
    still accurate. You can confirm this by running one of the following
    two alternatives::

        python -m pyextensions -h
        python -m pyextensions --help

.. note::

    Every relevant flag specific to pyextensions has a short form and a
    long form. In what follows we always show both alternatives.

Basic invocation
----------------

The primary role of pyextensions is to run programs that have a modified syntax.
This is done by one of the two following alternatives::

    python -m pyextensions -s name
    python -m pyextensions --source name

where ``name`` refers to a file named ``name.notpy``.  Any subsequent
``import`` statement will first look for file whose extension is ``notpy`` before
looking for normal ``py`` or ``pyc`` files. Any file with the ``notpy`` extension
that is imported will also be processed by the relevant source transformers.
Normal Python files will bypass the transformations.

A different extension that ``notpy`` can be specified as follows::

    python -m pyextensions -s name -x EXTENSION
    python -m pyextensions -s name --file_extension EXTENSION

Note that you really should not choose "py" and most definitely not "pyc"
as the file extension for files to be processed by ``pyextensions``.

Additional utilities
--------------------

If you want to view how pyextensions transformed an input file,
you can use the ``-d`` or ``--diff`` option::

    python -m pyextensions -s name -d
    python -m pyextensions --source name --diff

This will use Python's ``difflib`` module and write the result in a
file named ``name.html`` in the current directory.

.. todo::

   * document ``-c`` (``--convert``)
   * Implement ``-o [filename]`` (``--output``) and document

Quirky console
---------------

.. note::

    Python's interpreter console (REPL) is a useful tool for quick demos
    and code explorations. pyextensions includes a console which works
    reasonably well in most situations but can fail unexpectedly.
    To understand why, please console the documentation.

The simplest way to invoke pyextension's console is as follows::

    python -m pyextensions



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
import os.path

from . import config
from . import console
from . import import_hook
from . import transforms

start_console = console.start_console

# It is assumed that code transformers are third-party modules
# to be installed in a location from where they can be imported.
# For this proof of concept, we add a fake site-packages directory
# where the sample transformers will be located

top_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
fake_site_pkg = os.path.join(top_dir, "fake_site_pkg")

if not os.path.exists(fake_site_pkg):
    raise NotImplementedError(
        "A fake_site_pkg directory must exist for this demo to work correctly."
    )
sys.path.insert(0, fake_site_pkg)


if "-m" in sys.argv:
    console_dict = {}
    parser = argparse.ArgumentParser(
        description="""
        pyextensions sets up an import hook which
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

    parser.add_argument(
        "-t",
        "--transformers",
        nargs="+",
        help="Transformers to import if not loading source file",
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
        if args.transformers is not None:
            for tr in args.transformers:
                console_dict[tr] = transforms.import_transformer(tr)
        start_console(local_vars=console_dict, show_python=show_python)
