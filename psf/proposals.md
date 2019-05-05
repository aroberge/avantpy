# Python in Education Proposal

This is a request for support for a project named **Friendly-traceback**.

## The context

Recently, the Python Software Foundation Board Committee for Python in Education (hereafter referred to as "Committee") posted a [Request for Proposals](http://pyfound.blogspot.com/2019/04/update-on-python-in-education-proposal.html).
This followed a previous [Request for Ideas](http://pyfound.blogspot.com/2019/01/python-in-education-request-for-ideas.html).

During the **Request for Ideas** phase, I [submitted such an idea](https://github.com/aroberge/avantpy/blob/master/psf/idea.md)
about a potential project named AvantPy, which can be described as follows:

- AvantPy is a collection of dialects, each dialect being a superset of Python, designed to make it easier to learn programming concepts in a given human language.
  - Each dialect consists of a translations of most Python keywords in a given human language, supplemented by a few additional keywords intended to make some concepts easier to learn.
- AvantPy is a preprocessor, that takes a program written either totally or
in parts in a given dialect, and converts it to standard Python prior to execution.
  - A syntactically valid program can include a mix of code written in normal Python and in a specific dialect. This is to ease the transition to learning Python.
- AvantPy also includes a custom REPL.
- AvantPy also includes tools to analyze Python tracebacks and translate them
  into something easier to understand by beginners.
  [**Please take note of this last point.**]

When I submitted the previous document, AvantPy did not exist as such; now, it does.
It is still very much in its infancy, but it does work.
The current state of AvantPy is [mostly documented here](https://aroberge.github.io/avantpy/docs/html/).

As I worked on AvantPy, I realized that the tool I had planned to analyze
Python tracebacks and translate them into something easier to understand
by beginners was something of more general applicability, and would benefit
to be turned into a separate project, which could eventually be used by
AvantPy itself as well as other projects.
As an example, from some early discussions,
the main developpers for both
[Mu](https://codewith.mu/) and [Thonny](https://thonny.org/)
have expressed an interest into this new project.
This new project is named **Friendly-traceback** and is currently
[documented here](https://aroberge.github.io/friendly-traceback-docs/docs/html/index.html).

## Criteria from the PSF

In this section, I address briefly each topic mentioned in the blog post
about submission of proposals.

### Category

Friendly-traceback aims to provide simplified tracebacks translated
into as many languages as possible. It does fall under Category 2 (localization).

### Code of conduct

As stated in the [readme for friendly-traceback](https://github.com/aroberge/friendly-traceback):
*We completely support the
[Python Community Code of Conduct](https://www.python.org/psf/codeofconduct/).
Contributors to this project, including those filing or commenting on an issue,
are expected to do the same.*

### Mission of the PSF

*The mission of the Python Software Foundation is to promote, protect, and advance the Python programming language, and to support and* **facilitate the growth of a diverse and international community** *of Python programmers.* [Emphasis added.]

Friendly-traceback aims to reduce the learning curve for beginners in providing
explanations that are both easy to understand and translated into languages other
than English.

### Impact

By design, Friendly-traceback is intended to be used by an international audience.

I address the issue of the main challenges separately.

### Feasability

One month ago, Friendly-traceback did not exist.
The first commit to the code repository was made on April 7, 2019.
In a very brief period, significant progress has already been accomplished, as
[documented here](https://aroberge.github.io/friendly-traceback-docs/docs/html/index.html)

As of this writing, excluding `SyntaxError`, more than 20 different causes of
Python exceptions can be analyzed and explanations provided in
either [English](https://aroberge.github.io/friendly-traceback-docs/docs/html/tracebacks_en.html) or
[French](https://aroberge.github.io/friendly-traceback-docs/docs/html/tracebacks_fr.html)

For `SyntaxError`, we can currently replace the standard but very
unhelpful `SyntaxError: invalid syntax` by accurate explanations,
in either English or French, for 10 different cases.

The first milestone is to provide similar explanations for all standard
Python exceptions, in both French and English. Eventually, we might also
include exceptions from specific modules of the Python standard library,
such as [Decimal](https://docs.python.org/3/library/decimal.html)
or [Turtle](https://docs.python.org/3/library/turtle.html).

While the above describes my capability to start and make
progress on a project, it does not address the issue of capability of
bringing a project to a satisfactory state of completion.
To address this point, I offer two examples of my projects:

- My first Python related project was rur-ple,
  [first hosted on sourceforge](http://rur-ple.sourceforge.net/) and which
  has been used by thousand of beginners to learn Python.
  The latest version can be [downloaded here](https://code.google.com/archive/p/rur-ple/downloads) and includes support for English, French, German, Spanish,
  Turkish, Welsh, and Simplified Chinese.

- [Reeborg's World](http://reeborg.ca/reeborg.html) is the successor of
  rur-ple, with significantly more features. It has also been translated in
  a few languages as can be seen from the web site.

### Diversity and inclusivity

Trying to put words on issues dealing with diversity and inclusivity can be
difficult to do as the risk of misrepresenting opinions written by others
is always present.

The first mention of providing translations for Python tracebacks that
I have been able to find is a suggestion I made in May 2010
[on the Python-ideas list](https://mail.python.org/pipermail/python-ideas/2010-May/007211.html).
This idea was supported by a few other international users but not from
most people participating in this discussion list.

In October 2012, another user [filed a bug](https://bugs.python.org/issue16344)
on this issue, hoping to gets support, but got nowhere.
From the discussion, it is clear (to me) that many core developers did not see this
as an opportunity to make the Python community more inclusive and diverse.
On the contrary, some opinions expressed could be summarized/paraphrased
as "If you want to program in Python, learn English like the rest of us."

One of the goals of Friendly-traceback is to make it easier for people
who may feel inadequate as they do not understand English sufficiently well
to overcome what they perceive to be a barrier to learning programming
in Python.  Of course, the issue of understanding tracebacks is only the
tip of the iceberg when dealing with this problem; however, I see it as
an important first step.  (Side note: AvantPy, which I mentioned earlier,
may be a significant second step towards this goal.)

## Main challenges

The main challenges of this project are:

1. Providing accurate and easy to understand explanations for as many sources
   of Python exceptions as possible.

2. Translating these explanations in as many languages as possible.

In principle, and given enough time, I could meet (in some way) the first
goal entirely on my own.  I write "in some way" as the
"easy to understand explanations" will only be so based on my own pre-conceptions.

In order to be truly "easy to understand", it is essential that the work be
validated by instructors that work with beginners, who could provide
invaluable feedback that could be used to improve the explanations given.
The type of questions that need to be answered include:

- Are the explanations provided accurate and easy to understand?

- Are there cases where tracebacks occur and no adequate explanation
  is provided by Friendly-traceback?

- When a Python traceback occurs, a beginner's first reaction might be
  one of shame or inadequacy ("it's my fault; I'm stupid; etc.").
  How well does Friendly-traceback alleviates this problem and help
  beginners feel empowered to use the information provided to solve the
  problem they face.

- What does a beginner programmer think *they* ought to do when presented
  with an exception message?

- Are the beginners' perceptions the same that we
  (as experienced developers and/or educators) think they should
  have when they encounter an exception message?

- How well does Friendly-traceback contribute to helping beginners in
  understanding how to use the information provided by a standard Python
  traceback.

- etc.

In terms of translations, I can only write first drafts in French and English;
other languages will have to be contributed by other people.
The challenge here is to find a way to reach out to native speakers of
other languages and get them interested enough to contribute.

## The request

At this stage, Friendly-traceback needs more visibility:

1. To attract contributors who could increase the number of Exceptions
   covered;
2. to attract contributors who could provide translations;
3. to attract instructors working with students and who would be willing
   to give feedback leading to improvements.

Friendly-traceback does not require direct financial support for the PSF.
What is mostly needed is help in publicizing this project to a larger
international audience. This could be as simple as a blog post, or go as
far as making a point of mentioning it and the need for increasing the number
of languages covered whenever a request for funding comes
from organizers of Python-related conferences.

Helping to increase the number of Exception cases covered can be done either
[simply by suggesting a new example](https://aroberge.github.io/friendly-traceback-docs/docs/html/suggest.html) or
[writing code to deal with a new case](https://aroberge.github.io/friendly-traceback-docs/docs/html/adding_exception.html).
**The greater the number of potential contributors can be reached and
encouraged to either suggest an example or
contribute code, the faster the project will be completed.**

However, financial support for groups could be helpful in possibly two specific cases:

1. For groups that want to organize coding sprints to increase the number
   of exceptions being included in Friendly-traceback. If this project receives
   enough visibility to encourage volunteers to contribute quickly, this
   type of support might not be needed.

2. For experienced instructors that teach beginners in informal settings and
   are willing to use Friendly-traceback and provide feedback leading to
   improvement to the project.  (Financial support might be needed to
   cover the cost of renting a room and/or equipment, as well as possibly
   food for participants.)  We note that we have received private
   correspondance from the creator of [Mu](https://codewith.mu/) who plans
   to include Friendly-traceback in an alpha version for Mu.
   As you likely know, Mu has been designed specifically with beginners in mind.


## Final comment

As mentioned, Friendly-traceback has been carved out of a larger project
named AvantPy.  While the work on AvantPy has been temporarily stopped to
focus on Friendly-traceback, AvantPy's goals are larger than those
of Friendly-traceback and, I believe, would also meet the criteria set
out by the Education Committee for this request for proposal.
Just like Friendly-traceback, AvantPy could certainly benefit from an
increased visibility in order to attract contributors that could make it
accessible to a larger international audience.
