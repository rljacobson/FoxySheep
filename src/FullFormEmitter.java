/*
 * Copyright (c) 2015, Robert Jacobson
 * All rights reserved. 
 * 
 * Licensed under the BSD license. See LICENSE.txt for details.
 * 
 * Author(s): Robert Jacobson
 * 
 * Description: This class emits the FullForm representation of an expression.
 * 
 */

import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;

import java.io.FileInputStream;
import java.io.InputStream;
import java.util.Iterator;
import java.util.ArrayList;

public class FullFormEmitter extends FoxySheepBaseVisitor<String> {

	public String getFullForm(ParseTree e){
		if(e instanceof TerminalNode){
			return e.getText();
		}
		return visit(e);
	}
	
	public String makeHead(String head, ParseTree e){
		StringBuilder val = new StringBuilder(head);
		val.append("[");
		val.append(getFullForm(e));
		val.append("]");
		return val.toString();
	}
	public String makeHead(String head, ParseTree e1, ParseTree e2){
		StringBuilder val = new StringBuilder(head);
		val.append("[");
		val.append(getFullForm(e1));
		val.append(",");
		val.append(getFullForm(e2));
		val.append("]");
		return val.toString();
	}
	public String makeHead(String head, ParseTree e1, ParseTree e2, ParseTree e3){
		StringBuilder val = new StringBuilder(head);
		val.append("[");
		val.append(getFullForm(e1));
		val.append(",");
		val.append(getFullForm(e2));
		val.append(",");
		val.append(getFullForm(e3));
		val.append("]");
		return val.toString();
	}
	
	
	/*
	//visitPlusOp
	@Override public String visitPlusOp(FoxySheepParser.PlusOpContext ctx) {
		//This method is a bit bananas, because some ops are flat while others are left associative.
		
		StringBuilder val = new StringBuilder();
		String currentOp;
		String lastOp = "";
		String nextExpr;
		
		val.append( visit(ctx.expr(0)) );
		
		
		
		for(int i = 0; i < ctx.PlusMinus().size(); i++){
			nextExpr = visit(ctx.expr(i+1));
			currentOp = ctx.PlusMinus(i).getText();
			switch(currentOp){
			case "+":
				if (lastOp.equals(currentOp)){
					val.append(",");
					val.append( nextExpr );
				} else{
					//Close previous if exists.
					if(i > 0) val.append("],");
					val.append( nextExpr );
					//Open new.
					val.insert(0, "Plus[");
				}
				lastOp = currentOp;
				break;
			case "-":
				if(lastOp.equals("+")){
					val.append(",Times[-1,");
					val.append( nextExpr );
					//Close the Times.
					val.append("]");
				} else{
					//Close previous if exists.
					if (i > 0) val.append("],");
					val.append("Times[-1,");
					val.append( nextExpr );
					//Close the Times.
					val.append("]");
					//Open new at beginning.
					val.insert(0, "Plus[");
				}
				lastOp = "+";
				break;
			case "\u00b1": //PlusMinus
			case "\u2213": //MinusPlus
				//Close previous if exists.
				if(i > 0) val.append("]");
				val.append( visit(ctx.expr(i+1)) );
				//Close the PlusMinus.
				val.append("]");
				//Open new at beginning.
				val.insert(0, currentOp.equals("\u00b1") ? "PlusMinus[" : "MinusPlus[");
				lastOp = currentOp;
				break;
			} //end switch
		} //end for
		
		return val.toString(); 
	}
	*/
	
