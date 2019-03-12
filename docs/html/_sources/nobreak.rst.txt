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
of using ``else:``, one could write something like* ``if no break:``.
In theory, it might be possible to do something like this in AvantPy.
However, wanting to have a one-to-one keyword translation from one
dialect into another (excluding standard Python), I thought that a
suggestion made by Raymond Hettinger made the most sense:
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
instead, an explicit ``raise SyntaxError`` statement will be inserted
and the file transformation will be stopped at that point. 
See `this link <https://htmlpreview.github.io/?https://github.com/aroberge/avantpy/blob/master/tests/if_nobreak.html>`_ for an explicit example.

AvantPy aims to provide beginner-friendly tracebacks, written in their
native language.  Since we can identify this incorrect use of ``nobreak`` 
in the translation phase, it seems logical to ensure that this syntax error
will be identified as early as possible, with a meaningful error message
provided.

Think of other languages
------------------------

Using English, one can think of::

    if something:
        do_this()
    else:
        do_that()

as being equivalent to

    if something:
        do_this()
    otherwise:
        do_that()

However, ``otherwise`` would almost certainly be a wrong word choice in::

    while condition:
        do_this()
    otherwise:
        do_that()

Now, imagine a new dialect where a keyword equivalent to ``else`` has
been chosen in for the ``if/else`` construct. It is quite possible that
such a keyword would definitely not convey the right meaning for
a ``while/else`` loop.  If only for this reason, we believe it
makes sense to have an additional keyword, such as ``nobreak``.

What about try/except?
-----------------------

The ``else`` keyword can also be used in a ``try/except/else/finally`` block.
For now, we assume that, unlike ``nobreak,
we do not need any other keyword than ``else``.
If it were found that the use of the equivalent of ``else`` in some language
would not be appropriate in this construct, we could consider
introducing another keyword - perhaps something like ``noexcept``.
