Special keyword: ``repeat``
============================

Repeating a series of instructions is something that is often done when
running programs.  Block-based programming environments, such as
`Scratch <https://scratch.mit.edu/>`_,
`Blockly <https://developers.google.com/blockly/>`_,
`GP <https://gpblocks.org/>`_, etc,
have different blocks that can be used for this purpose.  For example:

.. image:: images/repeat10.png
   :scale: 100 %
   :alt: Repeat 10 block

.. image:: images/repeat_until.png
   :scale: 100 %
   :alt: Repeat until block

and a "repeat forever" loop in French:

.. image:: images/repeat_forever_fr.png
   :scale: 55 %
   :alt: French repeat forever block


Depending on the block-based environment one uses, there are up to four
four main such cases, which can be written as follows
in standard Python::

    for _ in range(n):
        '''Repeat a series of instruction n times, without having to
           keep track of the specific iteration number
        '''

    while condition:
        '''Repeat a series of instruction an unspecified number of times,
           while a certain condition is met.
        '''

    while not condition:
        '''Repeat a series of instruction an unspecified number of times,
           until a certain condition is met.
        '''

    while True:
        '''Repeat a series of instruction an unspecified number of times,
           until a something inside the loop triggers a "break" to end the loop.
        '''

Inspired by the choices made by creators of block-based programming environments,
AvantPy introduces a few additional keywords to cover the 4 cases above
in a natural way::

    repeat n:
        # code

    repeat while condition:
        # code

    repeat until condition:
        # code

    repeat forever:
        # condition

.. note:: **Learning from experts**

   The Quorum computing language has been designed based on evidence gathered
   from `how human learn programming languages <https://quorumlanguage.com/evidence.html>`_.

   It includes `three of the four repeat <https://quorumlanguage.com/tutorials/language/repeat.html>`_ choices mentioned above, with a slightly different syntax::

        repeat 10 times
            // code
        end

        repeat while condition
            // code
        end

        repeat until condition
            // code
        end



A concrete example
-------------------

Suppose that I am teaching programming to beginners using Python's turtle module.
So far, we've only written programs that use one instruction per line::

    from turtle import forward, left

    # Draw a square

    forward(100)
    left(90)

    forward(100)
    left(90)

    forward(100)
    left(90)

    forward(100)
    left(90)

I wish to use this to show to students how we can have computers **repeat**
a given set of instructions, instead of typing them multiple times.
Using Python, here's the natural way to do this::

    from turtle import forward, left

    # Draw a square

    for variable in range(4):
        forward(100)
        left(90)

In doing so, I need to introduce all at once many new concepts and additional terms:

   1. the concept of an indented code block preceded by a colon;

   2. two keywords, ``for`` and ``in``;

   3. the use of a *variable*, which is some quantity with a completely irrelevant name in this example, except that it cannot be a keyword;

   4. the introduction of a built-in function, ``range()``, which, unlike ``forward()`` or ``left()``, does not have a visual representation.

By contrast, using the ``repeat`` keyword, the above can be written as::

    from turtle import forward, left

    # Draw a square

    repeat 4:
        forward(100)
        left(90)

and we only need to introduce fewer new topics:

   1. the concept of an indented code block preceded by a colon;

   2. one new keyword: ``repeat``.

More gradual approach
---------------------

As we are writing this, we note that
`GP control blocks <https://gpblocks.org/wiki/doku.php?id=blocks:control>`_
include the following blocs which allow for a gradual
interpolation between something like ``repeat 10:`` and the
more complex and versatile Python idiom::

   for i in range(1, 10, step):
       # some
       # code

.. image:: images/repeat_gp.png
   :scale: 50 %
   :alt: Repeat blocks in GP

However, we do not see the need to include this type of granularity
in AvantPy.

A final word
-------------

We've already mentioned the usage in blocks-based programming environment
of ``repeat``, or some similar alternative in other languages. ``repeat``
was also the clearer possibility for people unfamiliar with programming jargon
as found by Andreas Stefik and Susanna Siebert, and published
"An Empirical Investigation into Programming Language Syntax."
ACM Transactions on Computing Education, 13(4), Nov. 2013.
