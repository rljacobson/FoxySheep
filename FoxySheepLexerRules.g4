lexer grammar FoxySheepLexerRules;

// LEXER RULES

// Identifiers/Names
Name
	:	LetterForm+ LetterFormOrDigit*
	;
	
//Too many fragments in this section?
fragment
LetterFormOrDigit :	LetterForm | DIGIT ;
fragment
LetterForm	: Letter | Letterlike ;
fragment
Letter : [a-zA-Z\u00c0-\u00d6\u00d8-\u00f6\u00f8-\u0103\u0106\u0107\u010c-\u010f\u0112-\u0115\u011a-\u012d\u0131\u0141\u0142\u0147\u0148\u0150-\u0153\u0158-\u0161\u0164\u0165\u016e-\u0171\u017d\u017e\u0391-\u03a1\u03a3-\u03a9\u03b1-\u03c9\u03d1\u03d2\u03d5\u03d6\u03da-\u03e1\u03f0\u03f1\u03f5\u210a-\u210c\u2110-\u2113\u211b\u211c\u2128\u212c\u212d\u212f-\u2131\u2133-\u2138\uf6b2-\uf6b5\uf6b7\uf6b9\uf6ba-\uf6bc\uf6be\uf6bf\uf6c1-\uf700\uf730\uf731\uf770\uf772\uf773\uf776\uf779\uf77a\uf77d-\uf780\uf782-\uf78b\uf78d-\uf78f\uf790\uf793-\uf79a\uf79c-\uf7a2\uf7a4-\uf7bd\uf800-\uf833\ufb01\ufb02];
fragment
Letterlike : [\u0024\u00a1\u00a2\u00a3\u00a5\u00a7\u00a9\u00ab\u00ae\u00b0\u00b5\u00b6\u00b8\u00bb\u00bf\u02c7\u02d8\u2013\u2014\u2020\u2021\u2022\u2026\u2032\u2033\u2035\u2036\u2060\u20ac\u210f\u2122\u2127\u212b\u21b5\u2205\u221e\u221f\u2220\u2221\u2222\u22ee\u22ef\u22f0\u22f1\u2300\u2318\u231a\u23b4\u23b5\u2500\u2502\u25a0\u25a1\u25aa\u25ae\u25af\u25b2\u25b3\u25bc\u25bd\u25c0\u25c6\u25c7\u25cb\u25cf\u25e6\u25fb\u25fc\u2605\u2639\u263a\u2660\u2661\u2662\u2663\u266d\u266e\u266f\u2736\uf3a0\uf3b8\uf3b9\uf527\uf528\uf720\uf721\uf722\uf723\uf725\uf749\uf74a\uf74d\uf74e\uf74f\uf750\uf751\uf752\uf753\uf754\uf755\uf756\uf757\uf760\uf763\uf766\uf768\uf769\uf76a\uf76b\uf76c\uf7d4\uf800\uf801\uf802\uf803\uf804\uf805\uf806\uf807\uf808\uf809\uf80a\uf80b\uf80c\uf80d\uf80e\uf80f\uf810\uf811\uf812\uf813\uf814\uf815\uf816\uf817\uf818\uf819\uf81a\uf81b\uf81c\uf81d\uf81e\uf81f\uf820\uf821\uf822\uf823\uf824\uf825\uf826\uf827\uf828\uf829\uf82a\uf82b\uf82c\uf82d\uf82e\uf82f\uf830\uf831\uf832\uf833\ufe35\ufe36\ufe37\ufe38];

//Number Representations
NumberLiteral
	//You can omit number before or number after decimal, but not both.
	:	(	(DIGITS DOUBLECARET (DigitInAnyBase+ DOT? DigitInAnyBase* | DigitInAnyBase* DOT? DigitInAnyBase+))
           |	(DIGITS DOT? DIGIT*  |  DIGIT* DOT? DIGITS)
        )
        (DOUBLEBACKQUOTE? (PLUS|MINUS)? (DIGIT+ DOT? DIGIT* | DIGIT* DOT? DIGIT+)|BACKQUOTE)? // Precision / Accuracy
        (ASTERISKCARET (PLUS|MINUS)? DIGIT+)? // Exponent
	;
	
DIGITS : DIGIT+;
fragment
DIGIT	: [0-9];
fragment
DigitInAnyBase
	:	DIGIT
	|	[a-zA-Z]
	;

//String Literal
//TODO: This section is not correct. It does not match "Hello,\- world!" which is a valid string.
//		Mathics has similar issues, e.g. doesn't match "Hello,\ world!"
StringLiteral
    :   QUOTE StringCharacters? QUOTE
    ;

fragment
StringCharacters
    :   StringCharacter+
    ;

