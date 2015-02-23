grammar FoxySheep;
import FoxySheepLexerRules;

@parser::members{
	/* TARGET LANGUAGE DEPENDENT CODE. */
	private boolean precededByPlusMinus(){
		int type = _input.LT(1).getType();
		return type != PLUS && type != MINUS;
	}
}

// PARSER RULES
expr
    :	NumberLiteral //numberLiteral
    |	pattern
    |	symbol
    |	StringLiteral
    |	outExpression
    |	slotExpression
    |	LPAREN expr RPAREN	//Grouping with parentheses
    |	LBRACE expressionList RBRACE	//List expression 
    |	expr LBRACKET expressionList RBRACKET //headedExpression
    |	expr accessExpression //accessor, i.e. a[[1]]
    |	expr DOUBLEPLUS //Increment
    |	expr DOUBLEMINUS	 //Decrement
    |	DOUBLEPLUS expr	//PreIncrement
    |	DOUBLEMINUS expr //PreDecrement
    |	<assoc=right> expr AT expr	 //application
    |	<assoc=right> expr (MAP | MAPALL | DOUBLEAT | TRIPPLEAT) expr	//Map[], MapAll[], Apply[e, e], Apply[e, e, {1}]
	|	expr (BANG | DOUBLEBANG) //Factorial, Double Factorial
	|	expr SINGLEQUOTE+ // Derivative[n][expr] where n counts the quotes.
	|	expr (LESSGREATER expr)+		//StringJoin
	|	<assoc=right> expr CARET expr	//Power
	|	INTEGRAL expr DIFFERENTIALD expr	//Integrate[]
	|	expr (CROSS expr)+	//Cross[]
	|	expr (DOT expr)+		//Dot[]
	|	MINUS expr	//Unary Minus
	|	PLUS expr	//Unary Plus
	|	expr DivisionSymbol expr	//Division, Divide[]
	|	expr { precededByPlusMinus() }? expr //Implicit multiplication, suppressed if second expr starts with '+'.
	|	expr MultiplicationSymbol expr (MultiplicationSymbol expr)* //Times[]
	|	expr (PLUS expr)+	//Plus[]
	|	expr MINUS expr	//Minus
	|	expr INTERSECTION expr //Set Intersection
	|	expr UNION expr	//Set Union
		// How do I do Span expressions?
		// http://reference.wolfram.com/language/ref/Span.html
//	|	expr? DOUBLESEMICOLON expr? (DOUBLESEMICOLON expr?) //Span
	|	expr ComparisonSymbol expr (ComparisonSymbol expr)* //Comparison
	|	expr SameComparisonSymbol expr (SameComparisonSymbol expr)* //SameQ, UnsameQ
	|	expr (ELEMENT | NOTELEMENT) expr // Set membership, Element[], NotElement[]
	|	expr (FORALL | EXISTS | NOTEXISTS) expr //Logical quantifiers
	|	(BANG | NOT) expr //Logical not
	|	expr LogicalAndSymbol expr (LogicalAndSymbol expr)* //Logical And/Nand
	|	expr LogicalXOrSymbol expr (LogicalXOrSymbol expr)* //Logical Xor/XNor
	|	expr LogicalOrSymbol expr (LogicalOrSymbol expr)* //Logical Or/Nor
	|	expr LRDOUBLEARROW expr (LRDOUBLEARROW expr)* //Logical equivalent
	|	<assoc=right> expr LogicalImpliesSymbol expr //Logical equivalent
	|	expr (DOUBLEDOT | TRIPPLEDOT)	//Repeated[] and RepeatedNull[]
	|	expr BAR expr	//Alternatives[]
	|	expr COLON expr ///Pattern[] and Optional[]
	|	expr DOUBLETILDE expr (DOUBLETILDE expr)* //StringExpression[]
	|	expr SLASHSEMI expr //Condition[]
	|	<assoc=right> expr (MINUSGREATER | RARROW | COLONGREATER | COLONARROW) expr //Rule/RuleDelayed
	|	expr (SLASHDOT | DOUBLESLASHDOT) expr //ReplaceAll[]/ReplaceRepeated[]
	|	<assoc=right> expr (PLUSEQUAL | MINUSEQUAL | STAREQUAL | SLASHEQUAL) expr // var += 1
	|	expr AMP	//Function[expr]
	|	expr EQUAL DOT	//Unset
	|	<assoc=right> expr (EQUAL | COLONEQUAL | CARETEQUAL | CARETCOLONEQUAL | FUNCTIONARROW) expr //Set[], SetDelayed[], etc.
	|	<assoc=right> symbol SLASHCOLON expr (EQUAL | COLONEQUAL) (expr | DOT)	//TagSet
	|	expr SEMICOLON (expr SEMICOLON)* expr? //CompoundExpression
    ;

//Symbols and Contexts
symbol
	: context? Name
	;

context
	: BACKQUOTE? Name BACKQUOTE
	| Name BACKQUOTE Name BACKQUOTE
	;

pattern
	:	symbol? (TRIPPLEBLANK | DOUBLEBLANK | BLANK) expr?
	|	symbol? BLANKDOT
	;

outExpression
	:	PERCENT DIGITS
	|	PERCENT+
	;

slotExpression
	:	HASH DIGITS
	|	HASH StringLiteral
	|	DOUBLEHASH DIGITS
	|	DOUBLEHASH
	|	HASH
	;

// List-like expressions

expressionList // Can be empty.
	:	expr? (COMMA expr?)*
	;


// Accessor is used to access parts of an expression, i.e. a[[1]]
accessExpression
	:	LBRACKET LBRACKET expr RBRACKET RBRACKET
	|	LBARBRACKET expr RBARBRACKET
	;


