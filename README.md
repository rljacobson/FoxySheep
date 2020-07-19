<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [FoxySheep2](#foxysheep2)
- [Using](#using)
- [Regenerating the lexer/parser](#regenerating-the-lexerparser)
    - [FoxySheepLexer Must Subclass Lexer](#foxysheeplexer-must-subclass-lexer)

<!-- markdown-toc end -->
# FoxySheep2

This is the Robert Jacobson's Python implementation of the FoxySheep parser and lexer for Mathematica.
It has been stripped down and reorganized a bit.

In particular, the Java code has been removed. For that see the original [FoxySheep](https://github.com/rljacobson/FoxySheep) code base.

You need Python 3.6 or later to run this.

There are various `Makefile` targets for:

* setting up to run from the source tree
* running a canned set of Mathematics translations
* running an interactive translation session
* (re)-generating Python files from the grammar

To see a list of the target names for each of the above run `remake --tasks`.

# Uses

Right now the code can show the corresponding FullForm equivalent of Mathtematica InputForm. "InputForm" is the normal (shorter-for) text input that Mathematica accepts, while FullForm is a simpler, unabbreviated kind of text input that makes everything explicit and doesn't use abbreviation or non-ascii symbols. FullForm is closer to the kind of input that Mathematica works on internally.

Going further, you can get a grammar parse of Mathematica expressions and this may help you "parse" or understand a Mathematica expression. This may be useful in understand the precedence of operators or the association precedence when there are several operators and possibilities.

Going futher, we have some rudimentary translation to Python. Down the like there may be more sophisticated kinds of translation to other CAS input like Sage, or Axion/Fricas.

# Using

When installed, the command-line translator is called `foxy-sheep`:
To run the code interactively:

```
$ foxy-sheep
Enter a Mathematica expression. Enter either an empty line, Ctrl-C, or Ctrl-D to exit.
in:= 1+2
Plus[1,2]
in:=D[4 x^2]
D[Times[4,Power[x,2]]]
in:=
$
```

To see a demo after installed, run `python demo.py` in this directory.

# Regenerating the lexer/parser

To change the grammar you'll need the ANTLR Parser Generator (`antlr4)`, version 4.7.x  installed. If you don't want to change the grammar but just run the code, the distribution and git repository contain the antlr-derived Python files.

To (re)generate the lexer/parser:

```bash
$ make
```

The resulting files are placed in `FoxySheep/generated`.

Files generated by ANTLR4 are assumed to be in a subdirectory called `generated` containing an empty `__init__.py` file. See the Makefile for details.

## InputForm and FullForm must Subclass Lexer

In order for the generated antlr4 lexer to work we need to patch the generated Python lexers. The patch files do this.
The Makefile target for `FoxySheepParser.py` contains the `patch` command.

If patching is not done you'll get an `AttributeError` exception in the lexer when you try to run it such as through `foxy-sheep`.

An example error message looks like:

```
AttributeError: 'FoxySheepLexer' object has no attribute 'checkAdditiveOp'
```
