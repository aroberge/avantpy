Special keyword: ``nobreak``
============================

Python's ``for`` and ``while`` loop include an ``else`` clause
whose meaning is not immediately obvious::

    while condition:
        # some
        # code
        # here
    else:
        # will be executed only if no
        # break statement occurred above

When I first understood this, I thought *wouldn't it be nice if, instead
of using* ``else:``, *one could write something like* ``if not break:`` which
uses only existing Python keywords.
In theory, it might be possible to do something like this in AvantPy.
However, wanting to have a one-to-one keyword translation from one
dialect into another (excluding standard Python) whenever possible,
I thought that a suggestion made by Raymond Hettinger made the most sense:
AvantPy's English dialect thus includes ``nobreak`` as an additional keyword.
It can be used instead of ``else`` in the above example::

    while condition:
        # some
        # code
        # here
    nobreak:
        # will be executed only if no
        # break statement occurred above

When AvantPy encounters a ``nobreak`` keyword, or its equivalent in a
file, it tries to determine if such a keyword is indented matching
a ``for`` or a ``while`` statement: if that is the case, it replaces
by ``else``.


``nobreak`` instead of ``else`` in ``if/else``
-------------------------------------------------------

The ``else`` keyword has a very different meaning when used as part
of an ``if`` statement.  In this situation, ``nobreak``, or its
translation in some other language would make no sense.

As a result, if one attempts to write the following::

    if condition:
        # some
        # code
        # here
    nobreak:
        # more code

``nobreak`` will **not** be replaced by ``else``;
instead, an explicit ``raise IfNobreakError`` statement will be inserted
and the file transformation will be stopped at that point.

AvantPy aims to provide beginner-friendly tracebacks, written in their
native language.  Since we can identify this incorrect use of ``nobreak``
in the translation phase, it seems logical to ensure that this syntax error
will be identified as early as possible, with a meaningful error message
provided.

What about try/except?
-----------------------

The ``else`` keyword can also be used in a ``try/except/else/finally`` block.
For now, we assume that, unlike ``nobreak,
we do not need any other keyword than ``else``.
If it were found that the use of the equivalent of ``else`` in some language
would not be appropriate in this construct, we could consider
introducing another keyword - perhaps something like ``noexcept``.

Is ``nobreak`` really needed?
------------------------------

Python's use of an ``else`` clause in ``for`` and ``while`` loops is
rather unusual, relatively poorly known and not easy to understand
at first glance. It is for this latter reason that we make it possible
to define an alternative keyword ``nobreak`` or an equivalent translation
in the user's language.  However, given that is not often used, one could argue
that it could be left out entirely from AvantPy since AvantPy is intended for
beginners.

Our decision to include it is to give the possibility, to those instructors
that wish to teach such a construct/concept, to use a more natural keyword
in their own language; anyone else is free to ignore it.
