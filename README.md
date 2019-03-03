# AvantPy

Python with training wheels: executable pseudocode in any language.

## Who is it for

AvantPy is designed with two similar target audiences:

- Non English speaking beginners who are learning programming for the first time in a classroom environment.
  Realistically, many of such students will never use programming immediately afterwards, and would retain concepts better if they are learning them in their natural language.
- Beginning programmers who have only use block-based programming environments,
  such as [Scratch](https://scratch.mit.edu/) or
  [Blockly](https://blockly-games.appspot.com/),
  and wish to start using text-based programming environments.

## What is AvantPy

:warning: The following describes what the final version of AvantPy should look
like; currently, much remains to be implemented.

- AvantPy is a collection of dialects, each dialect being a superset of Python, designed to make it easier to learn programming concepts in a given human language.
  - Each dialect consists of a translations of most Python keywords in a given human language, supplemented by a few additional keywords intended to make some concepts easier to learn.
- AvantPy is a preprocessor, that takes a program written either totally or
in parts in a given dialect, and converts it to standard Python prior to execution.
  - A syntactically valid program can include a mix of code written in normal Python and in a specific dialect. This is to ease the transition to learning Python.
- AvantPy also includes tools to analyze Python tracebacks and translate them into easier to understand feedback for beginners.
- AvantPy is written as a standard Python module/package meant to be usable with any "normal" Python environment. Thus, it could be included as a plugin for a given
editor, or run with a standard Python interpreter from the command line.
- AvantPy also includes a tool to convert programs written in a given dialect into standard Python, showing the differences between the two, thus helping motivated users to make the transition to using only standard Python.
- AvantPy also includes a custom REPL.

## What is meant by training wheels

To help beginners learning how to ride a bicycle, one sometimes uses [training wheels](https://en.wikipedia.org/wiki/Training_wheels). After a while, the new cyclists ride
their bicycles without the training wheels needing to touch the ground to offer
additional support.

This is what avantpy aims to do for learning Python.

Imagine that I am a French speaker that learns to program using AvantPy.
My first program might be:

```py
imprime("Bonjour !")
```

A while later, I might write a program like the following:

```py
si x == 'q'
   imprime("Au revoir !")
```

When I would try to execute such a program, I would get the following error message:

```txt
Il y a une erreur de syntaxe dans ce programme dans la ligne contenant le code suivant:

    si x == 'q'

Une instruction débutant avec le mot "si" doit terminer par deux points (:).
[Voir documentation-si.]
```

The equivalent English version would be

```txt
There is a syntax error in this program at the line containing the following code:

    if x == 'q'

A statement beginning with the word "if" must end with a colon (:).
[Relevant link to the documentation on "if" provided here.]
```

Eventually, I might want to learn some "true" Python code.
I would make use of a tool provided to show me the true Python code corresponding
to the code written in my given dialect:

```py
if x == 'q':              # si x == 'q':
    print("Au revoir !")  #     imprime("Au revoir !")
```

and feel ready to leave AvantPy and only write Python.

## How to use it

_ To be written _