	public static void main(String[] args) throws Exception{
		String inputFile = "/Users/rljacobson/Google Drive/Development/FoxySheep/Expression.txt";
		InputStream istream = new FileInputStream(inputFile);
		
		ANTLRInputStream input = new ANTLRInputStream(istream);
		FoxySheepLexer lexer = new FoxySheepLexer(input);
		CommonTokenStream tokens = new CommonTokenStream(lexer);
		FoxySheepParser parser = new FoxySheepParser(tokens);
		ParseTree tree = parser.expr();
		FullFormEmitter emitter = new FullFormEmitter();
		
//		System.out.println( tree.toString() );
		System.out.println( emitter.visit(tree));
	}
	
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitUnset(FoxySheepParser.UnsetContext ctx) {
		return makeHead("Unset", ctx.expr());
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitCondition(FoxySheepParser.ConditionContext ctx) {
		return makeHead("Condition", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitImplies(FoxySheepParser.ImpliesContext ctx) {
		return makeHead("Implies", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitCompoundExpression(FoxySheepParser.CompoundExpressionContext ctx) {
		if(ctx.expr().size() == 1){
			StringBuilder val = new StringBuilder("CompoundExpression[");
			val.append( getFullForm(ctx.expr(0)));
			val.append( ",Null]" );
			return val.toString();
		}
		return makeHead("CompoundExpression", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitVerticalBar(FoxySheepParser.VerticalBarContext ctx) {
		if(ctx.VERTICALBAR() != null){
			return makeHead("VerticalBar", ctx.expr(0), ctx.expr(1));
		}
		if(ctx.NOTVERTICALBAR() != null){
			return makeHead("NotVerticalBar", ctx.expr(0), ctx.expr(1));
		}
		if(ctx.DOUBLEVERTICALBAR() != null){
			return makeHead("DoubleVerticalBar", ctx.expr(0), ctx.expr(1));
		}
		//if(ctx.NOTDOUBLEVERTICALBAR() != null){
		return makeHead("NotDoubleVerticalBar", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitVerticalTilde(FoxySheepParser.VerticalTildeContext ctx) {
		return makeHead("VerticalTilde", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitVee(FoxySheepParser.VeeContext ctx) {
		return makeHead("Vee", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitCross(FoxySheepParser.CrossContext ctx) {
		return makeHead("Cross", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitStringJoin(FoxySheepParser.StringJoinContext ctx) {
		return makeHead("StringJoin", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitComparison(FoxySheepParser.ComparisonContext ctx) {
		/*
		 * This is a rather complicated construct, because:
		 * 		"x==y" 		-> Equal[x,y]
		 * 		"x==y>z" 	-> Inequality[x, Equal, y, Greater, z]
		 * 		"x==y==z		-> Equal[x,y,z]
		 * 		"x>y>z"		-> Greater[x,y,z]
		 * So we need to flatten many different operators at once
		 * if necessary.
		 * 
		 * We solve this problem by postprocessing the syntax tree
		 * to flatten the tree where appropriate.  
		 */
		if(ctx.DOUBLEEQUAL() != null || ctx.LONGEQUAL() != null){
			return makeHead("Equal", ctx.expr(0), ctx.expr(1));
		}
		if(ctx.BANGEQUAL() != null){
			return makeHead("Unequal", ctx.expr(0), ctx.expr(1));
		}
		if(ctx.GREATER() != null){
			return makeHead("Greater", ctx.expr(0), ctx.expr(1));
		}
		if(ctx.GREATEREQUAL() != null 
				|| ctx.GREATEREQUALSYMBOL() != null
				|| ctx.GREATERSLANTEQUALSYMBOL() != null){
			return makeHead("GreaterEqual", ctx.expr(0), ctx.expr(1));
		}
		if(ctx.LESS() != null){
			return makeHead("Less", ctx.expr(0), ctx.expr(1));
		}
		//Must be lessequal.
		//if(ctx.LESSEQUAL() != null 
		//		|| ctx.LESSEQUALSYMBOL() != null
		//		|| ctx.LESSSLANTEQUALSYMBOL() != null){
		
		return makeHead("LessEqual", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitCirclePlus(FoxySheepParser.CirclePlusContext ctx) {
		return makeHead("CirclePlus", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitTee(FoxySheepParser.TeeContext ctx) {
		if(ctx.LEFTTEE() !=null){
			return makeHead("LeftTee", ctx.expr(0), ctx.expr(1));
		}
		if(ctx.DOUBLELEFTTEE() !=null){
			return makeHead("DoubleLeftTee", ctx.expr(0), ctx.expr(1));
		}
		if(ctx.UPTEE() !=null){
			return makeHead("UpTee", ctx.expr(0), ctx.expr(1));
		}
		return makeHead("DownTee", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitIntersection(FoxySheepParser.IntersectionContext ctx) {
		return makeHead("Intersection", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitIncrement(FoxySheepParser.IncrementContext ctx) {
		if(ctx.DOUBLEMINUS()==null){
			return makeHead("Increment", ctx.expr());
		}
		return makeHead("Decrement", ctx.expr());
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitSlot(FoxySheepParser.SlotContext ctx) {
		return ctx.getText();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitSet(FoxySheepParser.SetContext ctx) {
		if(ctx.EQUAL() != null){
			return makeHead("Set", ctx.expr(0), ctx.expr(1));
		}
		if(ctx.COLONEQUAL() != null){
			return makeHead("SetDelayed", ctx.expr(0), ctx.expr(1));
		}
		if(ctx.CARETEQUAL() != null){
			return makeHead("UpSet", ctx.expr(0), ctx.expr(1));
		}
		if(ctx.CARETCOLONEQUAL() != null){
			return makeHead("UpSetDelayed", ctx.expr(0), ctx.expr(1));
		}
		//if(ctx.FUNCTIONARROW() != null)
		StringBuilder val = new StringBuilder("Function[{");
		
		val.append(getFullForm(ctx.expr(0)));
		val.append("},");
		val.append(getFullForm(ctx.expr(1)));
		val.append("]");
		
		return val.toString();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitXor(FoxySheepParser.XorContext ctx) {
		if(ctx.XOR() != null){
			return makeHead("Xor", ctx.expr(0), ctx.expr(1));
		}
		return makeHead("Xnor", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitComposition(FoxySheepParser.CompositionContext ctx) {
		return makeHead("Composition", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitOut(FoxySheepParser.OutContext ctx) {
		return ctx.getText();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitIntegrate(FoxySheepParser.IntegrateContext ctx) {
		return makeHead("Integrate", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitAccessor(FoxySheepParser.AccessorContext ctx) {
		return makeHead("Part", ctx.expr(), ctx.accessExpression());
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitHeadExpression(FoxySheepParser.HeadExpressionContext ctx) {
		return makeHead(visit(ctx.expr()), ctx.expressionList());
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitSquare(FoxySheepParser.SquareContext ctx) {
		return makeHead("Square", ctx.expr());
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitTherefore(FoxySheepParser.ThereforeContext ctx) {
		return makeHead("Therefore", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitPut(FoxySheepParser.PutContext ctx) {
		if(ctx.DOUBLEGREATER() != null){
			return makeHead("Put", ctx.expr(), ctx.StringLiteral());
		}
		return makeHead("PutAppend", ctx.expr(), ctx.StringLiteral());
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitPlusOp(FoxySheepParser.PlusOpContext ctx) {
		if(ctx.BINARYPLUS() != null){
			return makeHead("Plus", ctx.expr(0), ctx.expr(1));
		}
		if(ctx.BINARYMINUS() != null){
			//Mathematica interprets x-y as Plus[x,Times[-1,y]].
			StringBuilder val = new StringBuilder("Plus[");
			val.append( getFullForm(ctx.expr(0)) );
			val.append(",Times[-1,");
			val.append( getFullForm(ctx.expr(1)) );
			val.append("]]");
			return val.toString();
		}
		if(ctx.BINARYPLUSMINUS() != null){
			
		}
		if(ctx.BINARYMINUSPLUS() != null){
			
		}
		return ctx.getText();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitPower(FoxySheepParser.PowerContext ctx) {
		return makeHead("Power", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitVerticalSeparator(FoxySheepParser.VerticalSeparatorContext ctx) {
		return makeHead("VerticalSeparator", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitUnaryPlusMinus(FoxySheepParser.UnaryPlusMinusContext ctx) {
		if(ctx.MINUS() != null){
			StringBuilder val = new StringBuilder("Times[-1,");
			val.append( getFullForm(ctx.expr()) );
			val.append("]");
			return val.toString();
		}
		if(ctx.PLUS() != null){
			return makeHead("Plus", ctx.expr());
		}
		if(ctx.PLUSMINUS() != null){
			return makeHead("PlusMinus", ctx.expr());
		}
		//if(ctx.MINUSPLUS() != null)
		return makeHead("MinusPlus", ctx.expr());
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitUnion(FoxySheepParser.UnionContext ctx) {
		return makeHead("Union", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitPrefix(FoxySheepParser.PrefixContext ctx) {
		return makeHead( getFullForm(ctx.expr(0)), ctx.expr(1) );
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitPreIncrement(FoxySheepParser.PreIncrementContext ctx) {
		if(ctx.DOUBLEMINUS()==null){
			return makeHead("PreIncrement", ctx.expr());
		}
		return makeHead("PreDecrement", ctx.expr());
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitPatternExp(FoxySheepParser.PatternExpContext ctx) {
		//symb:expr
		return makeHead("Patter", ctx.symbol(), ctx.expr());
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitPatternForm(FoxySheepParser.PatternFormContext ctx) {
		return ctx.getText();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitBecause(FoxySheepParser.BecauseContext ctx) {
		return makeHead("Because", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitOr(FoxySheepParser.OrContext ctx) {
		if(ctx.NOR() != null){
			return makeHead("Nor", ctx.expr(0), ctx.expr(1));
		}
		return makeHead("Or", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitRightTee(FoxySheepParser.RightTeeContext ctx) {
		if(ctx.RIGHTTEE() != null){
			return makeHead("RightTee", ctx.expr(0), ctx.expr(1));
		}
		return makeHead("DoubleRightTee", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitCup(FoxySheepParser.CupContext ctx) {
		return makeHead("Cup", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitBoxParen(FoxySheepParser.BoxParenContext ctx) {
		return ctx.getText();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitStringExpression(FoxySheepParser.StringExpressionContext ctx) {
		return makeHead("StringExpression", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitPostfix(FoxySheepParser.PostfixContext ctx) {
		StringBuilder val = new StringBuilder();
		
		val.append(getFullForm(ctx.expr(1)));
		val.append("[");
		val.append(getFullForm(ctx.expr(0)));
		val.append("]");
		
		return val.toString();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitAnd(FoxySheepParser.AndContext ctx) {
		if(ctx.NAND() != null){
			return makeHead("Nand", ctx.expr(0), ctx.expr(1));
		}
		return makeHead("And", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitOptional(FoxySheepParser.OptionalContext ctx) {
		return makeHead("Optional", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitRightComposition(FoxySheepParser.RightCompositionContext ctx) {
		return makeHead("RightComposition", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitPatternTest(FoxySheepParser.PatternTestContext ctx) {
		return makeHead("PatternTest", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitNonCommutativeMultiply(FoxySheepParser.NonCommutativeMultiplyContext ctx) {
		return makeHead("NonCommutativeMultiply", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitSpanA(FoxySheepParser.SpanAContext ctx) {
		return ctx.getText();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitInfix(FoxySheepParser.InfixContext ctx) {
		return makeHead( getFullForm(ctx.expr(1)), ctx.expr(0), ctx.expr(2) );
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitParentheses(FoxySheepParser.ParenthesesContext ctx) { 
		return visit(ctx.expr()); 
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitFactorial(FoxySheepParser.FactorialContext ctx) {
		if(ctx.BANG()!=null){
			return makeHead("Factorial", ctx.expr());
		}
		return makeHead("Factorial2", ctx.expr());
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitSuchThat(FoxySheepParser.SuchThatContext ctx) {
		return makeHead("SuchThat", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitSpanE(FoxySheepParser.SpanEContext ctx) {
		return ctx.getText();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitSpanD(FoxySheepParser.SpanDContext ctx) {
		return ctx.getText();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitSpanC(FoxySheepParser.SpanCContext ctx) {
		return ctx.getText();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitNumberLiteral(FoxySheepParser.NumberLiteralContext ctx) {
		return ctx.getText();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitSetContainment(FoxySheepParser.SetContainmentContext ctx) {
		if(ctx.ELEMENT() != null){
			return makeHead("Element", ctx.expr(0), ctx.expr(1));
		}
		if(ctx.NOTELEMENT() != null){
			return makeHead("NotElement", ctx.expr(0), ctx.expr(1));
		}
		if(ctx.SUBSET() != null){
			return makeHead("Subset", ctx.expr(0), ctx.expr(1));
		}
		//if(ctx.SUPERSET() != null)
		return makeHead("Superset", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitSpanB(FoxySheepParser.SpanBContext ctx) {
		return ctx.getText();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitSpanH(FoxySheepParser.SpanHContext ctx) {
		return ctx.getText();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitCircleDot(FoxySheepParser.CircleDotContext ctx) {
		return makeHead("CircleDot", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitSpanG(FoxySheepParser.SpanGContext ctx) {
		return ctx.getText();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitSpanF(FoxySheepParser.SpanFContext ctx) {
		return ctx.getText();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitWedge(FoxySheepParser.WedgeContext ctx) {
		return makeHead("Wedge", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitDel(FoxySheepParser.DelContext ctx) {
		return makeHead("Del", ctx.expr());
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitColon(FoxySheepParser.ColonContext ctx) {
		return makeHead("Colon", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitBoxConstructor(FoxySheepParser.BoxConstructorContext ctx) {
		return ctx.getText();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitCap(FoxySheepParser.CapContext ctx) {
		return makeHead("Cap", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitOpEquals(FoxySheepParser.OpEqualsContext ctx) {
		if(ctx.PLUSEQUAL() != null){
			return makeHead("AddTo", ctx.expr(0), ctx.expr(1));
		}
		if(ctx.MINUSEQUAL() != null){
			return makeHead("SubtractFrom", ctx.expr(0), ctx.expr(1));
		}
		if(ctx.ASTERISKEQUAL() != null){
			return makeHead("TimesBy", ctx.expr(0), ctx.expr(1));
		}
		//if(ctx.SLASHEQUAL() != null){
		return makeHead("DivideBy", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitAlternatives(FoxySheepParser.AlternativesContext ctx) {
		return makeHead("Alternatives", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitReplaceAll(FoxySheepParser.ReplaceAllContext ctx) {
		if(ctx.SLASHDOT() != null){
			return makeHead("ReplaceAll", ctx.expr(0), ctx.expr(1));
		}
		return makeHead("ReplaceRepeated", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitDiamond(FoxySheepParser.DiamondContext ctx) {
		return makeHead("Diamond", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitDivide(FoxySheepParser.DivideContext ctx) {
		if(ctx.DIVIDE() != null){
			return makeHead("Divide", ctx.expr(0), ctx.expr(1));
		}
		//Mathematica treats x/y as Times[x,Power[y,-1]].
		StringBuilder val = new StringBuilder("Times[");
		val.append( getFullForm(ctx.expr(0)) );
		val.append(",Power[");
		val.append( getFullForm(ctx.expr(1)) );
		val.append(",-1]]");
		return val.toString();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitList(FoxySheepParser.ListContext ctx) {
		return makeHead("List", ctx.expressionList());
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitMapApply(FoxySheepParser.MapApplyContext ctx) {
		//expr (MAP | MAPALL | DOUBLEAT | TRIPPLEAT) expr
		if(ctx.MAP()!=null){
			return makeHead("Map", ctx.expr(0), ctx.expr(1));
		}
		if(ctx.MAPALL()!=null){
			return makeHead("MapAll", ctx.expr(0), ctx.expr(1));
		}
		if(ctx.DOUBLEAT()!=null){
			return makeHead("Apply", ctx.expr(0), ctx.expr(1));
		}
		//if(ctx.TRIPPLEAT()!=null)
		//We can't use makeHead because the third argument isn't a ParseTree.
		//Apply[expr1,expr2,{1}]
		StringBuilder val = new StringBuilder("Apply[");
		val.append( getFullForm(ctx.expr(0)) );
		val.append( "," );
		val.append( getFullForm(ctx.expr(1)) );
		val.append( ",List[1]]" ); 
		return val.toString();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitCenterDot(FoxySheepParser.CenterDotContext ctx) {
		return makeHead("CenterDot", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitConjugate(FoxySheepParser.ConjugateContext ctx) {
		if(ctx.CONJUGATE()!=null){
			return makeHead("Conjugate", ctx.expr());
		}
		if(ctx.TRANSPOSE()!=null){
			return makeHead("Transpose", ctx.expr());
		}
		//The other two are the same.
		//if(ctx.CONJUGATETRANSPOSE()!=null)
		//if(ctx.HERMITIANCONJUGATE()!=null)
		return makeHead("ConjugateTranspose", ctx.expr());
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitStringLiteral(FoxySheepParser.StringLiteralContext ctx) {
		return ctx.getText();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitEquivalent(FoxySheepParser.EquivalentContext ctx) {
		return makeHead("Equivalent", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitCoproduct(FoxySheepParser.CoproductContext ctx) {
		return makeHead("Coproduct", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitSmallCircle(FoxySheepParser.SmallCircleContext ctx) {
		return makeHead("SmallCircle", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitMessage(FoxySheepParser.MessageContext ctx) {
		//One string literal.
		if(ctx.StringLiteral().size() == 1){
			return makeHead("MessageName", ctx.expr(), ctx.StringLiteral(0));
		}
		//Two string literals.
		return makeHead("MessageName", ctx.expr(), ctx.StringLiteral(0), ctx.StringLiteral(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitMultiplyImplicit(FoxySheepParser.MultiplyImplicitContext ctx) {
		return makeHead("Times", ctx.expr(0), ctx.expr(1));
	}
	
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
//	@Override public String visitMultiplyImplicit(FoxySheepParser.MultiplyImplicitContext ctx) {
//		return makeHead("Times", ctx.expr(0), ctx.expr(1));
//	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitFunction(FoxySheepParser.FunctionContext ctx) {
		return makeHead("Function", ctx.expr());
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitTimes(FoxySheepParser.TimesContext ctx) {
		return makeHead("Times", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitTagSet(FoxySheepParser.TagSetContext ctx) {
		if(ctx.EQUAL() != null){
			return makeHead("TagSet", ctx.symbol(), ctx.expr(0), ctx.expr(1));
		}
		//Must be TagSetDelated.
		return makeHead("TagSetDelayed", ctx.symbol(), ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitTagUnset(FoxySheepParser.TagUnsetContext ctx) {
		return makeHead("TagUnset", ctx.symbol(), ctx.expr());
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitSymbolLiteral(FoxySheepParser.SymbolLiteralContext ctx) {
		//FullForm of a symbol is itself.
		return ctx.getText();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitRule(FoxySheepParser.RuleContext ctx) {
		if(ctx.MINUSGREATER() != null || ctx.RARROW() != null){
			return makeHead("Rule", ctx.expr(0), ctx.expr(1));
		}
		return makeHead("RuleDelayed", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitBackslash(FoxySheepParser.BackslashContext ctx) {
		return makeHead("Backslash", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitNot(FoxySheepParser.NotContext ctx) {
		return makeHead("Not", ctx.expr());
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitDot(FoxySheepParser.DotContext ctx) {
		return makeHead("Dot", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitCircleTimes(FoxySheepParser.CircleTimesContext ctx) {
		return makeHead("CircleTimes", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitSame(FoxySheepParser.SameContext ctx) {
		if(ctx.TRIPPLEEQUAL() != null){
			return makeHead("SameQ", ctx.expr(0), ctx.expr(1)); 
		}
		return makeHead("UnsameQ", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitStar(FoxySheepParser.StarContext ctx) {
		return makeHead("Star", ctx.expr(0), ctx.expr(1) );
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitDerivative(FoxySheepParser.DerivativeContext ctx) {
		StringBuilder val = new StringBuilder("Derivative[");
		val.append(Integer.toString(ctx.SINGLEQUOTE().size()));
		val.append("][");
		val.append( getFullForm(ctx.expr()) );
		val.append("]");
		return val.toString();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitGet(FoxySheepParser.GetContext ctx) {
		return makeHead("Get", ctx.StringLiteral());
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitRepeated(FoxySheepParser.RepeatedContext ctx) {
		if(ctx.DOUBLEDOT() != null){
			return makeHead("Repeated", ctx.expr());
		}
		return makeHead("RepeatedNull", ctx.expr());
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitCircleMinus(FoxySheepParser.CircleMinusContext ctx) {
		return makeHead("CircleMinus", ctx.expr(0), ctx.expr(1));
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitContextName(FoxySheepParser.ContextNameContext ctx) {
		return ctx.getText();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitSimpleContext(FoxySheepParser.SimpleContextContext ctx) {
		return ctx.getText();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitCompoundContext(FoxySheepParser.CompoundContextContext ctx) {
		return ctx.getText();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitPatternBlanks(FoxySheepParser.PatternBlanksContext ctx) {
		return ctx.getText();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitPatternBlankDot(FoxySheepParser.PatternBlankDotContext ctx) {
		return ctx.getText();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitOutNumbered(FoxySheepParser.OutNumberedContext ctx) {
		return ctx.getText();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitOutUnnumbered(FoxySheepParser.OutUnnumberedContext ctx) {
		return ctx.getText();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitSlotDigits(FoxySheepParser.SlotDigitsContext ctx) {
		return ctx.getText();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitSlotNamed(FoxySheepParser.SlotNamedContext ctx) {
		return ctx.getText();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitSlotSequenceDigits(FoxySheepParser.SlotSequenceDigitsContext ctx) {
		return ctx.getText();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitSlotSequence(FoxySheepParser.SlotSequenceContext ctx) {
		return ctx.getText();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitSlotUnnamed(FoxySheepParser.SlotUnnamedContext ctx) {
		return ctx.getText();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitExpressionListed(FoxySheepParser.ExpressionListedContext ctx) {
		//expressionList can be empty. 
		if(ctx.children.size()==0) return "";
		
		StringBuilder val = new StringBuilder();
		ParseTree child;
		int exprCounter = 0;
		
		for(int childCounter = 0; childCounter < ctx.children.size(); childCounter++){
			//Separate with a comma.
			if(childCounter > 0) val.append(",");
			
			child = ctx.children.get(childCounter);
			if(exprCounter < ctx.expr().size() && child == ctx.expr(exprCounter)){
				val.append( visit(child) );
				exprCounter++;
				childCounter++; //The next child is a comma (or end of list) which we skip.
			}else{
				//Must have been a comma indicating Null.
				val.append("Null");
				//If the comma is the last child, it needs to be followed by a Null, too.
				if(childCounter == ctx.children.size()-1){
					val.append(",Null");
				}
			}
		}
		return val.toString();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitAccessExpressionA(FoxySheepParser.AccessExpressionAContext ctx) {
		return ctx.expressionList().accept(this);
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitAccessExpressionB(FoxySheepParser.AccessExpressionBContext ctx) {
		return ctx.expressionList().accept(this);
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitBox(FoxySheepParser.BoxContext ctx) {
		return ctx.getText();
	}
}
