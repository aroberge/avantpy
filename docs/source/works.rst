How does it work?
=================

AvantPy uses an `import hook <https://docs.python.org/3/reference/import.html#import-hooks>`_
to load program files written in a known dialect (``xx``),
recognizing them based on their extension (``.pyxx``).
It uses the information in the definition file (``xx.py``) to translate keywords found
into that definition file into the corresponding Python keyword or idiom.
During this process, some errors can be caught and custom exceptions raised.

If no exceptions are raised, the transformed program is executed.
This could result in some standard Python exceptions raised.
These are caught and an attempt is made to provide information in a
more user-friendly way, possibly also with more details than Python's
standard tracebacks.

.. warning::

    The error analysis is far from being fully implemented.

Note that normal Python keywords are allowed into a file written
in another dialect.

The conversion process in some details
---------------------------------------

The following can definitely be skipped unless you are interested in
(most of) the gory details.

AvantPy uses Python's ``tokenize`` module to convert a
source into a sequence of tokens. A token might be the name
of a variable, an operator, a parenthesis, a string, etc.

AvantPy analyses these tokens,
replacing some written into a different dialect until all
are converted into standard Python tokens.  Then, these
are recombined into a string which is the source to be
executed.

Python's tokenize module includes a function, called
untokenize, which can be used to combine a series of tokens
into a valid program.  With a normal Python program, doing
something similar to::

    new_source = untokenize(tokenize(source))

would be such that executing ``new_source`` would be the same
as executing ``source``.  However, the spacing between tokens
would not necessarily be the same for both ``new_source``
and the original program.  For example, the original program
may include a line like::

    variable = function( argument )

which might be converted into::

    variable =function(argument)

This could make it more difficult to compare the original
code with the converted one, as it is possible to do
using one of the utilises provided with AvantPy,
or any "diff" program.
As a result, we do not use Python's
untokenize function, and explicitly keep track of spacing
between tokens.

To understand how the conversion process works, it is useful to review
all possible cases, from some of the most complex, ending
with the simplest ones.

A. ``nobreak``

AvantPy has an additional keyword, named ``nobreak`` in the
English dialect, which can be used in ``for`` or ``while``
loops instead of the standard ``else``, as in::

    while condition:
        # code
    nobreak:
        # code

However, ``nobreak`` cannot be used in an ``if/elif/else``
blocks to replace ``else``.

Furthermore, ``nobreak`` cannot be used instead of ``else``
in an assignment such as::

    a = 1 if True else 2

To identify if a program includes a ``nobreak`` keyword
mistakenly, every time we see a leading ``for``, ``while``,
``if`` or ``elif`` keyword (or their equivalent in a
given dialect), we note the indentation (column where the
first character is written) and the corresponding keyword.
A list containing these keywords is called ``blocks_with_else``
in this function.

Later, when we encounter a ``nobreak`` keyword at a given
indentation, we check to see if the last ``blocks_with_else``
keyword found at that same indentation was one for which
it made sense to use ``nobreak`` or not.  If it was a
loop, we simply replace ``nobreak`` by ``else``. If not,
we raise a custom exception which is handled elsewhere.

B. ``repeat``

In addition to the standard Python loops constructs, AvantPy
support four additional idioms::

    repeat forever:           # while True:
        pass
    repeat while condition:   # while condition:
        pass
    repeat until condition:   # while not condition:
        pass
    repeat n:                 # for some_var in range(n):
        pass

For this last case, ``n`` could be an expression that evaluates
to an integer. However, the only colon that can appear must be
the end of statement colon.

When we encounter the equivalent to the "repeat" keyword in
the selected dialect, we must make sure that it is the first
keyword occurring on a logical line; if not, we raise a
custom exception.

If ``repeat`` is the first keyword on a line, we set a flag
(repeat_loop) to True, preparing to look at the next token.

a) If the next token is one of ``forever``, ``until``, ``while``,
or their equivalent in the target dialect
(remember that including normal Python keywords in a program written
in a different dialect is allowed)
we can proceed with the rest in a straightforward manner.

b) if that is not the case, we set a different flag (repeat_n)
to True so that we can deal with the relevant for loop.

For this last case, the variable in the for loop is a dummy
variable; we must ensure that its name is chosen such that
it does not occur anywhere else in the source code.
This is accomplished using a method called
``get_unique_variable_names``.

C. ``nobreak`` and ``repeat``

A ``repeat`` loop is essentially a ``for`` or a ``while``
loop. As such, it could have an ``else`` clause which
has a clearer meaning if the keyword ``nobreak`` is used
instead.  Thus, just like we mentioned before, we also
keep track of where a leading ``repeat`` is used.

D. Direct translation

If a token does not match one of the cases described above,
we need to see if it is a term used in the dialect; if
so, we simply translate it into standard Python.

E. Brackets

In Python, brackets must always come in pairs: (...), [...],
{...}. In the course of processing the file, if we identify
brackets which are not paired correctly, an exception
is raised.

F. Remaining tokens

Any remaining token is left as is; it is assumed to be valid
Python.
