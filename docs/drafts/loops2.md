# Simpler loops?

## Context

You are teaching beginners about some concepts in computer programming in a Python-like language.
You have already shown them some "simple" constructs, perhaps like
```py
print("Hello World!")
```
so that they already know that:

* Some special words (keywords) have a specific meaning in the language
* Comments on a line are preceded by the `#` character
* Some special characters cannot appear in "words" (including keywords). For example, the following characters are not allowed in "words":

    [ ] ( ) ; , ' " (space)

  If a "word" is made of of many normal words in the language (English, French, etc.), we use the underscore character, `_`, where a space would appear. Thus, something like `else_if` would be a single "word" (possibly a keyword) in the computer language.


## Teaching the concept and syntax of loops

You want to teach the concepts of loops to beginners, and the syntax used for loops in the Python-like language you are using. These beginners have never seen the concept of loops before; if you have not taught such beginners, it is difficult to imagine how such a concept can be difficult to grasp when seen for the first time ... but it might be possible to imagine how a programming language syntax can complicate (or facilitate) the learning process. To this end, I will introduce the concept in a Python-like language where keywords are based on the French language.

A loop is a series of instructions that are repeated. The syntax used is the following:

```
répéter ? :
    # instructions
    # to be
    # repeated
    # are indented
```

There are four types of loops, identified by a different expression replacing the question mark above.

```
répéter n:      # n is an integer
    # block

répéter sans_fin:
    # block

répéter jusqu_à condition:
    # block

répéter pendant_que condition:
    # block
```

**A quiz**: which of the above correspond to Python's
```py
while condition:
    # block
```

If you know French and what a Python `while` loop is, the answer is obvious.
If you don't know French, you likely have a 50% chance of being wrong.

## The English version of the four loops

The four versions above can be written (in a different order) as follows
in English:

```py
repeat n:
    # block

repeat while condition:
    # block

repeat forever:
    # block

repeat until condition:
    # block
```

**A quiz**: which of the above correspond to Python's

```py
while condition:
    # block
```
This is the same question as before, but this time the answer should be completely obvious to someone who knows what a Python `while` loop is.

## Python's version

```py
for variable in range(n):
    # block

while True:
    # block

while not condition:
    # block

while condition:
    # block
```

For someone who is seeing the concept of loops for the very first time, the translation of any one of these four Python idioms (without seeing the other three) into the corresponding English version is likely not intuitively obvious.

## Observations

Python is often described as executable pseudocode. Once people have learned a few idiomatic expressions, like `for variable in range(n)`, translating pseudocode written in English into Python is usually very straightforward.

If the pseudocode is not written in English, the translation process is, at least initially, not as straightforward as an additional mental step is required by the translation from the original language into Python's English. The small number of keyword in Python is a definite help in this process.

For absolute beginners who are learning programming concepts (control flow structures, defining functions, etc.), being able to use a language that uses keywords easily understood in their own language can definitely facilitate the learning process.
This is the approach taken by people using block-based environment
(Scratch, Blockly, etc.) to help students learn programming concepts.
