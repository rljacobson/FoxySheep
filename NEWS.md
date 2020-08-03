1.2.2 2020-08-03
================

* in `foxy-sheep`:
  - Start output modes `--output=numpy` and `--output=sympy`
  - Add file reader `--file` and add StackExchance Mathematica example
  - In/Out indexing is 1 origin now
  - Range[...] now is list(range(...))
* Handle the simplest form of `Table[]` with range - it is a list comprehension
* Handle fullform function equivalents like `Plus[]` and `Times[]`
* Fill in many more trigonomentric functions and add `I` variable.

1.2.1 2020-08-02
================

* Handle numberLiteral with numberLiteralExponent. See https://mathematica.stackexchange.com/questions/85445/convert-mathematica-math-expression-form-to-python-math-expression/226648?noredirect=1#comment576795_226648
* Add `--debug`, (`-d`) option to show pretty-printed AST (via [`astpretty`](https://pypi.org/project/astpretty/))
* Add subscripting lists; this means we handle origin 1 vs. origin 0 indexing
* More tests

1.2.0 2020-07-28
================

Start saving state in REPL so `%` works

Revise pretty printer to include specific transformation names. For example:

```
$ foxy-sheep --tree=compact -e "3 (4+5)"
(<prog:Prog>  (<expr:Times>  (<expr:Number>  (<numberLiteral:NumberBaseTen>  '3')) (<expr:Parentheses>  '(' (<expr:PlusOp>  (<expr:Number>  (<numberLiteral:NumberBaseTen>  '4')) '+' (<expr:Number>  (<numberLiteral:NumberBaseTen>  '5'))) ')')))
Times[3,Plus[4,5]]

$ foxy-sheep --tree=full -e "3 (4+5)"
<prog:Prog> [1]
  <expr:Times> [2]
    0. <expr:Number> [1]
      <numberLiteral:NumberBaseTen> [1]
        '3'

    1. <expr:Parentheses> [3]
      '('

      1. <expr:PlusOp> [3]
        0. <expr:Number> [1]
          <numberLiteral:NumberBaseTen> [1]
            '4'

        1. '+'

        2. <expr:Number> [1]
          <numberLiteral:NumberBaseTen> [1]
            '5'

      1. ')'

Times[3,Plus[4,5]]
```

Compare with 1.1.0 shown in those release notes.

We now translate lists, and a few function names, namely `GCD` and `Sin`. Right now full coverage isn't as important as trying to get the framework correct.

Some bugs were fixed.


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
