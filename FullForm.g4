grammar FullForm;
import FullFormLexerRules;

// PARSER RULES
prog
	: expr (NEWLINE+ expr?)*
	;

expr
    :	numberLiteral	#Number
    |	StringLiteral	#StringLiteral
    |	symbol			#SymbolLiteral
    |	expr LBRACKET expressionList RBRACKET	#HeadExpression
    	;

expressionList // Can be empty.
	:	expr? (COMMA expr?)* 	#ExpressionListed
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
	:	MINUS? DIGITS NumberInBase numberLiteralPrecision? numberLiteralExponent? 	#NumberBaseN		// Number in any base.
	|	MINUS? (DIGITS | DecimalNumber) numberLiteralPrecision? numberLiteralExponent? 			#NumberBaseTen	// Number in base ten.
	;

numberLiteralPrecision
	:	DOUBLEBACKQUOTE (DecimalNumber | DIGITS)
	|	BACKQUOTE (DecimalNumber | DIGITS)?
	;

numberLiteralExponent
	:	(ASTERISKCARET (PLUS|MINUS)? DIGITS)
	;
