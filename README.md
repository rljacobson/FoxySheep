#What is FoxySheep?
FoxySheep is a **Wolf**_ram_ Language ANTLR4 lexer and parser grammar. FoxySheep also has a visitor that emits FullForm expressions (essentially the parse tree but in a format that Mathematica can read and evaluate). The FullForm emitter is written in Java, but other target languages are planned.

In this document, Wolfram Language refers to the programming language used in Mathematica (and some other Wolfram Research products), and Mathematica refers to the computer algebra system (or its kernel) produced by Wolfram Research. FoxySheep and its author(s) are not affiliated with Wolfram Research.

#Possible uses for FoxySheep
You can use it to

* write a pretty printer for Wolfram Language code.
* write a Wolfram Language code rewriter that inputs code written using nasty language constructs and outputs the same program but using saner notation. (Ever try to read someone else's crazy Wolfram Language code?)
* add support for Wolfram Language to your favorite open source computer algebra system to make a Mathematica clone.

What FoxySheep doesn't do:

* Execute Wolfram Language code
* Interact with Mathematica

But nothing is stopping *you* from using FoxySheep in your own project to do the above!

#Project Status
FoxySheep is probably not yet ready to be used in your project. It needs a lot of testing and lacks some language features (see "How complete is FoxySheep?").

#How complete is FoxySheep?
FoxySheep has complete coverage of non-box-related language features, and sketchy untested coverage of box-related features. While it is a goal of the project, FoxySheep does not always have identical behavior to Mathematica for the language constructs that it implements.

#Contributing
If you want to contribute to the project, read CONTRIBUTING.md.

# Authors and License
Author(s): Robert Jacobson 

License: BSD license. See the file LICENSE.txt for details.