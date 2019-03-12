"""Creates a version of traceback.rst to insert in the documentation.

This assumes that such a file already exist; this is only done to
ensure we have the right destination. If so, we actually rewrite it.

"""

import os
import sys
from contextlib import redirect_stdout

this_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(this_dir, ".."))
sys.path.insert(0, this_dir)
sys.path.insert(0, parent_dir)

import avantpy

target = os.path.normpath(os.path.join(parent_dir, "docs/source/tracebacks.rst"))

try:
    assert os.path.isfile(target) 
except AssertionError:
    print("Wrong path: traceback.rst does not exist.")
    print("This program should be run from the root directory of this repository.")
    sys.exit()

content = """Friendly error messages
=======================

AvantPy aims to provide friendlier feedback when an exception is raised than what is
done by Python.
Such feedback will also be available in languages other than English.

.. todo::

     Write program that generate sample tracebacks from each case covered and
     use it to generate the "Friendly error messages" file automatically.

Added by update_tb.py
"""

def make_title(text):
    print(text)
    print("-" * len(text), '\n') 

with open(target, 'w') as out:
    with redirect_stdout(out):
        print(content)

        make_title("IfNobreakError")
        print("Example 1::")
        import ifnobreakerror
