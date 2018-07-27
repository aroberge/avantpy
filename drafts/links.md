# Various links of potential interest

`__experimental__` mentioned: https://mail.python.org/pipermail/python-ideas/2011-August/011279.html

Luciano's support for repeat https://mail.python.org/pipermail/python-ideas/2015-October/036843.html

https://mail.python.org/pipermail/python-ideas/2015-October/036834.html

- adding hooks to IDLE for Python dialects

Very first mention of `__experimental__` https://mail.python.org/pipermail/python-list/2001-March/105776.html


http://macropy3.readthedocs.io/en/latest/index.html



Extensibility of various languages https://softwareengineering.stackexchange.com/questions/164665/programming-languages-with-a-lisp-like-syntax-extension-mechanism


https://github.com/samrushing/cps-python/

https://mail.python.org/pipermail/python-ideas/2016-January/038140.html

Rejected PEP (by its author): https://www.python.org/dev/peps/pep-0511/

Need to read https://mail.python.org/pipermail/python-ideas/2016-January/037892.html

"I think something that isn't made clear in the rationale is why an import hook is good enough for most semantic extensions, but isn't good enough for global optimizers."  https://mail.python.org/pipermail/python-ideas/2016-January/037908.html

https://mail.python.org/pipermail/python-ideas/2016-February/038450.html refers to where one might learn about implementing bytecodes.

## Blog posts

October 14, 1995 https://aroberge.blogspot.com/2015/10/from-experimental-import-somethingnew.html

I wrote the following:
> I'm not ready yet to bring another suggestion to the python-ideas list ... However ...
>
> Python support the special `from __future__ import ...` construct to determine how it will interpret the rest of the code in that file.  I think it would be useful if a similar kind of statement "from __experimental import ..." would also benefit from the same kind of special treatment so that it
would work in all instances, and not only when a module is imported.   People could then share (and install via pip) special code importers and know that they would work in all situations, and not limited to special environments like Reeborg's World, or IDLE as suggested by T.J. Reddy and likely others.

However, a concrete suggestions along these lines will have to wait for another day...


Octobre 14, 1995 - second post https://aroberge.blogspot.com/2015/10/from-experimental-import-somethingnew_14.html

Feb 5, 2017 https://aroberge.blogspot.com/2017/05/whats-in-name.html

Dec 1, 2015 https://aroberge.blogspot.com/2015/12/french-python.html

Apr 24, 2017 https://aroberge.blogspot.com/2017/04/easily-modifiable-python.html

## From Python-ideas

https://mail.python.org/pipermail/python-ideas/2007-September/000968.html

- `skip` instead of `continue`
- `loop` on its own
- `loop while` and `loop for`
- `breakif` and `skipif`

Note that `loop` was criticised by someone else as using computer jargon,
which is ironic given that the suggestion to use `skip` was to avoid
using `continue` given its different meaning in computer jargon.


translation of keywords:
https://mail.python.org/pipermail/python-ideas/2009-April/004179.html


translating tracebacks:
https://mail.python.org/pipermail/python-ideas/2010-May/007211.html
  important comment https://mail.python.org/pipermail/python-ideas/2010-May/007213.html


Completely localized version of Python:
https://mail.python.org/pipermail/python-ideas/2010-November/008826.html

- Follow up starting at https://mail.python.org/pipermail/python-ideas/2010-December/008831.html


https://mail.python.org/pipermail/python-ideas/2011-April/009765.html

- AST transformation hooks for domain specific languages
more at https://mail.python.org/pipermail/python-ideas/2011-April/009803.html


https://mail.python.org/pipermail/python-ideas/2012-August/015987.html

- verbose traceback formatting. The subsequent discussion mentions https://docs.python.org/3.7/library/cgitb.html.


https://mail.python.org/pipermail/python-ideas/2012-October/016275.html

- Guido's explanation about why allowing unicode identifiers is a good idea (but not for Python keywords)

https://mail.python.org/pipermail/python-ideas/2013-March/019727.html

- about having an `__experimental__` package

https://mail.python.org/pipermail/python-ideas/2016-January/037884.html

https://mail.python.org/pipermail/python-ideas/2015-March/032817.html

- Py.test goes through the trouble
of parsing the python test_.py files in order to generate nicer error
messages.

https://mail.python.org/pipermail/python-ideas/2015-May/033623.html

- Andrew Barnett about using import hooks


https://mail.python.org/pipermail/python-ideas/2015-May/033638.html

- explains how to use importlib to access the AST

https://mail.python.org/pipermail/python-ideas/2015-May/033633.html

- _I think that the majority of Python programmers have no idea that you
can even write an import hook at all, let alone how to do it._

https://mail.python.org/pipermail/python-ideas/2015-May/033661.html

- idea of "teachpacks", somewhat similar to Scheme

https://mail.python.org/pipermail/python-ideas/2015-June/033953.html

- adding a hook between lexer and parser



https://mail.python.org/pipermail/python-ideas/2015-June/034055.html

- `source_to_code` hook added ...
- mentions of Macropy, hylang, Numba
- See http://stupidpythonideas.blogspot.com/2015/06/hacking-python-without-hacking-python.html


https://mail.python.org/pipermail/python-ideas/2015-September/035672.html

- adding non English names in the turtle module

https://stackoverflow.blog/2014/02/13/cant-we-all-be-reasonable-and-speak-english/

https://mail.python.org/pipermail/python-ideas/2016-December/043910.html

- better error messages

https://mail.python.org/pipermail/python-ideas/2017-March/045344.html

- `repeat_for n:`

https://mail.python.org/pipermail/python-ideas/2015-May/033570.html

- `unless` as synonym for `if not`

## other

tail call optimization https://eli.thegreenplace.net/2017/on-recursion-continuations-and-trampolines/

about keywords for loops
http://neverworkintheory.org/2014/01/29/stefik-siebert-syntax.html
http://sci-hub.tw/10.1145/2534973