
Friendly error messages - en Français
======================================

Un des buts d'AvantPy est de fournir des rétroactions plus conviviales
que les fameux *tracebacks* de Python lorsqu'une exception survient.
Ci-dessous, on peut voir quelques exemples. Le but éventuel est de
documenter ici tous les exemples possibles tels qu'interprétés par AvantPy.

.. note::

     Le contenu de cette page a été généré par l'exécution de
     tb_pyfr.py situé dans le répertoire ``tests/pyfr/``.
     Ceci a besoin d'être fait de manière explicite lorsqu'on veut
     faire des corrections ou des ajouts, avant de faire la mise
     à jour du reste de la documentation avec Sphinx.


AvantPy, version 0.0.8;
Python, version 3.7.0



IfNobreakError
--------------

Exemple::


    Exception AvantPy : IfNobreakError

    Erreur trouvée dans le fichier 'raise_if_nobreak.pyfr' à la ligne 4.

    Dialecte utilisé : pyfr

       2: si Vrai:
       3:     passer
    -->4: pasinterrompu:

    Le mot-clé pasinterrompu spécifique à Avantpy ne peut pas être utilisé
    dans un énoncé si/sinonsi/sinon (Python: if/elif/else).


MismatchedBracketsError
-----------------------

Exemple::


    Exception AvantPy : MismatchedBracketsError

    Erreur trouvée dans le fichier 'raise_mismatched_brackets.pyfr' aux lignes [2 - 6].

    Dialecte utilisé : pyfr

    -->2: a = (1,
       3:     2,
       4:     3, 4,
       5:     5
    -->6: ]

    Le symbole gauche ( ne correspond pas au symbole droit ].


MissingLeftBracketError
-----------------------

Exemple::


    Exception AvantPy : MissingLeftBracketError

    Erreur trouvée dans le fichier 'raise_missing_left_bracket.pyfr' à la ligne 5.

    Dialecte utilisé : pyfr

       4:     3, 4,)
    -->5:     )
       6: b = 3

    Le symbole droit ) n'a pas de symbole gauche correspondant.


MissingRepeatError
------------------

Exemple::


    Exception AvantPy : MissingRepeatError

    Erreur trouvée dans le fichier 'raise_missing_repeat.pyfr' à la ligne 3.

    Dialecte utilisé: pyfr

       2: x = 0
    -->3: jusquà x == 2:
       4:     x += 1

    Le mot-clé jusquà spécifique à Avantpy peut seulement être utilisé
    s'il est précédé de 'répéter'.


Exemple 2::

    Exception AvantPy : MissingRepeatError

    Erreur trouvée dans le fichier 'raise_missing_repeat2.pyfr' à la ligne 3.

    Dialecte utilisé: pyfr

       2: x = 0
    -->3: sansfin:
       4:     x += 1

    Le mot-clé sansfin spécifique à Avantpy peut seulement être utilisé
    s'il est précédé de 'répéter'.


NameError
---------

Exemple::


    Exception Python : NameError: name 'c' is not defined

    Erreur trouvée dans le fichier '' à la ligne 4.

    Dialecte utilisé : pyfr

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

Exemple::


    Exception AvantPy : NobreakFirstError

    Erreur trouvée dans le fichier 'raise_nobreak_first.pyfr' à la ligne 3.

    Dialecte utilisé : pyfr

       2: # Need to prevent pasinterrompu being replaced by 'else' in this situation.
    -->3: a = 1 if True pasinterrompu 3
       4: 

    Le mot-clé pasinterrompu spécifique à Avantpy peut seulement être utilisé
    au lieu de sinon (Python: else) lorsqu'il débute un nouvel énoncé
    dans des boucles 'pour' ou 'tantque' (Python: for/while).


NobreakSyntaxError
------------------

Exemple::


    Exception AvantPy : IfNobreakError

    Erreur trouvée dans le fichier 'raise_nobreak_syntax.pyfr' à la ligne 4.

    Dialecte utilisé : pyfr

       3: a = 1
    -->4: pasinterrompu: pass
       5: 

    Le mot-clé pasinterrompu spécifique à Avantpy peut seulement être utilisé
    au lieu de sinon (Python: else) lorsqu'il débute un nouvel énoncé
    dans des boucles 'pour' ou 'tantque' (Python: for/while).


RepeatFirstError
----------------

Exemple::


    Exception AvantPy : RepeatFirstError

    Erreur trouvée dans le fichier 'raise_repeat_first.pyfr' à la ligne 3.

    Dialecte utilisé : pyfr

       2: # Catch an early case of using répéter not to begin a loop
    -->3: a = répéter
       4: 

    Le mot-clé répéter spécifique à Avantpy peut seulement être utilisé
    pour débuter une nouvelle boucle 'pour' ou 'tantque'
    (équivalent Python: 'for' ou 'while').


TryNobreakError
---------------

Exemple::


    Exception AvantPy : TryNobreakError

    Erreur trouvée dans le fichier 'raise_try_nobreak.pyfr' à la ligne 7.

    Dialecte utilisé : pyfr

       3:     essayer:
       4:         A = 1
       5:     siexception:
       6:         A = 2
    -->7:     pasinterrompu:

    Le mot-clé pasinterrompu spécifique à Avantpy ne peut pas être utilisé dans
    un énoncé essayer/siexception/sinon/finalement (Python: try/except/else/finally).


UnknownLanguageError
--------------------

Exemple::


    Exception AvantPy : UnknownLanguageError

    Le langage inconnu suivant a été demandé : xx.

    Les langages connus sont : {'en', 'fr'}.


UnknownDialectError
-------------------

Exemple::


    Exception AvantPy : UnknownDialectError

    Le dialecte inconnu suivant a été demandé : pyxx.

    Les dialectes connus sont : ['pyen', 'pyes', 'pyfr', 'pyupper'].

