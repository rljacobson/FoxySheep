grammar InputForm;
import InputFormLexerRules;


// PARSER RULES
prog
	: expr (NEWLINE+ expr?)*
	| expressionList
	;

expr
    :	numberLiteral	#Number
    |	StringLiteral	#StringLiteral

    |	LPAREN expr RPAREN	#Parentheses //Grouping with parentheses
    |	LBRACE expressionList RBRACE 	#List //List expression
    |	LANGLE expressionList RANGLE		#AngleBracket
    |	LFLOOR expr RFLOOR				#Floor
    |	LCEILING expr RCEILING			#Ceiling
    |	LBRACKETINGBAR expressionList RBRACKETINGBAR	#BracketingBar
    |	LDOUBLEBRACKETINGBAR expressionList RDOUBLEBRACKETINGBAR #DoubleBracketingBar

    |	expr DOUBLECOLON StringLiteral (DOUBLECOLON StringLiteral)?	#Message // MessageName[]
    |	slotExpression	#Slot //"forms containing #"
    |	outExpression 	#Out //"forms containing %"
//    |	pattern			#PatternForm // "forms containing _"
	|	symbol? (TRIPPLEBLANK | DOUBLEBLANK | BLANK) expr?	#PatternBlanks
	|	symbol? BLANKDOT		#PatternBlankDot
    |	symbol				#SymbolLiteral

    |	DOUBLELESS StringLiteral 	#Get

	//TODO: Finish and test box related grammar.
//	|	BoxLeftBoxParenthesis box* BoxRightBoxParenthesis	#BoxParen

	|	expr QUESTIONMARK expr 	#PatternTest
    |	expr LBRACKET expressionList RBRACKET	#HeadExpression
    |	expr accessExpression	#Accessor //accessor, i.e. a[[1]]
    |	BoxConstructor expr		#BoxConstructor
    |	expr (DOUBLEPLUS | DOUBLEMINUS)	#Increment //Increment or Decrement
    |	(DOUBLEPLUS | DOUBLEMINUS) expr	#PreIncrement //PreIncrement or PreDecrement
    |	expr ATASTERISK expr 			#Composition
    |	expr SLASHASTERISK expr 			#RightComposition
    |	<assoc=right> expr AT expr	 	#Prefix //Application: f@x === f[x]
    |	expr TILDE expr TILDE expr 		#Infix  //application: x~f~y === f[x, y]
    |	<assoc=right> expr (MAP | MAPALL | DOUBLEAT | TRIPPLEAT) expr		#MapApply //Map[], MapAll[], Apply[e, e], Apply[e, e, {1}]
	|	expr (BANG | DOUBLEBANG) 		#Factorial //Factorial (!) and Double Factorial (!!)
	|	expr (CONJUGATE | TRANSPOSE | CONJUGATETRANSPOSE | HERMITIANCONJUGATE)	#Conjugate
	|	expr SINGLEQUOTE+				#Derivative //Derivative[n][expr] where n counts the quotes.
	|	expr LESSGREATER expr			#StringJoin
	|	<assoc=right> expr CARET expr	#Power
	|	INTEGRAL expr DIFFERENTIALD expr	#Integrate
	|	<assoc=right> DEL expr			#Del
	|	<assoc=right> SQUARE expr		#Square
	|	expr SMALLCIRCLE expr			#SmallCircle
	|	expr CIRCLEDOT expr				#CircleDot
	|	expr DOUBLEASTERISK expr			#NonCommutativeMultiply
	|	expr CROSS expr					#Cross
	|	expr DOT expr					#Dot
	|	(MINUS | PLUS | PLUSMINUS | MINUSPLUS) expr	#UnaryPlusMinus
	|	expr (SLASH | DIVIDE) expr	#Divide
	|	expr RAWBACKSLASH expr 		#Backslash
	|	expr DIAMOND expr			#Diamond
	|	expr WEDGE expr 				#Wedge
	|	expr VEE expr				#Vee
	|	expr CIRCLETIMES expr		#CircleTimes
	|	expr CENTERDOT expr			#CenterDot

	//Implicit Multiplication
