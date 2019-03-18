Guiding principles
==================

AvantPy aims to be a project that facilitates learning computer programming while minimizing the pain. AvantPy will strive to make informed decisions about designs based on other successful programming language or environments, and from feedback from its users.


For students and instructors
-----------------------------

AvantPy aims to:

- make it possible for students to learn **basic** programming concepts in their own language;
- provide easy to understand basic error messages, simpler than Python tracebacks;
- reduce the number of non-obvious programming idioms, as compared with
  Python, such as when introducing ``repeat n``;
- allow for an easy transition to programming using standard Python.

In a given dialect, AvantPy keywords and functions should not be thought of as
straight translations from English of the Python keywords; instead, these should be
chosen so that they make sense in a programming context. For example, in the French dialect,
the function ``input`` is named ``demander`` which would normally be translated as ``ask``.
Similarly, the French equivalent to ``except`` is ``siexception``
which is composed of two words, ``si`` and  ``exception``.
Thus, ``siexception SyntaxError:`` can be read as ``if exception SyntaxError:``.

For contributors
-----------------

In addition to users that provide feedback, including bug reports and suggestions for improvements,
we can think of three other types of contributors.

A. Contributor of new language adaptation

As a concrete example, suppose somebody wishes to contribute the information required to create
a Russian dialect. Ideally, they should not need any special tools, nor any advanced knowledge
of programming. If they do know know English, but know another language supported by AvantPy,
they should be able to use that knowledge to easily create a new dialect.

To facilitate this, translation from one dialect into another should be doable by a
one-to-one keyword substitution. Such keywords might be essentially compound words
in a given language written in such a way that the language's grammar is not followed
**but** in a way that might nonetheless be relatively easy to understand by
beginners.

Translations of **messages** to user, such as simplified tracebacks, are currently implemented
(in theory - not much content yet) using a simple Python dictionary for each language,
instead of using a standard method such as that provided by pygettext.
This is possibly going to change in once the project's core functionality is completed
(probably around version 0.1).

B. Contributor of "core" code

Currently, the "core" code does not rely on any "advanced" knowledge of computer science.
Ideally, the code should be "easy" to understand and modified by a self-taught intermediate programmer - like the current author.

It is very likely that using more advanced programming techniques could speed up the transformations and error handling done by AvantPy;
however, speed of execution is not our ultimate goal:
AvantPy aims to be easy to use by beginners, and easy to contribute to by developers.

For third party software
------------------------

AvantPy does not aim to be a full programming environment; it adresses a different need
than editors or IDEs aimed at Python programmers. However, AvantPy aims to make it easy
for tools like Python's `IDLE <https://docs.python.org/3.7/library/idle.html>`_,
`Mu <https://codewith.mu/>`_,
`Thonny <https://thonny.org/>`_, etc., to "hook" to AvantPy and make it available
to their users.

Limitations
-----------

A. Limited scope

AvantPy is limited in scope: the goal is to provide only a basic set of translated/localized
keywords, built-in and error-handling functions, thus making it possible for absolute
beginners to learn very basic programming concepts in their own language.

AvantPy does not aim have a localized version of all of Python's builtin functions, nor
does it aim to provide a translation of any modules from Python's standard library.
If AvantPy is successful, it is conceivable that a few additional Python
resources, in particular its `Turtle <https://docs.python.org/3.7/library/turtle.html>`_ module, might be localized. However, no work
is planned in this direction in the near future for AvantPy.

B. Possibly incorrect grammatical structure

AvantPy dialects are assumed to be a one-to-one translations of keywords into the corresponding
AvantPy English dialect. Unlike the text that appears on blocks in Scratch or Blockly,
it could happen that the simple translation of keywords does not result in
grammatically correct word order in a given language.

As a concrete example, AvantPy assumes that separate translations of ``repeat`` and ``until`` exist,
and that they can be combined with a user-defined ``"condition"`` in **exactly** the following
order::

    repeat until "condition":

It is almost certainly the case that this will not yield a grammatically correct phrase
in some languages.  [If you know of concrete examples, please feel free to contribute.]
