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

//expressions : expr ('\n' expr)*;

expr
    :	NumberLiteral //numberLiteral
    |	symbol
    |	StringLiteral
    |	LPAREN expr RPAREN	//Grouping with parentheses
    |	LBRACE expressionList RBRACE	//List expression
    |	expr DOUBLECOLON StringLiteral (DOUBLECOLON StringLiteral)? // MessageName[]
    |	slotExpression // "forms containing #"
    |	outExpression // "forms containing %"
    |	pattern // "forms containing _"
    |	DOUBLELESS StringLiteral // Get[]

	|	BoxLeftBoxParenthesis box* BoxRightBoxParenthesis
	//TODO: Finish and test box related grammar.

	|	expr QUESTIONMARK expr
    |	expr LBRACKET expressionList RBRACKET //headedExpression
    |	expr accessExpression //accessor, i.e. a[[1]]
    |	BoxConstructor expr
    |	expr (DOUBLEPLUS | DOUBLEMINUS) //Increment/Decrement
    |	(DOUBLEPLUS | DOUBLEMINUS) expr	//PreIncrement/PreDecrement
    |	expr (ATASTERISK expr)+ //Composition
    |	expr (SLASHASTERISK expr)+ //RightComposition
    |	<assoc=right> expr AT expr	 //application
    |	expr TILDE expr TILDE expr //application
    |	<assoc=right> expr (MAP | MAPALL | DOUBLEAT | TRIPPLEAT) expr	//Map[], MapAll[], Apply[e, e], Apply[e, e, {1}]
	|	expr (BANG | DOUBLEBANG) //Factorial, Double Factorial
	|	expr (CONJUGATE | TRANSPOSE | CONJUGATETRANSPOSE | HERMITIANCONJUGATE) //Conjugate, etc.
	|	expr SINGLEQUOTE+ // Derivative[n][expr] where n counts the quotes.
	|	expr (LESSGREATER expr)+		//StringJoin
	|	<assoc=right> expr CARET expr	//Power
	|	INTEGRAL expr DIFFERENTIALD expr	//Integrate[]
	|	<assoc=right> DEL expr //Del[]
	|	<assoc=right> SQUARE expr //Square[]
	|	expr (SMALLCIRCLE expr)+ //SmallCircle[]
	|	expr (CIRCLEDOT expr)+ //CircleDot[]
	|	expr (DOUBLEASTERISK expr)+ //NonCommutativeMultiply[]
	|	expr (CROSS expr)+	//Cross[]
	|	expr (DOT expr)+		//Dot[]
	|	(MINUS | PLUS | PLUSMINUS | MINUSPLUS) expr	//Unary minus/plus
	|	expr (SLASH | DIVIDE) expr	//Division, Divide[]
	|	expr (BACKSLASH expr)+ //Backslash[]
	|	expr (DIAMOND expr)+ //Diamond[]
	|	expr (WEDGE expr)+ //Diamond[]
	|	expr (VEE expr)+ //Diamond[]
	|	expr (CIRCLETIMES expr)+ //Diamond[]
	|	expr (CENTERDOT expr)+ //Diamond[]
	|	expr { precededByPlusMinus() }? expr //Implicit multiplication, suppressed if second expr starts with '+'.
	|	expr (MultiplicationSymbol expr)+ //Times[]
	|	expr (STAR expr)+ //Star[]
	|	expr (VERTICALTILDE expr)+ //VerticalTilde[]
	|	expr (COPRODUCT expr)+ //Coproduct[]
	|	expr (CAP expr)+ //Cap[]
	|	expr (CUP expr)+ //Cup[]
	|	expr (CIRCLEPLUS expr)+ //CirclePlus[]
	|	expr CIRCLEMINUS expr //CirclePlus[]	
	|	expr (PLUS expr)+	//Plus[]
	|	expr MINUS expr	//Minus
	|	expr (PLUSMINUS expr)+ //PlusMinus[]
	|	expr (MINUSPLUS expr)+ //MinusPlus[]
	|	expr INTERSECTION expr //Set Intersection
	|	expr UNION expr	//Set Union

	//Span expressions. (Simplify?)
	|	expr DOUBLESEMICOLON expr DOUBLESEMICOLON expr
	|	expr DOUBLESEMICOLON DOUBLESEMICOLON expr
	|	DOUBLESEMICOLON expr DOUBLESEMICOLON expr
	|	DOUBLESEMICOLON DOUBLESEMICOLON expr
	|	expr DOUBLESEMICOLON expr
	|	expr DOUBLESEMICOLON
	|	DOUBLESEMICOLON expr
	|	DOUBLESEMICOLON

	|	expr (ComparisonSymbol expr)+ //Comparison
	|	expr (VerticalBarSymbol expr)+ //VerticalBar[], etc.
	|	expr (SameComparisonSymbol expr)+ //SameQ, UnsameQ
	|	expr (SetContainmentSymbol expr)+ // Set membership and containment
	// ForAll and friends require subscripting, i.e. they are not text-based commands.
