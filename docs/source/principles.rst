Guiding principles
==================

AvantPy aims to be a project that facilitates learning computer programming while minimizing the pain. AvantPy will strive to make informed decisions about designs based on other successful programming language or environments, and from feedback from its users.

AvantPy is limited in scope: the goal is to provide only a basic set of translated/localized
keywords, built-in and error-handling functions, 
thus making it possible for students to learn basic programming concepts in their own language.

AvantPy does not aim have a localized version of all of Python's builtin function, nor
does it aim to provide a translation of any modules from Python's standard library.
However, if AvantPy is successful, it is conceivable that a few additional Python
resources, such as the Turtle module, might be localized. However, no work
is planned in this direction in the near future for AvantPy.

For students
------------

AvantPy aims to:

- make it possible for students to learn **basic** programming concepts in their own language;
- provide simple to understand error messages (tracebacks);
- for those that wish going beyond the basics, allow for an easy transition to programming using standard Python.

For instructors
---------------

AvantPy aims to make the job of instructors teaching programming easier.  (This definitely needs to be explained better.)

For contributors
-----------------

Other than users that provide feedback, including bug reports and suggestions for improvements,
we can think of two different types of contributors.

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

B. Contributor of "core" code

Currently, the "core" code does not rely on any "advanced" knowledge of computer science.
The way that the users's code is parsed and modified uses simple methods, and does not
require any knowledge about parsers, abstract syntax trees, etc. Ideally, the code should
be "easy" to understand and modified by a self-taught intermediate programmer - like the
current author.

It is very likely that using more advanced programming techniques could speed up the transformations and error handling done by AvantPy; however, speed of execution is not the goal of AvantPy.
AvantPy aims to be easy to use by beginners, and easy to contribute to by developers.

For third parties
-----------------

AvantPy does not aim to be a full programming environment; it adresses a different need
than editors or IDEs aimed at Python programmers. However, AvantPy aims to make it easy
for tools like Python's IDLE, [Mu](https://codewith.mu/),
[Thonny](https://thonny.org/), or others, to "hook" to AvantPy and make it available
to their users.
