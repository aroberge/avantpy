# avantpy

Python with training wheels: executable pseudocode in any language.

## Some observations

First, some observations, in no particular order.

- Python is the best general purpose programming language! Ok, I admit, this is not really an observation, as much as my own opinion which seems to be shared by many.
- The success of block based programming environments, like [Scratch](https://scratch.mit.edu/), [Blockly](https://blockly-games.appspot.com/), [Edublocks](https://edublocks.org/), and many others, demonstrates that there may be better alternatives for introducing beginners to programming concepts than the traditional text-based environments.
- Python is often described as *executable pseudocode*. This is close to the truth if your pseudocode is written for an English audience but likely much less so for languages other than English.
- Edublocks describes itself as *Making the Transition from Scratch to Python easier.* Edublocks is a block-based environment and not a text-based one.
- The creators of [Racket](https://racket-lang.org/) clearly believe that having various dialects of a given programming language can be useful in helping to learn programming.
- Amongst the *best practices* identified by the creators of Blockly is the need for an [exit strategy](https://developers.google.com/blockly/guides/app-integration/best-practices#9_exit_strategy):

    *Block-based programming is often a starting point for programming. In the context of teaching computer programming, it is a gateway drug that gets students addicted, before moving them on to harder things. How long this block-based programming period should last for students is hotly debated, but if your goal is to teach programming it should be temporary.*

    ...

    *Block-based programming environments used for teaching programming need to have a concrete plan for graduating their students. A solid exit strategy also goes a long way towards placating those who argue that block-based programming isn't "real programming".*

## What is avantpy?

- avantpy is a collection of dialects, each dialect being a superset of Python, designed to make it easier to learn programming concept in a given human language.
- avantpy is also a collection of useful tools, like:

    - a custom REPL;
    - a tool to analyze Python tracebacks and translate them into easier to understand feedback for users;
    - a tool to convert programs written in a given dialect into standard Python, showing the differences between the two.

## What is meant by training wheels?

To help beginners learning how to ride a bicycle, one sometimes uses [training wheels](https://en.wikipedia.org/wiki/Training_wheels). After a while, the new cyclists ride
their bicycles without the training wheels needing to touch the ground to offer
additional support.

This is what avantpy aims to do for learning Python.

Say that I am a French speaker that learns to program using avantpy.
My first program might be:

```py
imprime("Bonjour !")
```

My second program might be

```py
répète 3:
   imprime("Ho !")
```

Eventually, I might start learning some "true" Python functions or keywords:

```py
répète 3:
   print("Ni!")
```

After a while, I will know enough to write

```py
for _ in range(3):
    print("Ni!")
```

and feel ready to leave avantpy and only write Python.

Just like Blockly's *exit strategy*, or Edublocks stated goal,
the goal of avantpy is to lead learners to eventually write programs in Python.