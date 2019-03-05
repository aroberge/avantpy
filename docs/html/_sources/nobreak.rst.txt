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

AvantPy's English dialect includes ``nobreak`` as an additional keyword.
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

