#### Table of Contents

* [What is FoxySheep?](#what-is-foxysheep)
* [Possible uses for FoxySheep](#possible-uses-for-foxysheep)
* [Project Status](#project-status)
* [Contributing](#contributing)
* [Authors and License](#authors-and-license)

# What is FoxySheep?
FoxySheep is a **Wolf**_ram_ Language ANTLR4 lexer and parser grammar. FoxySheep also has a visitor that emits FullForm expressions (essentially the parse tree but in a format that Mathematica can read and evaluate) and a trimmed down lexer/parse for parsing FullForm expressions. Both Java and Python target languages are supported.

In this document, Wolfram Language refers to the programming language used in Mathematica (and some other Wolfram Research products), and Mathematica refers to the computer algebra system (or its kernel) produced by Wolfram Research. FoxySheep and its author(s) are not affiliated with Wolfram Research.

# Possible Uses for FoxySheep
You can use it to...

* write a pretty printer for Wolfram Language code.
* write a Wolfram Language code rewriter that inputs code written using nasty language constructs and outputs the same program but using saner notation. (Ever try to read someone else's crazy Wolfram Language code?)
* add support for Wolfram Language to your favorite open source computer algebra system to make a Mathematica clone.

FoxySheep doesn't...

* Execute Wolfram Language code
* Interact with Mathematica

But nothing is stopping *you* from using FoxySheep in your own project to do the above!

# Building



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
If you want to contribute to the project, read CONTRIBUTING.md.

# Authors and License
Author(s): Robert Jacobson 

License: BSD license. See the file LICENSE.txt for details.