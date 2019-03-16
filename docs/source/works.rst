How does it work?
=================

AvantPy uses an `import hook <https://docs.python.org/3/reference/import.html#import-hooks>`_
to load program files written in a known dialect (``xx``), recognizing them based on their
extension (``.pyxx``).
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

For a concrete example showing a file written in the French dialect, using a mix
of French dialect constructs and normal Python keywords, and the source
transformed into standard Python, see
`this link <https://htmlpreview.github.io/?https://github.com/aroberge/avantpy/blob/master/tests/test_french.html>`_.

From the source
---------------

The following can definitely be skipped, unless you want to know all the details.

.. autofunction:: avantpy.conversion.to_python
   :noindex:
