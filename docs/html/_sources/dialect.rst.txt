Language or dialect?
=====================

In this documentation, the words "dialect" and "language" are used in what may seem
at first to be a confusing way.

Python is our main programming language. 
Python's keywords and other names are based on the English language.
AvantPy enables users to write programs with keywords based on their native language.
In this documentation, a **dialect** refers to an **extension to the Python programming language** 
which includes non-English based keywords.

A given language is identified by its 
`two-letter code <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_.
For example, ``fr`` identifies the French language.

AvantPy will recognize that a file with an extension of the form
``.pyxx`` is based on the ``xx`` language, provided a corresponding
language definition has been created.
Thus a file with the extension ``.pyfr`` is based on the French language.
We refer to such files as being written in the French (Python) dialect.

Dialects definitions for language ``xx`` are Python files 
named ``xx.py`` and are found in the AvantPy's repository:
`avantpy/dialects/ directory <https://github.com/aroberge/avantpy/tree/master/avantpy/dialects>`_.


AvantPy's English dialect
--------------------------

AvantPy includes an English dialect (``.pyen``) which adds a few keywords and constructs
to Python. 
The corresponding 
`definition file <https://github.com/aroberge/avantpy/blob/master/avantpy/dialects/en.py>`_
should be used as the basis for the creation of a new dialect.

In addition to the additional keywords needed for the special idioms used in AvantPy,
and explained later in this documentation, the English dialect includes the
keyword ``function`` as being equivalent to ``lambda``.
