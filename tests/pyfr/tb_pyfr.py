"""Creates a version of traceback.rst to insert in the documentation.

This assumes that such a file already exist; this is only done to
ensure we have the right destination. If so, we actually rewrite it.

"""

import os
import sys
import platform
from contextlib import redirect_stdout


# Make it possible to find avantpy and docs source
this_dir = os.path.dirname(__file__)
root_dir = os.path.abspath(os.path.join(this_dir, "..", ".."))
sys.path.insert(0, this_dir)
sys.path.insert(0, root_dir)


import avantpy  # sets up import hook

# Require that a version already exists - to confirm we are at the right location
target = os.path.normpath(os.path.join(root_dir, "docs/source/tracebacks_fr.rst"))


try:
    assert os.path.isfile(target)
except AssertionError:
    print("Wrong path: {} does not exist.".format(target))
    sys.exit()


content = """
Friendly error messages - en Français
======================================

Un des buts d'AvantPy est de fournir des rétroactions plus conviviales
que les fameux *tracebacks* de Python lorsqu'une exception survient.
Ci-dessous, on peut voir quelques exemples. Le but éventuel est de
documenter ici tous les exemples possibles tels qu'interprétés par AvantPy.

.. note::

     Le contenu de cette page a été généré par l'exécution de
     {name} situé dans le répertoire ``tests/pyfr/``.
     Ceci a besoin d'être fait de manière explicite lorsqu'on veut
     faire des corrections ou des ajouts, avant de faire la mise
     à jour du reste de la documentation avec Sphinx.


AvantPy, version {avantpy}
Python, version {python}

""".format(
    avantpy=avantpy.version.__version__, python=platform.python_version(), name=__file__
)


def make_title(text):
    print()
    print(text)
    print("-" * len(text), "\n")
    print("Example::\n")


def create_tracebacks():
    with open(target, "w", encoding="utf8") as out:
        with redirect_stdout(out):
            print(content)

            make_title("IfNobreakError")
            import raise_if_nobreak

            make_title("MismatchedBracketsError")
            import raise_mismatched_brackets

            make_title("MissingLeftBracketError")
            import raise_missing_left_bracket

            make_title("MissingRepeatError")
            import raise_missing_repeat

            print("\nExample 2::")
            import raise_missing_repeat2

            make_title("NobreakFirstError")
            import raise_nobreak_first

            make_title("NobreakSyntaxError")
            import raise_nobreak_syntax

            make_title("RepeatFirstError")
            import raise_repeat_first

            make_title("TryNobreakError")
            import raise_try_nobreak

            make_title("UnknownLanguageError")
            import raise_unknown_language

            make_title("UnknownDialectError")
            import raise_unknown_dialect

            make_title("UnexpectedError")
            print("    No example found yet.\n")


try:
    create_tracebacks()
except ImportError:
    print("ImportError: please try running this program from it location using")
    print("             python tb_pyupper.py")
