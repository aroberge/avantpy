
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
Python version: 3.7.3



IfNobreakError
--------------

.. code-block:: none


    Erreur de syntaxe AvantPy :
        IfNobreakError: Keyword nobreak found matching if/elif
        
    Le mot-clé 'pasinterrompu' spécifique à Avantpy ne peut pas être utilisé
    dans un énoncé 'si/sinonsi/sinon' (Python: if/elif/else).
    
    
    Python peut seulement analyser le fichier '~\github\avantpy\tests\pyfr\raise_if_nobreak.pyfr'
    jusqu'à l'endroit indiqué par --> et ^.
    
       1: '''Should raise IfNobreakError'''
       2: si Vrai:
       3:     passer
    -->4: pasinterrompu:
          ^

MismatchedBracketsError
-----------------------

.. code-block:: none


    Erreur de syntaxe AvantPy :
        MismatchedBracketsError: Closing bracket found matching a different opening one.
        
    Le symbole gauche ( ne correspond pas au symbole droit ].
    
    
    Python peut seulement analyser le fichier '~\github\avantpy\tests\pyfr\raise_mismatched_brackets.pyfr'
    jusqu'à l'endroit indiqué par --> et ^.
    
       3:     2,
       4:     3, 4,
       5:     5
    -->6: ]
          ^

MissingLeftBracketError
-----------------------

.. code-block:: none


    Erreur de syntaxe AvantPy :
        MissingLeftBracketError: Closing bracket found with no matching opening one
        
    Le symbole droit ) n'a pas de symbole gauche correspondant.
    
    Python peut seulement analyser le fichier '~\github\avantpy\tests\pyfr\raise_missing_left_bracket.pyfr'
    jusqu'à l'endroit indiqué par --> et ^.
    
       2: a = (1,
       3:     2,
       4:     3, 4,)
    -->5:     )
          ^

MissingRepeatColonError
-----------------------

