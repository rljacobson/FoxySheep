import java.util.Arrays;
import java.util.List;

import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.Token;

public abstract class Lexer extends org.antlr.v4.runtime.Lexer{
	
	Lexer self;
	long bracketLevel;
	Token lastToken;

	public Lexer(CharStream input) {
		super(input);
		self = this;
		lastToken = null;
		bracketLevel = 0;
	}

	public static void main(String[] args) throws Exception{
		FoxySheep.main(args);
	}

	/*
	 * TARGET LANGUAGE DEPENDENT CODE.
	 */
	 
	/*
	* Binary plus follows a complete expression. Complete
	* expressions always end with one of the following
	* tokens. On the other hand, unary plus never follows
	* these tokens. Distinguishing unary plus from binary
	* plus disambiguates the grammar and allows us to use
	* implicit multiplication.  
	*/
	List<Integer> closeExprTokens = Arrays.asList(
		FoxySheepParser.NumberLiteral,
		FoxySheepParser.Name,
		FoxySheepParser.StringLiteral,
		FoxySheepParser.RPAREN,
		FoxySheepParser.RBRACE,
		FoxySheepParser.HASH,
		FoxySheepParser.PERCENTDIGITS,
		FoxySheepParser.PERCENTS,
		FoxySheepParser.TRIPPLEBLANK,
		FoxySheepParser.DOUBLEBLANK,
		FoxySheepParser.BLANK,
		FoxySheepParser.HASHDIGITS,
		FoxySheepParser.HASHStringLiteral,
		FoxySheepParser.DOUBLEHASHDIGITS,
		FoxySheepParser.HASH,
		FoxySheepParser.DOUBLEHASH,
		FoxySheepParser.DIGITS,
		FoxySheepParser.RBRACKET,
		FoxySheepParser.RBARBRACKET,
		FoxySheepParser.BoxRightBoxParenthesis,
		FoxySheepParser.DOUBLEPLUS,
		FoxySheepParser.DOUBLEMINUS,
		FoxySheepParser.BANG,
		FoxySheepParser.DOUBLEBANG,
		FoxySheepParser.CONJUGATE,
		FoxySheepParser.TRANSPOSE,
		FoxySheepParser.CONJUGATETRANSPOSE,
		FoxySheepParser.HERMITIANCONJUGATE,
		FoxySheepParser.SINGLEQUOTE,
		FoxySheepParser.DOUBLESEMICOLON,
		FoxySheepParser.DOUBLEDOT,
		FoxySheepParser.TRIPPLEDOT,
		FoxySheepParser.AMP,
		FoxySheepParser.DOT,
		FoxySheepParser.SEMICOLON
		);

	/* 
	 * Curiously, the lexer does not allow us to inspect previous
	 * tokens. Thus we need to keep track of the previous token
	 * so that we can use it to disambiguate unary/binary plus.
	 * 
	 */ 
	public Token getToken(){
		Token lt = super.getToken();
		if(lt.getChannel() != HIDDEN) lastToken = lt;
		return lt;
	}
	public Token nextToken(){
		Token lt = super.nextToken();
		if(lt.getChannel() != HIDDEN) lastToken = lt;
		return lt;
	}
	
	/*
	 * The following checks to see if the previous token likely 
	 * ended an expr. If so, it returns true. We use this method 
	 * in an action on plus to disambiguate between unary plus
	 * and binary plus.
	 */
	boolean precededByExpr(){
		//Returns true if the previous token ended a complete expr.
		if(lastToken == null) return false;
		int tokenType = lastToken.getType();
		return closeExprTokens.contains(tokenType); 
	}

	
	/*
	 * To determine if a newline separates expressions, we keep 
	 * track of the bracketing level. Note that we treat all 
	 * bracket-like characters as the same.
	 */
	void incrementBracketLevel(int i){
		bracketLevel += i;
	}
	
	/*
	 * We need to differentiate between ";;" when it follows a complete
	 * expression or not in order to solve a context sensitivity 
	 * problem in the parser. See the Span parser rules for details.
	 */
	void checkDoubleSemicolon(){
		 if(!precededByExpr()) setType(FoxySheepParser.SPANSEMICOLONS); 
	}
	
	/*
	 * We distinguish between unary plus and binary plus.
	 */
	void checkAdditiveOp(int type){
		if(precededByExpr()) setType(type);
	}
	
	/*
	 * Note that FoxySheep treats newlines the same way Mathematica does: 
	 * Wolfram Language "treats the input that you give on successive 
	 * lines as belonging to the same expression whenever no complete 
	 * expression would be formed without doing this."
	 * 
	 * The following checks to see if the current token (a newline)
	 * separates two expressions using the following heuristic:
	 * If the token follows a complete expression and all bracket-
	 * like characters have been matched, then the token is an
	 * expression separator, and we return true.
	 */
	void checkNewline(){
		if( !(precededByExpr() && bracketLevel == 0) ) setChannel(HIDDEN);
	}
	
}
