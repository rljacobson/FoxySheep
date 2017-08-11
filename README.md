[TOC]: # "What is FoxySheep"

# What is FoxySheep?
FoxySheep is a collection of compiler technologies for **Wolf**_ram_ Language\*. In particular, FoxySheep...
* is an ANTLR4 lexer and parser grammar for Wolfram Language.
* is a Wolfram Language expression to FullForm expression translator. In other words, the FoxySheep parser has a visitor for the parse tree it produces that emits the FullForm of the parsed expression. The FullForm of an expression is a functionally equivalent form of the expression in a lisp-like expression format (`Head[arg1, arg2, ...]`). Thus FullForm is very easy to parse.
* includes a trimmed down lexer/parse for parsing FullForm expressions. Both Java and Python target languages are supported. Users can use Mathematica itself or some other Wolfram Language parser to produce a FullForm expression and then use FoxySheep's FullForm parser to read the result into their own programs.
* (Planned) is a FullForm to Python translator.

If you are here looking for a Wolfram Language parser for your project, jump down to [Similar Projects](#similar-projects).

\*In this document, Wolfram Language refers to the programming language used in Mathematica (and some other Wolfram Research products), and Mathematica refers to the computer algebra system (or its kernel) produced by Wolfram the company. FoxySheep and its author(s) are not affiliated with Wolfram.

## Motivation and Goals
For the Wolfram Language parser, I wanted something that is both fully functional and easy for students to understand, use in their own projects, modify, and contribute to. ANTLR4 is the perfect choice to achieve these goals. ANTLR4 produces parsers for Java, C#, Python 2&3, JavaScript, Go, C++, and Swift. The FoxySheep ANTLR4 grammars are language agnostic while the FullForm emitter comes in both Java and Python flavors. It would be easy to add support for another language.

For the Wolfram Language to Python translator, the goal is to be *useful*. My standard for usefulness is, it is sufficiently functional and easy to use that people, students especially, would want to use it to write simple programs in a Jupyter or Sage notebook.

Finally, for FoxySheep as a whole, my goal is that the project is helpful for students who are learning about compiler construction or Wolfram Language and helpful for me to learn how to teach those topics.

## Possible Uses for FoxySheep
You can use it to...

* write a pretty printer for Wolfram Language code.
* write a Wolfram Language code rewriter that inputs code written using nasty language constructs and outputs the same program but using saner notation. (Ever try to read someone else's crazy Wolfram Language code?)
* add support for Wolfram Language to your favorite open source computer algebra system to make a Mathematica clone.

FoxySheep doesn't...

* Execute Wolfram Language code
* Interact with Mathematica

But nothing is stopping *you* from using FoxySheep in your own project to do the above!

# Building
This section is incomplete.

You will need ANTLR4 installed and available in your path. To check this, check that you can run `antlr4` in a terminal.

## Python target

You will need the ANTLR4 Python runtime somewhere in your site-packages. To check this, run `python -c "import antlr4"` in a terminal and make sure you don't get an ImportError.

To generate the Python target:
```bash
cd python_target
make
```

# Project Status
FoxySheep is in heavy development. It is probably not yet ready to be used in your project. It needs a lot of testing and lacks some language features.

FoxySheep has complete coverage of non-box-related language features, and sketchy untested coverage of box-related features. While it is a goal of the project, FoxySheep does not always have identical behavior to Mathematica for the language constructs that it implements.

The table below summarizes the status of planned features.

<table style="table-layout: fixed; width: 100%">
<colgroup>
<col style="width: 30%;">
<col style="width: 12%;">
<col style="width: 58%;">
</colgroup>
  <tr>
    <th>Feature</th>
    <th>Status</th>
    <th>Comments</th>
  </tr>
  <tr>
    <td>Parses major language constructs</td>
    <td>complete</td>
    <td>The definition of "complete" and "major language constructs" is subjective. To be honest this needs auditing and testing.</td>
  </tr>
  <tr>
    <td>Parses box-related constructs</td>
    <td>started</td>
    <td>Low priority.</td>
  </tr>
  <tr>
    <td>Java target</td>
    <td>complete</td>
    <td>Target language dependent components of the parser written in java.</td>
  </tr>
  <tr>
    <td>Python target</td>
    <td>complete</td>
    <td>Target language dependent components of the parser written in python.</td>
  </tr>
  <tr>
    <td>FullForm emitter (java)</td>
    <td>complete</td>
    <td></td>
  </tr>
  <tr>
    <td>FullForm emitter (python)</td>
    <td>complete</td>
    <td></td>
  </tr>
  <tr>
    <td>Develop test suite</td>
    <td>not started</td>
    <td></td>
  </tr>
  <tr>
    <td>Translator to another HIL</td>
    <td>started</td>
    <td>Nontrivial impedance mismatch makes this a very complex task.</td>
  </tr>
</table>

# Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md).

# Similar Projects

Here's what the open source Wolfram Language parser landscape looks like:

* FoxySheep! A relatively complete, easy to understand, easy to hack parser and FullForm emitter.  And in the future, the only Wolfram Language translator to Python/Sage.
* [Mathematica IntelliJ Plugin](http://wlplugin.halirutan.de/). If you want a mature, well-tested Wolfram Language parser for your project and aren't concerned with the issues described under "Motivation and Goals" above, this parser is probably your best choice. This isn't just a syntax highlighter, it's a complete, mature Wolfram Language parser capable of emitting FullForm and doing various code analysis. The parser is a beautiful example of a Pratt parser, a top down operator precedence parsing strategy first described by Vaughan Pratt in the 70s.
* [Mathics](http://mathics.github.io/): A free, light-weight alternative to Mathematica created by Jan Pöschko. A Mathematica clone written in Python, Mathics includes a complete parser, FullForm emitter, and evaluator.
* [Mateusz Paprocki's Mathematica Parser in Scala](https://github.com/mattpap/mathematica-parser): "A library for parsing Mathematica's programming language written in Scala. It uses parser combinators and packrat parsers from Scala's standard library. Currently only a subset of Mathematica's language is supported."
* [MockMMA](https://sourceforge.net/projects/mockmma/): By [Richard Fateman](https://people.eecs.berkeley.edu/~fateman/) written in Lisp. This one's an old classic and of historical interest.
* [basicCAS](https://pypi.python.org/pypi/basicCAS/1.0): By Alex Gittens, a python Mathematica parser. It appears to have disappeared from the author's website, but it's still available elsewhere on the net for those interested in looking for it. This project is interesting because it includes Alex's notes regarding implementation.
* [omath](https://github.com/omath/omath) is similar in spirit to Mathics but is written in Java/Scala and appears to have had a 7 year hiatus from 2005 to 2012. The original parser "is mostly written by Yossi Farjoun, with some help from Scott Morrison" and is a generated parser using JavaCC and JJTree. There seems to be a newer parser written in Scala. The source code is distributed without a license. The historical repository lives at http://svn.omath.org/.
* [Symja-parser](https://github.com/axkr/symja-parser) is the Mathematica parser for [Symja - Java Computer Algebra Library](https://bitbucket.org/axelclk/symja_android_library/wiki/Home), "a general purpose Java library for symbolic mathematics" by Axel Kramer. Symja contains a Mathematica parser for a reasonable subset of Mathematica.

# Authors and License
Author(s): Robert Jacobson 

License: BSD license. See the file LICENSE.txt for details.