//	|	expr expr	#MultiplyImplicit

	|	expr MultiplicationSymbol? expr	#Times
	|	expr STAR expr			#Star
	|	expr VERTICALTILDE expr 	#VerticalTilde
	|	expr COPRODUCT expr		#Coproduct
	|	expr CAP expr 			#Cap
	|	expr CUP expr 			#Cup
	|	expr CIRCLEPLUS expr		#CirclePlus
	|	expr CIRCLEMINUS expr 	#CircleMinus

	|	expr (BINARYPLUS | BINARYMINUS | BINARYPLUSMINUS | BINARYMINUSPLUS) expr	#PlusOp

	|	expr INTERSECTION expr		#Intersection
	|	expr UNION expr				#Union

	//Span expressions.
	/*
	 * There is a tricky context sensitivity with the following two rules. Consider the
	 * expression "2 ;; 10 ;; 3". Since implicit multiplication has higher precedence
	 * than span, this expression wants to parse as Times[2, Span[All, 10, 3]]. We
	 * solve this problem in the lexer by detecting when the ";;" follows a complete
	 * expression (or another ";;"), and if it doesn't, sending a different token to
	 * the parser. Hence the two tokens SPANSEMICOLONS and DOUBLESEMICOLON both
	 * representing ";;".
	 *
	 * Note that the following rules do not accurately represent permissible Span
	 * expressions in Wolfram Language (though they accept and reject the right stuff).
	 * The parse tree is rewritten post-parse to obtain the correct tree for Wolfram
	 * Language Span expressions, because the correct parse trees are difficult to get
	 * using automated parser generators.
	 *
	 */
	|	expr DOUBLESEMICOLON expr?  #SpanA
	|	SPANSEMICOLONS expr? (DOUBLESEMICOLON expr?)* #SpanB


	//Comparison
	|	expr (EqualSymbol | NotEqualSymbol | GreaterEqualSymbol | LessEqualSymbol | GREATER | LESS) expr	#Comparison

	|	expr (VERTICALBAR | NOTVERTICALBAR | DOUBLEVERTICALBAR | NOTDOUBLEVERTICALBAR) expr		#VerticalBar
	|	expr (TRIPPLEEQUAL | EQUALBANGEQUAL) expr	#Same //SameQ, UnsameQ
	|	expr (ELEMENT | NOTELEMENT | SUBSET | SUPERSET) expr 	#SetContainment //Set membership and containment
	// ForAll and friends require subscripting, i.e. they are not text-based commands.
//	|	expr (FORALL | EXISTS | NOTEXISTS) expr //Logical quantifiers
	|	(BANG | NOT) expr					#Not //Logical not
	|	expr (DOUBLEAMP | AND | NAND) expr 	#And //Logical And/Nand
	|	expr (XOR | XNOR) expr 				#Xor //Logical Xor/XNor
	|	expr (OR | NOR | DOUBLEBAR) expr 	#Or  //Logical Or/Nor
	|	expr LRDOUBLEARROW expr				#Equivalent //Logical equivalent
	|	<assoc=right> expr (RDOUBLEARROW | LCONTAINS) expr		#Implies //Logical implies
	|	<assoc=right> expr (RIGHTTEE | DOUBLERIGHTTEE) expr		#RightTee //RightTee, DoubleRightTee
	|	expr (LEFTTEE | DOUBLELEFTTEE | UPTEE | DOWNTEE) expr	#Tee //LeftTee, etc.
	|	<assoc=right> expr SUCHTHAT expr	#SuchThat
	|	expr (DOUBLEDOT | TRIPPLEDOT)	#Repeated //Repeated[] and RepeatedNull[]
	|	expr BAR expr			#Alternatives
	|	symbol RAWCOLON expr		#PatternExp //Pattern[] and Optional[]
	|	expr RAWCOLON expr		#Optional //Pattern[] and Optional[]
	|	expr DOUBLETILDE expr	#StringExpression
	|	expr SLASHSEMI expr		#Condition
	|	<assoc=right> expr (MINUSGREATER | RARROW | COLONGREATER | COLONARROW) expr 	#Rule //Rule and RuleDelayed
	|	expr (SLASHDOT | DOUBLESLASHDOT) expr	#ReplaceAll //ReplaceAll[]/ReplaceRepeated[]
	|	<assoc=right> expr (PLUSEQUAL | MINUSEQUAL | ASTERISKEQUAL | SLASHEQUAL) expr 	#OpEquals //var += 1
	|	expr AMP					#Function //Function[expr]
	|	expr COLON expr 			#Colon //Undefined flat infix, not to be confused with pattern which uses RAWCOLON.
	|	expr DOUBLESLASH expr	#Postfix //Postfix "headed" exression, i.e. expr//InputForm
	|	expr VERTICALSEPARATOR expr		#VerticalSeparator
	|	<assoc=right> expr THEREFORE expr	#Therefore
	|	expr BECAUSE expr					#Because
	|	expr EQUAL DOT						#Unset
	|	<assoc=right> expr (EQUAL | COLONEQUAL | CARETEQUAL | CARETCOLONEQUAL | FUNCTIONARROW) expr	#Set //Set[], SetDelayed[], etc.
	|	<assoc=right> symbol SLASHCOLON expr (EQUAL | COLONEQUAL) expr	#TagSet //TagSetDelayed
	|	symbol SLASHCOLON expr EQUAL DOT		#TagUnset
	|	expr (DOUBLEGREATER | TRIPPLEGREATER) StringLiteral	#Put //Put/PutAppend
	|	expr SEMICOLON expr?					#CompoundExpression
    ;

