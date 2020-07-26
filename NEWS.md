1.1.0 2020-07-23
================

The main thrust here has been to start a translator to Python.
This is option `-o python`. There is a lot of low hanging fruit left to be picked.

We've added a number of options to the `foxy-sheep` command, aside from `-o python`. We've added showing the parse trees in two formats: `--tree=compact` and `--tree=full`. The former is for short expressions that aren't too complicated in nesting. The latter pretty prints the tree, indenting levels of nesting, numbers children and numbers children.

Examples
--------

```
$ foxy-sheep --tree=compact -e "3 (4+5)"
(prog (expr (expr (numberLiteral '3')) (expr '(' (expr (expr (numberLiteral '4')) '+' (expr (numberLiteral '5'))) ')')))
Times[3,Plus[4,5]]
```

```
$ foxy-sheep --tree=full -e "3 (4+5)"
0. prog[1]
  0. expr[2]
    0. expr[1]
      0. numberLiteral[1]
        '3'

    1. expr[3]
      '('

      1. expr[3]
        0. expr[1]
          0. numberLiteral[1]
            '4'

        1. '+'

        2. expr[1]
          0. numberLiteral[1]
            '5'

      1. ')'

Times[3,Plus[4,5]]
(prog (expr (expr (numberLiteral '3')) (expr '(' (expr (expr (numberLiteral '4')) '+' (expr (numberLiteral '5'))) ')')))
Times[3,Plus[4,5]]
```

Tests have been expanded and reorganized. We now use TravisCI for testing.

In all of the above bit more code reorganization was done so as to make this look more like a Python project. Recall this was part of a larger Python + Java project. As such it used Python-compatible but Java-like conventions. Some of that is still there, just less of it. And more Python-centric features are now used.

1.0.0 2020-07-15 One Oh!
========================

First PyPI Release!

This release is to bring to a wider audience Robert Jacobson's excellent FoxyParser for Mathematica.

We've removed the Java code and focused on Python packaging. Some code reorganization has been done.

A simple command-line utility called foxy-sheep has been added which will convert Mathematica InputForm to Mathematica FullForm without having Mathematica installed. To get help on that run foxy-sheep --help.

In the long term I hope to add translation to various CAS's like sage, SciPy, Axiom, Maxima, etc. Because internally there is a parse tree, I expect more sophisticated semantic analysis will be done.
