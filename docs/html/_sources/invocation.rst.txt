Invocation
===========

If you cannot wait to try AvantPy before reading the rest of the documentation,
here's how you can do it::

    $ python -m avantpy -h
    usage: -m [-h] [-s SOURCE] [--lang LANG] [--dialect DIALECT] [--dev_py]
              [--show_converted] [--gui]

    AvantPy sets up an import hook which makes it possible to run a file that
    contains modified Python syntax provided the relevant source transformers can
    be imported.

    optional arguments:
      -h, --help            show this help message and exit
      -s SOURCE, --source SOURCE
                            Source file to be transformed and executed. It is
                            assumed that it can be imported. Format: path.to.file
                            -- Do not include an extension.
      --lang LANG           This sets the language used by AvantPy. Usually this
                            is a two-letter code such as 'fr' for French. If
                            DIALECT is not specified, this will also sets the
                            corresponding DIALECT.
      --dialect DIALECT     This sets the dialect used by AvantPy. Usually this is
                            a two-letter code such as 'pyfr' for French. If LANG
                            is not specified, this will also sets the
                            corresponding value for LANG.
      --dev_py              This disables the custom exception handling so that
                            Python tracebacks are printed.
      --show_converted      When using the console, if this flag is set, each time
                            the code entered is compaeed with the code
                            transformed. If the two are not identical, the
                            converted code is printed in the console.
      --gui                 Launches a basic GUI interface, useful for some
                            converting programs from one dialect into another or
                            into Python.


.. sidebar:: Straight from the source

    The content of the rest of this page comes from the
    docstring of ``invocation.py``.


.. automodule:: avantpy.invocation
   :members:

