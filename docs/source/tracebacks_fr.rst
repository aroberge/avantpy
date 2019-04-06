
Friendly error messages - en Français
======================================

Un des buts d'AvantPy est de fournir des rétroactions plus conviviales
que les fameux *tracebacks* de Python lorsqu'une exception survient.
Ci-dessous, on peut voir quelques exemples. Le but éventuel est de
documenter ici tous les exemples possibles tels qu'interprétés par AvantPy.

.. note::

     Le contenu de cette page a été généré par l'exécution de
     tb_pyfr.py situé dans le répertoire ``tests/``.
     Ceci a besoin d'être fait de manière explicite lorsqu'on veut
     faire des corrections ou des ajouts, avant de faire la mise
     à jour du reste de la documentation avec Sphinx.

AvantPy version: 0.0.9
Python version: 3.7.0



IfNobreakError
--------------

Example::

    AvantPy exception: IfNobreakError

    Error found in file 'raise_if_nobreak.pyfr' on line 4.

    Dialect used: pyfr

       2: si Vrai:
       3:     passer
    -->4: pasinterrompu:

    Le mot-clé 'pasinterrompu' spécifique à Avantpy ne peut pas être utilisé
    dans un énoncé 'si/sinonsi/sinon' (Python: if/elif/else).


IndentationError: expected an indented block
--------------------------------------------

Example::

    Python exception: 
        IndentationError: expected an indented block

    Error found in file 'raise_indentation_error1.pyfr' on line 3.

    Dialect used: pyfr

       1: '''Should raise IndentationError'''
       2: si Vrai:
    -->3: passer
       4: 

    Une erreur d'indentation a lieu lorsqu'une ligne de code
    n'est pas indentée (alignée verticalement) tel qu'attendu.
    Dans ce cas-ci, la ligne indiquée par une flèche devrait
    normalement commencer un nouveau bloc de code indenté.


IndentationError: unexpected indent
-----------------------------------

Example::

    Python exception: 
        IndentationError: unexpected indent

    Error found in file 'raise_indentation_error2.pyfr' on line 4.

    Dialect used: pyfr

       1: '''Should raise IndentationError'''
       2: si Vrai:
       3:     passer
    -->4:       passer
       5: 

    Une erreur d'indentation a lieu lorsqu'une ligne de code
    n'est pas indentée (alignée verticalement) tel qu'attendu.
    Dans ce cas-ci, la ligne indiquée par une flèche
    est plus indentée que ce qui était attendu et ne
    correspond pas à l'indentation de la ligne précédente.


IndentationError - no match
---------------------------

Example::

    Python exception: 
        IndentationError: unindent does not match any outer indentation level

    Error found in file 'raise_indentation_error3.pyfr' on line 4.

    Dialect used: pyfr

       1: '''Should raise IndentationError'''
       2: si Vrai:
       3:       passer
    -->4:     passer
       5: 

    Une erreur d'indentation a lieu lorsqu'une ligne de code
    n'est pas indentée (alignée verticalement) tel qu'attendu.
    Dans ce cas-ci, la ligne indiquée par une flèche
    est moins indentée que la ligne précédente,
    et n'est pas alignée verticalement avec un autre bloc de code.


MismatchedBracketsError
-----------------------

Example::

    AvantPy exception: MismatchedBracketsError

    Error found in file 'raise_mismatched_brackets.pyfr' on line 6.

    Dialect used: pyfr

    -->2: a = (1,
       3:     2,
       4:     3, 4,
       5:     5
    -->6: ]

    Le symbole gauche ( ne correspond pas au symbole droit ].


MissingLeftBracketError
-----------------------

Example::

    AvantPy exception: MissingLeftBracketError

    Error found in file 'raise_missing_left_bracket.pyfr' on line 5.

    Dialect used: pyfr

       4:     3, 4,)
    -->5:     )
       6: b = 3

    Le symbole droit ) n'a pas de symbole gauche correspondant.


MissingRepeatColonError
-----------------------

Example::

    AvantPy exception: MissingRepeatColonError

    Error found in file 'raise_missing_repeat_colon.pyfr' on line 3.

    Dialect used: pyfr

       2: x = 0
    -->3: répéter jusquà (x ==
       4:          1):

    Un énoncé débutant avec le mot clé 'répéter' spécifique à Avantpy
    doit être sur une seule ligne terminant avec deux points (:) qui indiquent
    le début d'un bloc de code de code indenté, sans qu'il n'y ait
    d'autre deux points qui apparaissent sur cette ligne.


MissingRepeatError
------------------

Example::

    AvantPy exception: MissingRepeatError

    Error found in file 'raise_missing_repeat.pyfr' on line 3.

    Dialect used: pyfr

       2: x = 0
    -->3: jusquà x == 2:
       4:     x += 1

    Le mot-clé 'jusquà' spécifique à Avantpy peut seulement être utilisé
    s'il est précédé de 'répéter'.


NameError
---------

Example::

    Python exception: 
        NameError: name 'c' is not defined

    Error found in file 'raise_name_error.pyfr' on line 4.

    Dialect used: pyfr

       3: a = 1
    -->4: b = c
       5: d = 3

    Une exception de type NameError indique que le nom d'une variable
    ou d'une fonction utilisée dans votre programme est inconnu par Python.
    Le plus souvent, ceci se produit parce que vous faites une faute
    d'orthographe dans l'écriture de votre variable ou de votre fonction;
    ceci peut également se produire si vous invoquez cette fonction ou utilisez
    cette variable sans l'avoir définie auparavant.
    Dans votre programme, le nom inconnu est 'c'.


NobreakFirstError
-----------------

Example::

    AvantPy exception: NobreakFirstError

    Error found in file 'raise_nobreak_first.pyfr' on line 3.

    Dialect used: pyfr

       2: # Need to prevent pasinterrompu being replaced by 'else' in this situation.
    -->3: a = 1 if True pasinterrompu 3
       4: 

    Le mot-clé 'pasinterrompu' spécifique à Avantpy peut seulement être utilisé
    au lieu de sinon (Python: else) lorsqu'il débute un nouvel énoncé
    dans des boucles 'pour' ou 'tantque' (Python: for/while).


NobreakSyntaxError
------------------

Example::

    AvantPy exception: NobreakSyntaxError

    Error found in file 'raise_nobreak_syntax.pyfr' on line 4.

    Dialect used: pyfr

       3: a = 1
    -->4: pasinterrompu: pass
       5: 

    Le mot-clé 'pasinterrompu' spécifique à Avantpy peut seulement être utilisé
    au lieu de 'sinon' (Python: else) lorsqu'il débute un nouvel énoncé
    dans des boucles 'pour' ou 'tantque' (Python: for/while).


RepeatFirstError
----------------

Example::

    AvantPy exception: RepeatFirstError

    Error found in file 'raise_repeat_first.pyfr' on line 3.

    Dialect used: pyfr

       2: # Catch an early case of using répéter not to begin a loop
    -->3: a = répéter
       4: 

    Le mot-clé 'répéter' spécifique à Avantpy peut seulement être utilisé
    pour débuter une nouvelle boucle
    (équivalent Python: 'for' ou 'while').


TryNobreakError
---------------

Example::

    AvantPy exception: TryNobreakError

    Error found in file 'raise_try_nobreak.pyfr' on line 7.

    Dialect used: pyfr

       3:     essayer:
       4:         A = 1
       5:     siexception:
       6:         A = 2
    -->7:     pasinterrompu:

    Le mot-clé 'pasinterrompu' spécifique à Avantpy ne peut pas être utilisé dans
    un énoncé 'essayer/siexception/sinon/finalement' (Python: try/except/else/finally).


UnknownDialectError
-------------------

Example::

    Exception AvantPy : UnknownDialectError

    Le dialecte inconnu suivant a été demandé : pyxx.

    Les dialectes connus sont : ['pyen', 'pyes', 'pyfr', 'pyupper'].


UnknownLanguageError
--------------------

Example::

    Exception AvantPy : UnknownLanguageError

    Le langage inconnu suivant a été demandé : xx.

    Les langages connus sont : {'fr', 'en'}.

