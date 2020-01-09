# AvantPy

Python with **training wheels**: _executable pseudocode_ in any language.

:warning: On April 7th, I decided decided to carve out the part of this project dealing with
simplified tracebacks into a project of its own. **For the next few weeks, I will temporarily
stop working on AvantPy.** Work will resume when "friendly-traceback" is substantially complete.

Those interested should go to https://aroberge.github.io/friendly-traceback-docs/docs/html/index.html  (Code at: https://github.com/aroberge/friendly-traceback)

Please see https://aroberge.github.io/avantpy/docs/html/ for more information, including for those
who wish to contribute or file issues.
AvantPy uses Black.
![Black logo](https://img.shields.io/badge/code%20style-black-000000.svg)

## What is AvantPy

- AvantPy is a collection of dialects, each dialect being a superset of Python, designed to make it easier to learn programming concepts in a given human language.
  - Each dialect consists of a translations of most Python keywords in a given human language, supplemented by a few additional constructs intended to make some programming concepts easier to learn.
  - The current version includes three dialects: English, French and Spanish.
  The translation currently done is subject to change; feel free to make suggestions for alternative to use.
- AvantPy is a preprocessor, that takes a program written either totally or
in parts in a given dialect, and converts it to standard Python prior to execution.
  - A syntactically valid program can include a mix of code written in normal Python and in a specific dialect. This is to ease the transition to learning Python.
- AvantPy is written as a standard Python module/package meant to be usable with any "normal" Python environment. Thus, it could be included as a plugin for a given
editor, or run with a standard Python interpreter from the command line.
- AvantPy also includes a tool to convert programs written in a given dialect into standard Python, showing the differences between the two, thus helping motivated users to make the transition to using only standard Python.
- AvantPy also includes a custom REPL that can use any of the existing dialects.

AvantPy uses [Friendly-traceback](https://aroberge.github.io/friendly-traceback-docs/docs/html/) to process Python tracebacks and translate them into easier to understand feedback for beginners.

## Who is it for

The main target audience is composed of students who do not know English and are learning programming for the first time, under the guidance of an
instructor.

## Why

More details to be added, but in the meantime, [read this](http://pgbovine.net/non-native-english-speakers-learning-programming-paper.htm)

## Executable pseudocode

Python is often described as executable pseudocode. Once people have learned a few idiomatic expressions, like `for variable in range(n)`, translating pseudocode written in English into Python is usually very straightforward.

If the pseudocode is not written in English, the translation process is, at least initially, not as straightforward since an additional mental step is required by the translation from the original language into Python's English.

Even though the number of Python keywords is small, for absolute beginners who are learning programming concepts (control flow structures, defining functions, etc.), being able to use a language that uses keywords easily understood in their own language can definitely facilitate the learning process.
**This is the approach taken by people using block-based environment
(Scratch, Blockly, etc.) developed by educational experts
to help students learn programming concepts.**

Realistically, many students who learn computer programming as part of a formal course might never use programming again or, if so, it might not be for many years. Given enough time, they would likely forget most of the programming syntax they had learned.
However they likely would retain programming **concepts** better if they are first learning them in their natural language.

## What is meant by training wheels

To help beginners learning how to ride a bicycle, one sometimes uses [training wheels](https://en.wikipedia.org/wiki/Training_wheels). After a while, the new cyclists ride
their bicycles without the training wheels needing to touch the ground to offer
additional support. This is similar to what AvantPy aims to do for learning Python.

Imagine that I am a French speaker that learns to program using AvantPy.
My first program might be:

```py
imprime("Bonjour !")
```

A while later, I might write a program like the following:

```py
si commande == 'q'
   imprime("Au revoir !")
```

When I would try to execute such a program, I would get the following error message:

```txt
Il y a une erreur de syntaxe dans ce programme dans la ligne contenant le code suivant:

    si commande == 'q'

Une instruction débutant avec le mot "si" doit terminer par deux points (:).
[Voir documentation-si.]
```

The equivalent English version would be

```txt
There is a syntax error in this program at the line containing the following code:

    if commande == 'q'

A statement beginning with the word "if" must end with a colon (:).
[Relevant link to the documentation on "if" provided here.]
```

Eventually, I might want to learn some "true" Python code.
Along the way, I would make use of a tool provided to show me the
true Python code corresponding to the code written in my given dialect:

```py
if commande == 'q':        # si commande == 'q':
    print("Au revoir !")   #     imprime("Au revoir !")
```

and feel ready to leave AvantPy and only write Python.


## Code of Conduct

We completely support the [Python Community Code of Conduct](https://www.python.org/psf/codeofconduct/)
Contributors to this project are expected to do the same.
