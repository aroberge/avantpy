Notes on translations - using gettext
=====================================

.. important::

    There are many sites that explain how to use gettext. However, I found
    that, no matter what individual explanation I read, it was either
    incomplete, too specific, or otherwise glossing over some minor point
    that was important for my project.

    I wrote these notes mostly for myself, but they may be useful for
    you as well.


What is gettext?
----------------

gettext is basically a standardized way of internationalization (i18n)
and localization (l10n) of computer programs.

What this means for this project, is the translation of strings shown
to the user in their preferred language.


Structure of this project
-------------------------

Below, I make references to various files. Here's a simplified view of the
directory structure of this project, showing some relevant files::

    avantpy/
        avantpy/
            locales/
                en/
                    LC_MESSAGES/
                        en.mo
                        en.po
                fr/
                    LC_MESSAGES/
                        fr.mo
                        fr.po
                messages.pot
            exception_handling.py
            make_pot.bat
            sessions.py
        docs/
        tests/
        setup.py

If you look at the repository on Github (or cloned locally), you will not
see the file ``make_pot.bat``.
I'll explain its role below.


How to use gettext
--------------------

Suppose we want to greet a user in their own language. For example,
in English we might have the following::

    print("Hello {name}".format(name=username))

while in French, we might have::

    print("Bonjour {name}".format(name=username))

The first thing to do would normally be to choose one of these forms as
our standard to be used as the reference for translation. I actually
prefer to use a slight variation where some words are written in uppercase
letter to make it more obvious to see if a translation is missing.
(More on this below.)

To indicate that a string needs to be translated, the common way is to
surround it by a function call, using ``_`` as the function name::

    print(  _( "HELLO {name}" )  .format(name=username)  )

    # extra spaces above added for clarity

Next, we need to create a "template" file for translations.
I use ``pygettext.py`` included as a **tool** with Python.
It is very likely not on the normal path where it can be found by Python.
If you don't know where your python files are located, you can use
Python's REPL and do the following::

    >>> import pydoc
    >>> print(pydoc.__file__)
    C:\Users\andre\AppData\Local\Programs\Python\Python37\lib\pydoc.py

You can then navigate to the directory containing the Python version
you are using. Instead of the ``lib`` subdirectory, you will almost certainly
find ``pygettext.py`` under the ``tools\i18n`` subdirectory.

``pygettext`` will extract all the strings surronded by ``_( )`` in the
input file you specify and create a "template" file (identified by a ``.pot``
extension). To make my life easier, I simply type ``make_pot`` at the prompt
which executes the content of ``make_pot.bat`` (I'm using Windows)::

    python c:\users\andre\appdata\local\programs\python\python37\tools\i18n\pygettext.py -p locales *.py


- ``make_pot.bat`` is located in the same directory where the Python source files
  containing strings to be translated is located.
- I use ``python filename.py`` instead of simply ``filename.py`` as I set my
  computer default to open ``.py`` files with my preferred editor instead of
  executing them.
- The ``-p locales`` option specifies that the template file is going to be
  created (or updated) in the ``locales/`` directory
  (see above for the directory structure).
- Since I did not specify a name to be used for the template file, the default
  ``messages.pot`` will be used (again, see above).
- The source files scanned by pygettext (``*.py``) will be all the
  Python files in that directory.

There's more to be done; let's break this up into a few additional
sections.

Using Poedit
-------------

In principle, template files can be edited with any standard text editor
to create "portable object" (``.po``) files from a template file.
However, this is more easily done using
`Poedit <https://poedit.net/>`_ which is a free program especially designed
for this task.

With Poedit, you have the choice of either creating a new translation
from a ``.pot`` file, or from a ``.po`` file. Open the relevant file,
choose a language, and start translating the various strings.

If you are updating an existing translation, open the ``.po`` file
and use Poedit's "Catalog" menu (fourth at the top of the menu
bar) to first update the source (``messages.pot``) from which the
``.po`` file is derived.

Poedit gives the choice to translate for specific regions (e.g. fr_CA for
French used in Canada). For this project, I prefer to choose a generic
two-letter code (fr) as it is assumed to be the case in various places.

.. warning::

    If, for a given language, you absolutely need different language
    translations, specific to a region, please file an issue
    first so that this can be discussed and the impact on the rest of
    the code can be properly evaluated.

    One of the goals of this project is to provide easier to understand
    tracebacks than those provided by Python. These do not need to be
    absolutely perfect.

When it comes time to save the ``.po`` file, use a similar structure
as that shown above and save
it in the ``LC_MESSAGES`` directory of the appropriate language.
Note that Poedit will automatically save another file with
a ``.mo`` extension; this is a "machine object" file that will actually
be used by your program.

In addition to strings to be translated, ``.po`` files contain some
information about who translated the file and some copyright information.
In general, you might want to fill in the appropriate information.
Note that Poedit allows you to set your personal information (name
and email address) which will be automatically used, so that you don't
have to edit the created file by hand.

.. warning::

    Do not contribute translations to AvantPy where you attribute the
    copyright to yourself. Either do not include any copyright information
    (which is what I have done) or attribute it to the AvantPy project.

Telling Python to use the translations
--------------------------------------

In this project, the language selection is done in the file ``session.py``.
(See directory structure above.)
This file needs to be imported in any module where a translated string
appears. (See for example ``exception_handling.py``.)
At the top of ``sessions.py``, ``gettext`` is imported.  Changing language
is done using the ``set_lang`` method; the relevant parts are as follows::

    def set_lang(self, lang):
        gettext_lang = gettext.translation(
            "messages",  # 1
            localedir=os.path.normpath(
                os.path.join(os.path.dirname(__file__), "locales")  # 2
            ),
            languages=[lang],
            fallback=True,  # 3
        )
        gettext_lang.install()  # 4

Here is an explanation for the numbered comments above:

    1. Indicates that translations will be found in files named "messages.mo"

    2. "Foolproof" way of locating the translation directory

    3. By default, fallback is ``False``. If the default is used and a request
       is made to use a non-existing translation, an exception is raised.
       By using ``fallback=True``, the untranslated string (as it exists in
       the source file) is used instead.  By using at least some UPPERCASE
       words, the messages is still readable (in English) while giving us
       a clue that a translation is missing.

    4. This adds the function named ``_`` to the builtins. So, it will be known
       to any module that imports ``session.py``.  ``install`` takes an
       optional argument which makes it possible to use different behaviour.
       By using the default, we do not provide any support for dealing with
       alternative translations based on quantity (singular/plural).


.. warning::

    When using flake8 (or likely other similar linters), ``_`` will be flagged
    as an unknown function.  This is taken care of in this project by adding::

        builtins =
            _

    to the ``.flake8`` configuration file.


.. warning::

    Every language has its own way to deal (or not) with plural forms of words.
    As mentioned, in principle, ``gettext`` offers a way to handle with the language specific complexities.
    In practice for this project, we assume a single form to be used.


Why are .mo files in the repository
-----------------------------------

When configuring the project, the automatically generated ``.gitignore`` file
include exclusion for ``.pot`` and ``.mo`` files.
The rationale is that these files are automatically generated (by some standard
programs) and it is generally suggested that such files not be included.

However, in this case, we want these files to be available to end users.
If someone clones the project, and needs to upload a version somewhere (e.g. pypi.org),
these generated files (at least the ``.mo`` files) need to be included.
