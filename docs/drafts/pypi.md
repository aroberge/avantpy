# Inclusion in Python core vs module on pypi

Nowadays, before a package is added to the Python standard library, it is
often suggested that it be made available on pypi first.
This suggestion is, _I believe_, made primarily for two reasons:

1. Ensure that there is enough interest for the module,
2. Ensure that the API is mature enough and useful enough compared with only using the existing modules from the standard library.

However, even when this is the case, such as the well-known [requests](http://docs.python-requests.org/en/master/) library, the inclusion in the
standard library is far from automatic. Modules included in the standard
library are meant to be stable, with very few changes expected in their API when a new
Python version is released.

## Why should the proposed module be included directly in the Python standard library?

As [Steve d'Aprano wrote in May 2015](https://mail.python.org/pipermail/python-ideas/2015-May/033633.html):

> I think that the majority of Python programmers have no idea that you can even write an import hook at all, let alone how to do it.

Programmers know that you can create your own syntax with languages from
the Lisp family. In the same way, the vast majority of programmers
_know_ that you cannot do this with Python ... even though you can, using
an import hook. Releasing a package on pypi that allows you to do something
that people think is not possible to do is not very helpful in having them
discover this capability.

Designing an API for an import hook as described, which would include a new
syntax for identifying what code transformation is to be applied, is too important
not to be standardized after careful consideration by a group of experts.
Leaving it to amateurs, like myself, to come up with their own syntax and
upload a module to pypi, [like I did for a toy](https://pypi.org/project/experimental/),
is not the right approach for something that could give even more visibility
to Python in the international community.


Recently, I got a copy of the third edition of
the Python Cookbook, written by David Beazley and Brian K. Jones. Almost 3 years
prior to getting this book, I had already managed to use import hooks to find a way to easily modify Python's syntax (add references here).
To do so, I had initially used the `imp` module which is deprecated.
I tried to use the newer approach but could not manage to do so on my own;
thankfully, someone on StackOverflow was nice enough to explain how to do this.

So, I was quite eager to see if Beazley and Jones had included examples
of using import hooks in the cookbook. And they do.
In the discussion of one of the recipes they
give (10.11), they wrote (on page 420):

> _...it should be emphasized that Python's module, package and import
> mechanism is one of the most complicated parts fo the entire language --
> often poorly understood by even the most seasoned Python programmers
> unless they've devoted effort to peeling back the covers._

Near the end of the discussion (on page 428), they add

> _Assuming that your head hasn't completely exploded at this point, ...
> Last, but not least, spending some time sleeping with
> [PEP 302](https://www.python.org/dev/peps/pep-0302/) and the
> documentation for `importlib` under your pillow may be advisable._

Given this assessment, I believe it would be essential that such a module
be written by people that are experts in using `importlib`. Having it
in the standard library would ensure that it could be relied upon when a new
version of Python is made available.

NOte: from https://devguide.python.org/stdlibchanges/#acceptable-types-of-modules

> _Typically two types of modules get added to the stdlib. One type is a module which implements something that is difficult to get right._


It would also ensure that its API is documented and, with the adoption of
[PEP 545](https://www.python.org/dev/peps/pep-0545/), made available in
many languages - keeping in line with one of the motivation for the proposed
addition.