Friendly error messages
=======================

AvantPy aims to provide friendlier feedback when an exception is raised than what is
done by Python.
Such feedback will also be available in languages other than English.

.. todo::

     Write program that generate sample tracebacks from each case covered and
     use it to generate the "Friendly error messages" file automatically.

Added by update_tb.py

IfNobreakError
-------------- 

Example 1::

    AVANTPY EXCEPTION: IfNobreakError

    The AvantPy NOBREAK keyword cannot be used in an IF/ELIF/ELSE
    clause (Python: if/elif/else).

    Error found in file ifnobreakerror.pyupper on line 4.

             2: if True:
             3:     pass
      -->    4: NOBREAK:

