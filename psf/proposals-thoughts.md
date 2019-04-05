# Thoughts on AvantPy-releated proposals for the PSF

Recently, the Python Software Foundation Board Committee for Python in Education (hereafter referred to as "Committee") posted a [Request for Proposals](http://pyfound.blogspot.com/2019/04/update-on-python-in-education-proposal.html).
This followed a previous [Request for Ideas](http://pyfound.blogspot.com/2019/01/python-in-education-request-for-ideas.html).

During the **Request for Ideas** phase, I [submitted such an idea](https://github.com/aroberge/avantpy/blob/master/psf/idea.md).
I will not repeat its contents here, but some of that content could,
and probably should be included in a formal proposal.

When I submitted the previous document, AvantPy did not exist as such; now, it does.
It is still very much in its infancy, is far from being complete (even for
a single language and/or dialect), but it does work.
The current state of AvantPy is [mostly documented here](https://aroberge.github.io/avantpy/docs/html/).

According to the initial posting on the PSF blog, some funding will be made
available to support approved projects.
**I do not intend to request any funding for my own work on AvantPy.**
However, various contributions to the project would likely need financial
support from the PSF.  If you are reading this as a potential contributor
to AvantPy itself, or to another project that could make use of AvantPy, you
are in a position to determine if you need funding to accomplish your goal.

## What AvantPy needs

AvantPy needs:

    1. More work done on error handling to provide meaningful feedback to beginners instead
       of standard Python tracebacks.
    2. More languages supported.
    3. More dialects, one for each language supported.
    4. A GUI-based REPL, to demonstrate how it could be integrated in other editors/IDEs
    5. A GUI-based editor/code runner, to demonstrate how it could be integrated in other editors/IDEs
    6. A basic turtle-like module, translated into another language, to be used as a template to be adapted in any other supported language.

I plan to work on items 1, 4, 5, and 6 on my own, but would definitely welcome contributions.  I also will provide support to anyone that wishes to contribute for items 2 and 3.

There are other ideas I wish to explore; I will give only one example.
Currently, [Mu](https://codewith.mu/) uses [Black](https://github.com/ambv/black)
as a code formatter available to students. From what I have read, it appears to
be an addition very much welcome by students and teachers alike.
Given the ability of AvantPy to convert code from a given dialect to Python and
back to that dialect again, it might be possible to demonstrate how Black
could be used to do the same for any given dialect. This would require some
changes to the conversion functions used in AvantPy.


## What AvantPy could use

AvantPy, as a concept, has three core elements, and a potential fourth one:

    1. Its "friendlier tracebacks" translated in various languages
    2. The addition of a few keywords, such as `repeat`, `notimported`, etc.,
    3. The "localization/translation" of Python keywords to create different dialects
    4. The localization/translation of a turtle-like module

Our premise is that these could be useful to beginners learning programming.
**This should be validated.**

AvantPy could use the following.

    - Having experienced teachers work with new students and see if students can indeed benefit from using AvantPy in their learning process.
    - Doing the same, but it some formal study, with two different groups of learners
    - Writing code to integrate it into existing editors/IDEs as a plugin.

## One or many proposals

There is nothing that prevents many individuals or groups from submitting
different proposals for funding to the PSF.

I personally would like to submit a proposal to the PSF, either as an individual
or as part of group of collaborators.

However, I also support the idea of other individuals or groups independently
submitting their own proposals based on AvantPy to the PSF.

If I were to submit a proposal to the PSF without collaborators,
my current/initial thoughts would be to ask for

  - Recognition/approval in principle of the concept of AvantPy, as meeting the criteria set for the Request for proposals
  - Setting some money aside for supporting local user groups in various international settings that wish to work on AvantPy, either by doing some code sprints (including translation work) or by conducting workshop with students in order to validate the approach.