//Symbols and Contexts
symbol
	: context? Name	#ContextName
	;

context
	: BACKQUOTE? Name BACKQUOTE		#SimpleContext
	| Name BACKQUOTE Name BACKQUOTE	#CompoundContext
	;

//Numbers
numberLiteral
	:	DIGITS NumberInBase numberLiteralPrecision? numberLiteralExponent? 	#NumberBaseN		// Number in any base.
	|	(DIGITS | DecimalNumber) numberLiteralPrecision? numberLiteralExponent? 			#NumberBaseTen	// Number in base ten.
	;

numberLiteralPrecision
	:	DOUBLEBACKQUOTE (DecimalNumber | DIGITS)
	|	BACKQUOTE (DecimalNumber | DIGITS)?
	;

numberLiteralExponent
	:	(ASTERISKCARET (PLUS|MINUS)? DIGITS)
	;

//Slot[] and Out[]
outExpression
	:	PERCENTDIGITS	#OutNumbered
	|	PERCENTS			#OutUnnumbered
	;

slotExpression
	:	HASHDIGITS			#SlotDigits
	|	HASHStringLiteral	#SlotNamed
	|	DOUBLEHASHDIGITS		#SlotSequenceDigits
	|	DOUBLEHASH			#SlotSequence
	|	HASH					#SlotUnnamed
	;

// List-like expressions

expressionList // Can be empty.
	:	expr? (COMMA expr?)* 	#ExpressionListed
	;


// Accessor is used to access parts of an expression, i.e. a[[1]]
accessExpression
	:	LBRACKET LBRACKET expressionList RBRACKET RBRACKET	#AccessExpressionA
	|	LBARBRACKET expressionList RBARBRACKET				#AccessExpressionB
	;

//box
//	:	expr
//	|	BoxLeftBoxParenthesis box* BoxRightBoxParenthesis
//
//	|	box BoxUnderscript box BoxOtherscript box // Underoverscript[]
//	|	box BoxOverscript box BoxOtherscript box // Underoverscript[]
//	|	<assoc=right> box (BoxOverscript | BoxUnderscript) box // Overscript[]/Underscript
//
//	|	box BoxSubscript box BoxOtherscript box // Power[Subscript[]]
//	|	box BoxSubscript box //Subscript
//	|	InterpretedBox BoxLeftBoxParenthesis box+ BoxRightBoxParenthesis
//
//	|	box BoxOverscript box
//	|	box BoxUnderscript box BoxOtherscript box
//	|	box BoxUnderscript box
//	|	box BoxFraction box
//	|	BoxSqrt box BoxOtherscript box
//	|	BoxSqrt box
//	|	box FormBox box
//	;
