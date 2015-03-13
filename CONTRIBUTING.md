# Ways to contribute
Here are some ideas:

* Find an input for which FoxySheep and Mathematica give differing `FullForm`'s and document it in a new ticket.
* Align lexical names to Mathematica. 
* Implement a FullFormEmitter in a new target language. ANTLR4 can currently target Java, C#, Python 2&3, and JavaScript.
* Implement a translator to your favorite CAS's input language.
* Implement a symantic analyzer (in your favorite target language). This is often left for run time, but some analysis can be done at parse time (or immediately following parsing, as it were).
* Implement error recovery rules. (This is best left to experienced developers.)
* Improve the parsing of number literals by bringing the number literal rule from the lexer to the parser. The parser should extract the base, etc. As it stands, the parser treats the number literal as a string blob, so any further analysis must parse the blog. 

Or fix some current known bugs:

* Fix the string literal parsing rules so they parse Wolfram Language string literals. (Currently string literals are implemented incorrectly with lexer rules.)
* Newlines are not treated the same way as they are in Mathematica.
* There is a weird bug affecting parsing number literals that needs squashing. 
* Implicit multiplication is fragile and occassionally breaks when changes are made to the grammar. Test implicit multiplication, and if it doesn't work correctly, fix it.

# Finding your way through the source grammar
The lexer rules are implemented in `FoxySheepLexerRules.g4`, while the parser rules are in `FoxySheep.g4`. Most of the action in the FoxySheep grammar happens in the `expr` production rule. The grammar relies on ANTLR to implement correct operator precedence according to the order of the alternatives.

ANTLR generates a parse tree, but the tree needs to be walked using the PostParser listener (implemented in `src/PostParser.java`) which restructures the parse tree to flatten some of the operators.

The FullForm emitter is a visitor class. It is implemented in `src/PostParser.java`.

#Target language dependent code
The project attempts to keep target language dependent code to a minimum. However, there is minimal target language dependent code embedded in `FoxySheepLexerRules.g4` to disambiguate unary plus/minus from binary plus/minus which in turn makes implicit multiplication possible. This code is written in Java, but it should be trivial to port it to another target language.

The FullForm emitter and PostParser are written in Java. FullForm emitters for other target languages are planned—in fact, that would be a great way for you to contribute! 

#Where is Wolfram Language documented?
There is no official grammar available. However, the language is described in detail in a few documents published on Wolfram Research's website.

| Document | Description |
|----------|-------------|
| [Operator Input Forms](http://reference.wolfram.com/language/tutorial/OperatorInputForms.html) | Describes the majority of the Wolfram Language syntax, including operator precedence and associativity. |
| [Wolfram Language Syntax](http://reference.wolfram.com/language/guide/Syntax.html) | A "big picture" overview of the syntax, much more terse than the above document. |
| [Input Syntax](http://reference.wolfram.com/language/tutorial/InputSyntax.html) | Detailed descriptions of syntax for numeric literals, strings, symbols and contexts, and other language constructs. |
| [Special Characters](http://reference.wolfram.com/language/tutorial/SpecialCharacters-MathematicalAndOtherNotation.html) | A description of how special characters work in Mathematica. This is useful in dealing with operators involving special symbols. |
| [Listing of Named Characters](http://reference.wolfram.com/language/guide/ListingOfNamedCharacters.html) | Lists all of the special characters Mathematica has a name for. This is useful when working with operators involving special symbols. |

#Special symbols
Special symbols are just unicode characters. No non-ascii characters should appear in the code itself. Use escape codes instead. Mathematica provides a database of named characters here: `.../SystemFiles/FrontEnd/TextResources/UnicodeCharacters.tr`.

#Helpful Mathematica code snippets

###Get the \uxxxx unicode string for a character
`"\\u" <> TextString[BaseForm[ToCharacterCode["\[And]"][[1]], 16]]` 

###Get Mathematica's "name" of a special character
`FullForm["\[And]"]`

###Get Mathematica to give you a syntax tree of an arbitrary expression.
`FullForm` also gives what is essentially a syntax tree of any Wolfram Language expression. For example,

```
In[1]:=  FullForm[Hold[Plus@Integrate[#, x] & /@ {x^2, x - 1/x}]]
Out[1]= FullForm[Hold[Map[Function[Plus[Integrate[Slot[1], x]]], {Power[x, \
2], Plus[x, Times[-1, Times[1, Power[x, -1]]]]}]]]
```

You will notice, however, that `FullForm` retains the list syntax `{...}`. The `Hold` is necessary. It's helpful to pass the output of `FullForm` to `TextString` so that you can copy+paste the output: `TextString[FullForm[Hold[ expression ]]]`.

#Code conventions

Parser rules go in `FoxySheep.g4` while lexer rules go in `FoxySheepLexerRules.g4`.

A readable and correct grammar is much more important than a grammar which produces a fast lexer/parser.

Unless you have a compelling reason to do otherwise, you should prefer to write<br>
```
	 |	expr (OPTOKENA | OPTOKENB | OPTOKENC) expr 
```
<br>for three infix operators having the same precedence instead of the three lines

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

#Mathematica oddities
Command line Mathematica and Notebook Mathematica produce different output for `FullForm[Hold[3x^2-+2x + - -1]]`. Looks like the notebook doesn't properly flatten `Times[]`. Why the notebook has a different parser than the command line is a mystery.

The Mathematica parser does not correctly hold the multiplication by -1 with number literals: `FullForm[Hold[1-2]]` gives `Plus[1, -2]`, whereas `FullForm[Hold[a-b]]` gives `Plus[a, Times[-1,b]]`.