.. code-block:: none


    Erreur de syntaxe AvantPy :
        MissingRepeatColonError: Missing colon on line beginning with repeat
        
    Un énoncé débutant avec le mot clé 'répéter' spécifique à Avantpy
    doit être sur une seule ligne terminant avec deux points (:) qui indiquent
    le début d'un bloc de code de code indenté, sans qu'il n'y ait
    d'autre deux points qui apparaissent sur cette ligne.
    
    Python peut seulement analyser le fichier '~\github\avantpy\tests\pyfr\raise_missing_repeat_colon.pyfr'
    jusqu'à l'endroit indiqué par --> et ^.
    
       1: '''Should raise MissingRepeatColonError'''
       2: x = 0
    -->3: répéter jusquà (x ==
          ^

MissingRepeatError
------------------

.. code-block:: none


    Erreur de syntaxe AvantPy :
        MissingRepeatError: until and forever must be preceeded by repeat
        
    Le mot-clé 'jusquà' spécifique à Avantpy peut seulement être utilisé
    s'il est précédé de 'répéter'.
    
    
    Python peut seulement analyser le fichier '~\github\avantpy\tests\pyfr\raise_missing_repeat.pyfr'
    jusqu'à l'endroit indiqué par --> et ^.
    
       1: '''Should raise MissingRepeatError'''
       2: x = 0
    -->3: jusquà x == 2:
          ^

NameError
---------

.. code-block:: none


    Exception Python:
        NameError: name 'c' is not defined
        
    Une exception NameError indique que le nom d'une variable
    ou d'une fonction n'est pas connue par Python.
    Habituellement, ceci indique une simple faute d'orthographe.
    Cependant, cela peut également indiquer que le nom a été
    utilisé avant qu'on ne lui ait associé une valeur.
    
    Cause probable :
        Dans votre programme, le nom inconnu est 'c'.
        
    L'exécution s'est arrêtée à la ligne 115 du fichier '~\github\avantpy\avantpy\import_hook.py'
    
       113: 
       114:         try:
    -->115:             exec(source, vars(module))
       116:         except Exception:

    source: '"""Should raise NameError"""\n\na = 1\nb = c...'  | len(source): 48
    module: <module 'raise_name_error' from 'C:\\Users\\a...>

    Exception levée à la ligne du fichier '<string>'.
    
Malheureusement, aucune information supplémentaire n’est disponible:
le contenu du fichier '<string>' n’est pas accessible.

NobreakFirstError
-----------------

.. code-block:: none


    Erreur de syntaxe AvantPy :
        NobreakFirstError: nobreak must be first statement on a line
        
    Le mot-clé 'pasinterrompu' spécifique à Avantpy peut seulement être utilisé
    au lieu de sinon (Python: else) lorsqu'il débute un nouvel énoncé
    dans des boucles 'pour' ou 'tantque' (Python: for/while).
    
    
    Python peut seulement analyser le fichier '~\github\avantpy\tests\pyfr\raise_nobreak_first.pyfr'
    jusqu'à l'endroit indiqué par --> et ^.
    
       1: '''Should raise NobreakFirstError'''
       2: # Need to prevent pasinterrompu being replaced by 'else' in this situation.
    -->3: a = 1 if True pasinterrompu 3
          ^

NobreakSyntaxError
------------------

.. code-block:: none


    Erreur de syntaxe AvantPy :
        NobreakSyntaxError: Keyword nobreak not matching a valid block
        
    Le mot-clé 'pasinterrompu' spécifique à Avantpy peut seulement être utilisé
    au lieu de 'sinon' (Python: else) lorsqu'il débute un nouvel énoncé
    dans des boucles 'pour' ou 'tantque' (Python: for/while).
    
    
    Python peut seulement analyser le fichier '~\github\avantpy\tests\pyfr\raise_nobreak_syntax.pyfr'
    jusqu'à l'endroit indiqué par --> et ^.
    
       1: '''Should raise NobreakSyntaxError'''
       2: # Need to prevent pasinterrompu being replaced by 'else' in this situation.
       3: a = 1
    -->4: pasinterrompu: pass
          ^

RepeatFirstError
----------------

.. code-block:: none


    Erreur de syntaxe AvantPy :
        RepeatFirstError: repeat must be first statement on a line
        
    Le mot-clé 'répéter' spécifique à Avantpy peut seulement être utilisé
    pour débuter une nouvelle boucle
    (équivalent Python: 'for' ou 'while').
    
    
    Python peut seulement analyser le fichier '~\github\avantpy\tests\pyfr\raise_repeat_first.pyfr'
    jusqu'à l'endroit indiqué par --> et ^.
    
       1: '''Should raise RepeatFirstError'''
       2: # Catch an early case of using répéter not to begin a loop
    -->3: a = répéter
          ^

TryNobreakError
---------------

.. code-block:: none


    Erreur de syntaxe AvantPy :
        TryNobreakError: Keyword nobreak found matching try/except
        
    Le mot-clé 'pasinterrompu' spécifique à Avantpy ne peut pas être utilisé dans
    un énoncé 'essayer/siexception/sinon/finalement' (Python: try/except/else/finally).
    
    Python peut seulement analyser le fichier '~\github\avantpy\tests\pyfr\raise_try_nobreak.pyfr'
    jusqu'à l'endroit indiqué par --> et ^.
    
        4:         A = 1
        5:     siexception:
        6:         A = 2
    --> 7:     pasinterrompu:
           ^

UnknownDialectError
-------------------

.. code-block:: none


    Exception AvantPy:
        UnknownDialectError: Unknown dialect pyxx
        
    Le dialecte inconnu suivant a été demandé : pyxx.
    
    Les dialectes connus sont : ['pyen', 'pyes', 'pyfr', 'pyupper'].
    
    
    L'exécution s'est arrêtée à la ligne 115 du fichier '~\github\avantpy\avantpy\import_hook.py'
    
       113: 
       114:         try:
    -->115:             exec(source, vars(module))
       116:         except Exception:

    source: '\'\'\'Raises UnknownDialectError\'\'\'\nimpo...'  | len(source): 282
    module: <module 'raise_unknown_dialect' from 'C:\\Use...>

    Exception levée à la ligne du fichier '~\github\avantpy\avantpy\session.py'.
    
       110:         if not self.is_dialect(dialect):
       111:             raise exceptions.UnknownDialectError(
    -->112:                 "Unknown dialect %s" % dialect, (dialect, self.all_dialects())
       113:             )

    dialect: 'pyxx'
    dialect: 'pyxx'
    self: <avantpy.session._State object at 0x032D6030>

UnknownLanguageError
--------------------

.. code-block:: none


    Exception AvantPy:
        UnknownLanguageError: Unknown language xx
        
    Le langage inconnu suivant a été demandé : xx.
    
    Les langages connus sont : {'fr', 'en'}.
    
    
    L'exécution s'est arrêtée à la ligne 115 du fichier '~\github\avantpy\avantpy\import_hook.py'
    
       113: 
       114:         try:
    -->115:             exec(source, vars(module))
       116:         except Exception:

    source: '\'\'\'Raises UnknownLanguageError\'\'\'\nimp...'  | len(source): 278
    module: <module 'raise_unknown_language' from 'C:\\Us...>

    Exception levée à la ligne du fichier '~\github\avantpy\avantpy\session.py'.
    
       135:         if not self.is_lang(lang):
       136:             raise exceptions.UnknownLanguageError(
    -->137:                 "Unknown language %s" % lang, (lang, self.languages)
       138:             )

    lang: 'xx'
    lang: 'xx'
    self: <avantpy.session._State object at 0x032D6030>
