1.0.0 2020-07-15
================

First PyPI Release!

This release is to bring to a wider audience Robert Jacobson's excellent FoxyParser for Mathematica.

We've remove the Java code and focused on Python packaging. Some code reorganization has been done.

A simple command-line utility called `foxy-parser` has been added which will convert [Mathematica InputForm](https://reference.wolfram.com/language/ref/InputForm.html) to [Mathematica FullForm](https://reference.wolfram.com/language/ref/FullForm.html) without having Mathematica installed. To get help on that run ``foxy-parser --help``.

In the long term I hope to add translation to various CAS's like sage, SciPy, Axiom, Maxima, etc. Because internally there is a parse tree, I expect more sophisticated semnatic analysis will be done.
