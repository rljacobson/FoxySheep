[TOC]:
# FoxySheep2

This is the Robert Jacobson's Python implementation of the FoxySheep parser and lexer for Mathematica.
It has been stripped down and reorganized a bit.

In particular, the Java code has been removed. For that see the original [FoxySheep](https://github.com/rljacobson/FoxySheep) code base.

You need Python 3.6 or later to run this.

To change the grammar you'll need the ANTLR Parser Generation version 4.7.x (`antlr4)` installed. However the git repo currently contains the antlr-derived Python files. This may change in the future.

There are varous Makefile targets for:

* setting up to run from the source tree
* running a canned set of Mathematics translations
* running an interactive translation session
* (re)-generating Python files from the grammar

To see a list of the target names for each of the above run `remake --tasks`.

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

To (re)generate the lexer/parser:

```bash
$ make
```

The resulting files are placed in `FoxySheep/generated`.

Files generated by ANTLR4 are assumed to be in a subdirectory called `generated` containing an empty `__init__.py` file. See the Makefile for details.

## FoxySheepLexer Must Subclass Lexer

In order for the generated antlr4 lexer to work we need to patch the generated Python lexer `FoxySheep.lexer.py`; The patch file `FoxySheep.lexer.py.patch` does this.
The Makefile target for `FoxySheepParser.py` contains the `patch` command.

If patching is not done you'll get an `AttributeError` exception in the lexer you try to run it such as through `foxy-sheep`.

```
AttributeError: 'FoxySheepLexer' object has no attribute 'checkAdditiveOp'
```