fragment
StringCharacter
    :   ~["\\]
    |   EscapeSequence
    ;
    
// Escape Sequences for Character and String Literals
fragment
EscapeSequence
    :   RAWBACKSLASH [btnfr"'\\]
    |   UnicodeEscape
    ;

fragment
UnicodeEscape
    :   RAWBACKSLASH RAWCOLON HexDigit HexDigit HexDigit HexDigit
    ;
    
fragment
HexDigit
    :   [0-9a-fA-F]
    ;

//Comments
COMMENT
	:	LCOMMENT .*? RCOMMENT -> skip
	; 

// Separators and brackets

LPAREN      : '(';
RPAREN      : ')';
LBRACE      : '{';
RBRACE      : '}';
LBRACKET      : '[';
RBRACKET      : ']';
COMMA       : ',';
LCOMMENT		: '(*';
RCOMMENT		: '*)';
LANGLE		: '\u2329'; //Angled brackets <
RANGLE		: '\u232a'; //Angled brackets >
LFLOOR		: '\u230a';
RFLOOR		: '\u230a';
DOUBLEBAR	: '||';
BAR			: '|';
//BARBAR	: '\uf607'; //Single character version of ||
LBARBRACKET		: '\u301a'; //Single character version of [[
RBARBRACKET		: '\u301b'; //Single character version of ]]

//Quote Characters
DOUBLEBACKQUOTE	: '``';
BACKQUOTE	: '`';
SINGLEQUOTE	: '\'';
QUOTE		: '"';

// File I/O operators.
DOUBLELESS		: '<<';
TRIPPLEGREATER	: '>>>';
DOUBLEGREATER	: '>>';

//Comparison symbols

SameComparisonSymbol
	:	TRIPPLEEQUAL
	|	EQUALBANGEQUAL
	;
TRIPPLEEQUAL		: '===';
EQUALBANGEQUAL	: '=!=';

ComparisonSymbol
	:	LONGEQUAL
	|	DOUBLEEQUAL
	|	EQUAL
	|	BANGEQUAL
	|	GREATEREQUAL
	|	GREATER
	|	GREATEREQUALSYMBOL
	|	GREATERSLANTEQUALSYMBOL
	|	LESSEQUAL
	|	LESS
	|	LESSEQUALSYMBOL
	|	LESSSLANTEQUALSYMBOL
	;
LONGEQUAL	: '\uf7d9';
DOUBLEEQUAL	: '==';
EQUAL		: '=';
BANGEQUAL	: '!=';
GREATEREQUAL	: '>=';
GREATER		: '>';
GREATEREQUALSYMBOL	: '\u2265';
GREATERSLANTEQUALSYMBOL	: '\u2a7e';
LESSEQUAL	: '<=';
LESS			: '<';
LESSEQUALSYMBOL	: '\u2264';
LESSSLANTEQUALSYMBOL	: '\u2a7d';

VerticalBarSymbol
	:	VERTICALBAR
	|	NOTVERTICALBAR
	|	DOUBLEVERTICALBAR
	|	NOTDOUBLEVERTICALBAR
	;
VERTICALBAR	: '\uf3d0';
NOTVERTICALBAR	: '\uf3d1';
DOUBLEVERTICALBAR	: '\u2225';
NOTDOUBLEVERTICALBAR	: '\u2226';

//Symbols related to set theory
SetContainmentSymbol
	:	ELEMENT
	|	NOTELEMENT
	|	SUBSET
	|	SUPERSET
	;
ELEMENT		: '\u2208'; // \in
NOTELEMENT	: '\u2209'; // \not\in
SUBSET		: '\u2282';
SUPERSET		: '\u2283';

//Symbols related to predicate calculus
/* ForAll and friends require subscripts, i.e., are not text-based commands.
FORALL		: '\u2200'; //Universal quantifier A
EXISTS		: '\u2203'; //Existential quantifier E
NOTEXISTS	: '\u2204'; //Existential quantifier with a slash
*/
NOT	: '\u00ac'; //Logical not, \neg

LogicalAndSymbol
	:	DOUBLEAMP
	|	AND
	|	NAND
	;
DOUBLEAMP	: '&&';
AND			: '\u2227'; //Logical and, \wedge
NAND			: '\u22bc'; //Logical "not and"

LogicalXOrSymbol
	:	XOR
	|	XNOR
	;
XOR		: '\u22bb'; //Logical xor
XNOR		: '\uf4a2'; //Logical xnor

LogicalOrSymbol
	:	OR
	|	NOR
	;
OR	: '\u2228';
NOR	: '\u22bd';

LRDOUBLEARROW	: '\u29e6';

LogicalImpliesSymbol
	:	RDOUBLEARROW
	|	LCONTAINS
	;
RDOUBLEARROW		: '\uf523';
LCONTAINS		: '\u2970';

RightTeeSymbol
	:	RIGHTTEE
	|	DOUBLERIGHTTEE
	;
RIGHTTEE			: '\u22a2';
DOUBLERIGHTTEE	: '\u22a8';

TeeSymbol
	:	LEFTTEE
	|	DOUBLELEFTTEE
	|	UPTEE
	|	DOWNTEE
	;
LEFTTEE	: '\u22a3';
DOUBLELEFTTEE	: '\u2ae4';
UPTEE	: '\u22a5';
DOWNTEE	: '\u22a4';

SUCHTHAT		: '\u220d';
THEREFORE	: '\u2234';
BECAUSE		: '\u2235';

// Pattern related symbols
TRIPPLEDOT	: '...';
DOUBLEDOT	: '..';

QUESTIONMARK	: '?';

TRIPPLEBLANK	: '___';
DOUBLEBLANK	: '__';
BLANKDOT		: '_.';
BLANK		: '_';

DOUBLEHASH	: '##';
HASH : '#';

PERCENT	: '%';

DOUBLECOLON	: '::';
RAWCOLON	: ':';
DOUBLETILDE	: '~~';
SLASHSEMI	: '/;';

MINUSGREATER		: '->';
RARROW			: '\uf522';
COLONGREATER		: ':>';
COLONARROW		: '\uf51f';

SLASHDOT			: '/.';
DOUBLESLASHDOT	: '//.';

// Symbols related to setting/assignment
PLUSEQUAL	: '+=';
MINUSEQUAL	: '-=';
ASTERISKEQUAL	: '*=';
SLASHEQUAL	: '/=';

AMP	: '&';

COLONEQUAL	: ':=';
CARETEQUAL	: '^=';
CARETCOLONEQUAL	: '^=';
SLASHCOLON	: '^=';
FUNCTIONARROW	: '\uf4a1';

// Other Operators and Characters 
DOT         : '.';
DOUBLECARET	: '^^';
CARET		: '^';
ASTERISKCARET	: '*^';
DOUBLEPLUS	: '++';
PLUS			: '+';
DOUBLEMINUS	: '--';
MINUS		: '-';
TRIPPLEAT	: '@@@';
DOUBLEAT		: '@@';
ATASTERISK	: '@*';
AT	: '@';
MAP	: '/@';
SLASHASTERISK	: '/*';
MAPALL	: '//@';
DOUBLEBANG	: '!!';
BANG		: '!';
LESSGREATER	: '<>';
INTEGRAL		: '\u222b';
DIFFERENTIALD	: '\uf74C'; //Blackboard bold d
CROSS	: '\uf4a0'; //Cross product x.
RAWBACKSLASH		: '\\';
INTERSECTION		: '\u22c2'; //  $\cup$
UNION			: '\u22c3'; //  $\cap$
DOUBLESEMICOLON	: ';;';
SEMICOLON        : ';';
TRANSPOSE	: '\uf3c7'; //T
CONJUGATETRANSPOSE	: '\uf3c9'; //cross
HERMITIANCONJUGATE	: '\uf3ce'; //H
CONJUGATE	: '\uf3c8'; //Star
TILDE	: '~';
DEL		: '\u2207'; //Nabla
SQUARE	: '\uf520';
SMALLCIRCLE	: '\u2218';
CIRCLEDOT	: '\u2299';
DOUBLEASTERISK	: '**';
PLUSMINUS	: '\u00b1';
MINUSPLUS	: '\u2213';
BACKSLASH	: '\u2216'; //That's right: the name backslash does not refer to the ascii character.
DIAMOND		: '\u22c4';
WEDGE		: '\u22c0';
VEE			: '\u22c1';
CIRCLETIMES	: '\u2297';
CENTERDOT	: '\u00b7';
STAR		: '\u22c6'; //That's right: the name star does not refer to the identical glyph asterisk.
VERTICALTILDE	: '\u2240';
COPRODUCT	: '\u2210';
CAP			: '\u2322';
CUP			: '\u2323';
CIRCLEPLUS	: '\u2295';
CIRCLEMINUS	: '\u2296';
COLON		: '\u2236'; //That's right: the name colon does not refer to the identical ascii character.
DOUBLESLASH	: '//';
VERTICALSEPARATOR	: '\uf432';

//Box related tokens.
//These are special because they can only occur in a box.
FormBox	: '\\`';
InterpretedBox	: '\\!';
BoxFraction	: '\\/';
BoxLeftBoxParenthesis	:	'\\(';
BoxOtherscript	: '\\%';
BoxOverscript	: '\\&';
BoxRightBoxParenthesis	:  '\\)';
BoxSqrt	: '\\@';
BoxSubscript	: '\\_';
BoxSuperscript	: '\\^';
BoxUnderscript	: '\\+';
BoxConstructor	: '\\*';

//Division symbols
SLASH	: '/';
DIVIDE	: '\u00f7'; //Division symbol (obelus)

//Multiplication symbols
MultiplicationSymbol
	:	ASTERISK
	|	TIMES
	;
ASTERISK		: '*';
TIMES	: '\u00d7';


//Whitespace
WHITESPACE  :   [ \t\r\n]+ -> skip ;
