Language or dialect?
=====================

In this documentation, the words "dialect" and "language" are used in what may seem
at first to be a confusing way.

A given language is identified by its
`two-letter code <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_.
For example, ``fr`` identifies the French language.

Dialects definitions for language ``xx`` are Python files
named ``pyxx.py`` and are found in the AvantPy's repository:
`avantpy/dialects/ directory <https://github.com/aroberge/avantpy/tree/master/avantpy/dialects>`_.


.. warning::

    In the console below, instead of Python's standard main prompt,
    ``>>> ``, the main prompt shows the **dialect** being used
    without including the prefix ``py``. This is to keep it to the
    same length as the standard Python prompt,
    except when the UPPERCASE dialect (pyupper) is used.

    This could change.

Perhaps an example is the best way to demonstrate, using two different
"languages" in an unusual way.
We we will generate an
error message by trying to assign the AvantPy keyword ``repeat``
(``répéter`` in the French **dialect**) and show the error message
in the other language using the AvantPy console::

    $ python -m avantpy --lang fr --dialect pyen
    AvantPy version 0.0.7. [Python version: 3.7.0]

    en> repeat 3:
    ...     print('Hello!')
    ...
    Hello!
    Hello!
    Hello!
    en> # Let's do something forbidden; the explanation will be in French
    en> a = repeat

        Exception AvantPy: RepeatFirstError

        Erreur trouvée dans le fichier REPL à la ligne 1.

        Dialecte utilisé: pyen

        -->1: a = repeat

        Le mot-clé repeat spécifique à Avantpy peut seulement être utilisé
        pour débuter une nouvelle boucle 'pour' ou 'tantque'
        (équivalent Python: 'for' ou 'while').

    en> # Ok, let's do things in opposite languages
    en> set_lang('en')
    en> set_dialect('pyfr')
    'pyfr'
    fr> répéter 3:
    ...     afficher('Bonjour !')
    ...     print('---')  # Normal Python always recognized.
    ...
    Bonjour !
    ---
    Bonjour !
    ---
    Bonjour !
    ---
    fr> b = répéter

        AvantPy exception: RepeatFirstError

        Error found in file REPL on line 1.

        Dialect used: pyfr

        -->1: b = répéter

        The AvantPy répéter keyword can only be used to begin
        a new for or while loop.


Existing dialects
------------------

Dialects definitions for language ``xx`` are Python files
named ``pyxx.py`` and are found in the AvantPy's repository:
`avantpy/dialects/ directory <https://github.com/aroberge/avantpy/tree/master/avantpy/dialects>`_.

Currently, a **DRAFT** implementation of the following dialects exist:

- `English <https://github.com/aroberge/avantpy/tree/master/avantpy/dialects/pyen.py>`_
- `French <https://github.com/aroberge/avantpy/tree/master/avantpy/dialects/pyfr.py>`_
- `Spanish <https://github.com/aroberge/avantpy/tree/master/avantpy/dialects/pyes.py>`_

In addition to the additional keywords needed for the special idioms used in AvantPy,
and explained later in this documentation, the English dialect includes the
keyword ``function`` as being equivalent to ``lambda``, and ``ask`` as being
equivalent to ``input``.


Finally, an
`UPPERCASE version <https://github.com/aroberge/avantpy/tree/master/avantpy/dialects/pyupper.py>`_
of AvantPy's English dialect exists; this is primarily intended to be used as a template
for other dialects, and for testing.

Existing languages
------------------

Language translations files for language ``xx`` are Python files
named ``xx.py`` and are found in the AvantPy's repository:
`avantpy/translations/ directory <https://github.com/aroberge/avantpy/tree/master/avantpy/translations>`_.

Currently, a **DRAFT** implementation of the following translations exist:

- `English translations <https://github.com/aroberge/avantpy/tree/master/avantpy/translations/en.py>`_
- `French translations <https://github.com/aroberge/avantpy/tree/master/avantpy/translations/fr.py>`_
- `English UPPERCASE version <https://github.com/aroberge/avantpy/tree/master/avantpy/translations/pyupper.py>`_ is primarily intended to be used as a template
  for other languages, and for testing.
