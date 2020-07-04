#### Table of Contents

  * [Ways to contribute](#ways-to-contribute)
  * [Finding your way through the source grammar](#finding-your-way-through-the-source-grammar)
  * [Target language dependent code](#target-language-dependent-code)
  * [Code conventions](#code-conventions)
  * [Where is Wolfram Language documented?](#where-is-wolfram-language-documented)
  * [Helpful Mathematica code snippets](#helpful-mathematica-code-snippets)
      * [Get the \\uxxxx unicode string for a character](#get-the-uxxxx-unicode-string-for-a-character)
      * [Get Mathematica's "name" of a special character](#get-mathematicas-name-of-a-special-character)
      * [Get Mathematica to give you a syntax tree of an arbitrary expression\.](#get-mathematica-to-give-you-a-syntax-tree-of-an-arbitrary-expression)
  * [Mathematica oddities](#mathematica-oddities)
    * [Context resolution](#context-resolution)
    * [Differences between notebook and command line](#differences-between-notebook-and-command-line)
    * [Number literals](#number-literals)

# Ways to contribute

## Write unit tests

Write a unit test (or doctest for the Python target)  for every function in the `FullFormEmitter` or `PostParser`.

Write some automated tests comparing the equivalence of Mathematica's output to FoxySheep.

## Add new features.

Here are some ideas:

* Find an input for which FoxySheep and Mathematica give differing `FullForm`'s and document it in a new ticket.
* Align lexical names to Mathematica.
* Implement parsing of "special input":
	http://reference.wolfram.com/language/tutorial/InputSyntax.html
* Implement a FullFormEmitter in a new target language. As of April, 2017, ANTLR4 can currently target Java, C#, Python 2&3, JavaScript, Go, C++, and Swift. See the [ANTLR4 docs](https://github.com/antlr/antlr4/blob/master/doc/targets.md) for up-to-date information about target languages.
* Implement a translator to your favorite CAS's input language.
* Implement a semantic analyzer (in your favorite target language).
* Implement error recovery rules. (This is best left to experienced developers.)
* Create a new option. Here are some ideas:
  * An option affecting parsing of subtraction: to automatically simplify `Times[-1, a]` to `-a` in the case that `a` is a number literal; to output `Subtract[a, b]` for `a-b`; to emulate Mathematica.
  * An option for `PostParser` to flatten functions having the `Flat` attribute (`Attributes[name]` contains `Flat`). Similarly for `OneIdentity`.
  * An option specifying some translation behavior.

## Fix bugs:

See [Known Bugs](KnownBugs.md).

# Finding your way through the source grammar
The lexer rules are implemented in [`FoxySheepLexerRules.g4`](FoxySheepLexerRules.g4), while the parser rules are in [`FoxySheep.g4`](FoxySheep.g4). Most of the action in the FoxySheep grammar happens in the `expr` production rule. The grammar relies on ANTLR to implement correct operator precedence according to the order of the alternatives.

ANTLR generates a parse tree, but the tree needs to be walked using the PostParser listener (implemented in [`src/PostParser.java`](java_target/src/PostParser.java) and [`FoxySheep/PostParser.py`](python_target/FoxySheep/PostParser.py)) which restructures the parse tree to flatten some of the operators.

The FullForm emitter is a visitor class. It is implemented in [`src/FullFormEmitter.java`](java_target/src/FullFormEmitter.java) and [`FoxySheep/FullFormEmitter.py`](python_target/FoxySheep/FullFormEmitter.py).

# Target language dependent code in the grammar
The project attempts to keep target language dependent code in the grammar to a minimum. There is minimal target language dependent code embedded in [`FoxySheepLexerRules.g4`](FoxySheepLexerRules.g4) that is written to be both valid Java and valid Python. It should be trivial to port this code to another target language. This code can be found:

 * In every bracket-like lexer rule.
 * In the actions on the PLUS, MINUS, PLUSMINUS, and MINUSPLUS lexer rules.
 * In the action on DOUBLESEMICOLON ";;".
 * In the NEWLINE action.

To make this embedded target language dependent code work, we put supporting member functions in a superclass that the generated lexer subclasses. 

There is a post parser and FullForm emitter for Java and Python. Creating these classes for another target language would be a great way for you to contribute! 

# Code conventions

Parser rules go in [`FoxySheep.g4`](FoxySheep.g4) while lexer rules go in [`FoxySheepLexerRules.g4`](FoxySheepLexerRules.g4).

A readable and correct grammar is much more important than a grammar which produces a fast lexer/parser.

Unless you have a compelling reason to do otherwise, you should prefer to write
```
        |	expr (OPTOKENA | OPTOKENB | OPTOKENC) expr
```
for three infix operators having the same precedence instead of the three lines
```
        |	expr OPTOKENA expr
        |	expr OPTOKENB expr
        |	expr OPTOKENC expr
```
which forces an arbitrary and artificial precedence on the operators.

Use a lexer rule when the object is treated as a monolithic "chunk" by the parser. Use a parser rule when the object needs to be taken apart and inspected by the parser, that is, when the parser "cares" about the individual pieces on the RHS of the rule.

Maximize the use of `fragment` in lexer rules.

Use named tokens.

Tokens that are string literals or character classes are in all caps. Tokens that are regular expressions or rules are in CamelCase. (If someone wants to go through and regularize the naming, go for it.)

Special symbols are just unicode characters. No non-ascii characters should appear in the code itself. Use escape codes instead. Mathematica provides a database of named characters here: `.../SystemFiles/FrontEnd/TextResources/UnicodeCharacters.tr`.



# Where is Wolfram Language documented?
There is no official grammar available. However, the language is described in detail in a few documents published on Wolfram Research's website.

| Document | Description |
|----------|-------------|
| [Operator Input Forms](http://reference.wolfram.com/language/tutorial/OperatorInputForms.html) | Describes the majority of the Wolfram Language syntax, including operator precedence and associativity. |
| [Wolfram Language Syntax](http://reference.wolfram.com/language/guide/Syntax.html) | A "big picture" overview of the syntax, much more terse than the above document. |
| [Input Syntax](http://reference.wolfram.com/language/tutorial/InputSyntax.html) | Detailed descriptions of syntax for numeric literals, strings, symbols and contexts, and other language constructs. |
| [Special Characters](http://reference.wolfram.com/language/tutorial/SpecialCharacters-MathematicalAndOtherNotation.html) | A description of how special characters work in Mathematica. This is useful in dealing with operators involving special symbols. |
| [Listing of Named Characters](http://reference.wolfram.com/language/guide/ListingOfNamedCharacters.html) | Lists all of the special characters Mathematica has a name for. This is useful when working with operators involving special symbols. |

Mathematica includes facilities in the language itself to describe the syntax, options, messages, etc., of functions. The most important functions that do this are given below.

| Document | Description |
|----------|-------------|
| [`SyntaxInformation`](http://reference.wolfram.com/language/ref/SyntaxInformation.html) | Gives "ArgumentPattern" and other syntax properties of built-in functions. |
| [`WolframLanguageData`](http://reference.wolfram.com/language/ref/WolframLanguageData.html) | Can be used to query a database of a variety of information on Wolfram Language symbols, including many—but not all—of the information that these other functions produce. |
| [`Definition`](http://reference.wolfram.com/language/ref/Definition.html) | Prints out attributes, defaults, options, and, for user defined functions, definitions (*-`Values`).
| `OwnValues` | Gives a symbol's OwnValues. |
| `DownValues` | `DownValues` are a symbols function definitions. |
| `UpValues` | Like `DownValues`, but more obscure. |
| `Defaults` | Default values for function arguments. |
| [`Attributes`](http://reference.wolfram.com/language/ref/Attributes.html) | Gives "attributes" of a function, i.e. whether the function is listable, flat, etc. |
| [`Messages`](http://reference.wolfram.com/language/ref/Messages.html) | Gives all messages associated to a function. |


# Helpful Mathematica code snippets

### Get the \uxxxx unicode string for a character
`"\\u" <> TextString[BaseForm[ToCharacterCode["\[And]"][[1]], 16]]` 

### Get Mathematica's "name" of a special character
`FullForm["\[And]"]`

### Get Mathematica to give you a syntax tree of an arbitrary expression.
`FullForm` also gives what is essentially a syntax tree of any Wolfram Language expression. For example,

    In[1]:=  FullForm[Hold[Plus@Integrate[#, x] & /@ {x^2, x - 1/x}]]
    Out[1]= Hold[Map[Function[Plus[Integrate[Slot[1],x]]],
    List[Power[x,2],Plus[x,Times[-1,Times[1,Power[x,-1]]]]]]]

The `Hold` is necessary. It's helpful to pass the output of `FullForm` to `TextString` so that it's easier to copy+paste the output: `TextString[FullForm[Hold[ expression ]]]`.