//	|	expr (FORALL | EXISTS | NOTEXISTS) expr //Logical quantifiers
	|	(BANG | NOT) expr //Logical not
	|	expr (LogicalAndSymbol expr)+ //Logical And/Nand
	|	expr (LogicalXOrSymbol expr)+ //Logical Xor/XNor
	|	expr (LogicalOrSymbol expr)+ //Logical Or/Nor
	|	expr (LRDOUBLEARROW expr)+ //Logical equivalent, Equivalent[]
	|	<assoc=right> expr LogicalImpliesSymbol expr //Logical equivalent
	
	|	<assoc=right> expr RightTeeSymbol expr //RightTee, DoubleRightTee
	|	expr TeeSymbol expr //LeftTee, etc.
	|	<assoc=right> expr SUCHTHAT expr //SuchThat[]
	|	expr (DOUBLEDOT | TRIPPLEDOT)	//Repeated[] and RepeatedNull[]
	|	expr BAR expr	//Alternatives[]
	|	expr RAWCOLON expr ///Pattern[] and Optional[]
	|	expr (DOUBLETILDE expr)+ //StringExpression[]
	|	expr SLASHSEMI expr //Condition[]
	|	<assoc=right> expr (MINUSGREATER | RARROW | COLONGREATER | COLONARROW) expr //Rule/RuleDelayed
	|	expr (SLASHDOT | DOUBLESLASHDOT) expr //ReplaceAll[]/ReplaceRepeated[]
	|	<assoc=right> expr (PLUSEQUAL | MINUSEQUAL | ASTERISKEQUAL | SLASHEQUAL) expr // var += 1
	|	expr AMP	//Function[expr]
	|	expr (COLON expr)+ //Undefined flat infix, not to be confused with pattern which uses RAWCOLON.
	|	expr DOUBLESLASH expr //Postfix "headed" exression.
	|	expr (VERTICALSEPARATOR expr)+ //VerticalSeparator
	|	<assoc=right> expr THEREFORE expr
	|	expr BECAUSE expr
	|	expr EQUAL DOT	//Unset
	|	<assoc=right> expr (EQUAL | COLONEQUAL | CARETEQUAL | CARETCOLONEQUAL | FUNCTIONARROW) expr //Set[], SetDelayed[], etc.
	|	<assoc=right> symbol SLASHCOLON expr (EQUAL | COLONEQUAL) (expr | DOT)	//TagSet
	|	expr (DOUBLEGREATER | TRIPPLEGREATER) StringLiteral //Put/PutAppend
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

box
	:	expr
	|	BoxLeftBoxParenthesis box* BoxRightBoxParenthesis
	
	|	box BoxUnderscript box BoxOtherscript box // Underoverscript[]
	|	box BoxOverscript box BoxOtherscript box // Underoverscript[]
	|	<assoc=right> box (BoxOverscript | BoxUnderscript) box // Overscript[]/Underscript
	
	|	box BoxSubscript box BoxOtherscript box // Power[Subscript[]]
	|	box BoxSubscript box //Subscript
	|	InterpretedBox BoxLeftBoxParenthesis box+ BoxRightBoxParenthesis

	|	box BoxOverscript box
	|	box BoxUnderscript box BoxOtherscript box
	|	box BoxUnderscript box
	|	box BoxFraction box
	|	BoxSqrt box BoxOtherscript box
	|	BoxSqrt box
	|	box FormBox box
	;

