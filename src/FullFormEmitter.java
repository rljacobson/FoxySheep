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

import java.util.List;
import java.util.HashMap;
//import java.util.Map;


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
	
	/**
	 * {@inheritDoc}
	 *
	 * <p>Makes a "head" expression with arguments from List e. When passing in
	 * ctx.children for e, one must remove the TerminalNode representing the
	 * operator from ctx.children first. Alternatively, pass ctx.expr().</p>
	 */
	public String makeHeadList(String head, List e){
		StringBuilder val = new StringBuilder(head);
		val.append("[");
		for(int i = 0; i < e.size(); i++){
			val.append( getFullForm((ParseTree)e.get(i)) );
			if(i < e.size()-1){
				val.append(",");
			}
		}
		val.append("]");
		return val.toString();
	}
	
	public static void main(String[] args) throws Exception{
		FoxySheep.main(args);
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
		/* Since we need to check for ending in "Null" anyway, we might as
		 * well not bother with makeHeadList(). 
		 */
		StringBuilder val = new StringBuilder("CompoundExpression[");
		val.append( getFullForm(ctx.getChild(0) ));
		for(int i = 2; i<ctx.getChildCount(); i +=2){
			val.append(",");
			val.append( getFullForm(ctx.getChild(i) ));
		}
		if(ctx.getChildCount() % 2 == 0){
			//An even number of children means we ended in a semicolon.
			val.append( ",Null]" );
		}else{
			val.append( "]" );
		}
		return val.toString();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitVerticalBar(FoxySheepParser.VerticalBarContext ctx) {
		if(ctx.VERTICALBAR() != null){
			return makeHeadList("VerticalBar", ctx.expr());
		}
		if(ctx.NOTVERTICALBAR() != null){
			return makeHeadList("NotVerticalBar", ctx.expr());
		}
		if(ctx.DOUBLEVERTICALBAR() != null){
			return makeHeadList("DoubleVerticalBar", ctx.expr());
		}
		//if(ctx.NOTDOUBLEVERTICALBAR() != null){
		return makeHeadList("NotDoubleVerticalBar", ctx.expr());
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitVerticalTilde(FoxySheepParser.VerticalTildeContext ctx) {
		return makeHeadList("VerticalTilde", ctx.expr());
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitVee(FoxySheepParser.VeeContext ctx) {
		return makeHeadList("Vee", ctx.expr());
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitCross(FoxySheepParser.CrossContext ctx) {
		return makeHeadList("Cross", ctx.expr());
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitStringJoin(FoxySheepParser.StringJoinContext ctx) {
		return makeHeadList("StringJoin", ctx.expr());
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
		
		HashMap<Integer, String> opText = new HashMap<Integer, String>(6);
		opText.put(FoxySheepParser.EqualSymbol, "Equal");
		opText.put(FoxySheepParser.NotEqualSymbol, "Unequal");
		opText.put(FoxySheepParser.GREATER, "Greater");
		opText.put(FoxySheepParser.GreaterEqualSymbol, "GreaterEqual");
		opText.put(FoxySheepParser.LESS, "Less");
		opText.put(FoxySheepParser.LessEqualSymbol, "LessEqual");
		
		
		boolean allSame = true;
		int opType = ((TerminalNode)ctx.getChild(1)).getSymbol().getType();
		for(int i = 3; i < ctx.getChildCount(); i+=2){
			allSame = allSame && (opType == ((TerminalNode)ctx.getChild(i)).getSymbol().getType());
		}
		
		//If all operators are the same, make a "head" with that operator. 
		if(allSame){
			return makeHeadList((String)opText.get(opType), ctx.expr());
		}
		
		//All operators are not the same. We need to create an Inequality[].
		TerminalNode op;
		StringBuilder val = new StringBuilder("Inequality[");
		val.append( getFullForm(ctx.expr(0)) );
		for(int i = 1; i < ctx.getChildCount(); i+=2){
			val.append(",");
			op = (TerminalNode)ctx.getChild(i);
			val.append( (String)opText.get( op.getSymbol().getType() ) );
			val.append(",");
			val.append( getFullForm(ctx.getChild(i+1)) );
		}
		val.append("]");
		return val.toString();
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitCirclePlus(FoxySheepParser.CirclePlusContext ctx) {
		return makeHeadList("CirclePlus", ctx.expr());
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
		return makeHeadList("Intersection", ctx.expr());
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
			return makeHeadList("Xor", ctx.expr());
		}
		return makeHeadList("Xnor", ctx.expr());
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitComposition(FoxySheepParser.CompositionContext ctx) {
		return makeHeadList("Composition", ctx.expr());
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
			return makeHeadList("Plus", ctx.expr());
		}
		if(ctx.BINARYMINUS() != null){
			//Mathematica interprets x-y as Plus[x,Times[-1,y]].
			StringBuilder val = new StringBuilder("Plus[");
			val.append( getFullForm(ctx.expr(0)) );
			for(int i = 1; i < ctx.expr().size(); i++){
				val.append(",Times[-1,");
				val.append( getFullForm(ctx.expr(i)) );
				val.append("]");
			}
			val.append("]");
			
			return val.toString();
		}
		if(ctx.BINARYPLUSMINUS() != null){
			return makeHeadList("PlusMinus", ctx.expr());
		}
		if(ctx.BINARYMINUSPLUS() != null){
			return makeHeadList("MinusPlus", ctx.expr());
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
		return makeHeadList("VerticalSeparator", ctx.expr());
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
		return makeHeadList("Union", ctx.expr());
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
			return makeHeadList("Nor", ctx.expr());
		}
		return makeHeadList("Or", ctx.expr());
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
		return makeHeadList("Cup", ctx.expr());
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
		return makeHeadList("StringExpression", ctx.expr());
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
			return makeHeadList("Nand", ctx.expr());
		}
		return makeHeadList("And", ctx.expr());
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
		return makeHeadList("RightComposition", ctx.expr());
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
		return makeHeadList("NonCommutativeMultiply", ctx.expr());
	}
	
	/**
	 * {@inheritDoc}
	 *
	 * <p>This is code factored out of both visitSpanA and visitSpanB.</p>
	 */
	public String visitSpan(ParserRuleContext ctx){
		StringBuilder val = new StringBuilder("Span[");
		int curChild = 0;
		
		//Because this SpanA might have been created by a subtree rewrite, we
		//cannot guarantee it begins with an expr.
		if( ctx.getChild(curChild).getText().equals(";;") ){
			//Begins with ";;", implicit start of 1.
			val.append( "1" );
			curChild++;
		}else{
			//Begins with expr
			val.append( getFullForm(ctx.getChild(curChild)  ) );
			curChild += 2;
		}
		//Cursor now points to one past the first ";;"
		if( curChild < ctx.children.size() && !ctx.getChild(curChild).getText().equals(";;") ){
			//The middle expr has not been omitted
			val.append( "," );
			val.append( getFullForm(ctx.getChild(curChild)) );
			curChild++;
		}else{
			//The middle expr has been omitted.
			val.append(",All");
		}
		
		//Cursor now points to either the second ";;" or past the end of the expr.
		if( curChild < ctx.children.size() && ctx.getChild(curChild).getText().equals(";;") ){
			//There is a skip amount.
			val.append( "," );
			val.append( getFullForm( ctx.getChild(curChild + 1)   ) );
		}

		val.append("]");
		return val.toString();
	}
	
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitSpanA(FoxySheepParser.SpanAContext ctx) {
		return visitSpan(ctx);
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitSpanB(FoxySheepParser.SpanBContext ctx) { 
		return visitSpan(ctx);
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
			return makeHeadList("Element", ctx.expr());
		}
		if(ctx.NOTELEMENT() != null){
			return makeHeadList("NotElement", ctx.expr());
		}
		if(ctx.SUBSET() != null){
			return makeHeadList("Subset", ctx.expr());
		}
		//if(ctx.SUPERSET() != null)
		return makeHeadList("Superset", ctx.expr());
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitCircleDot(FoxySheepParser.CircleDotContext ctx) {
		return makeHeadList("CircleDot", ctx.expr());
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitWedge(FoxySheepParser.WedgeContext ctx) {
		return makeHeadList("Wedge", ctx.expr());
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
		return makeHeadList("Colon", ctx.expr());
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
		return makeHeadList("Cap", ctx.expr());
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
		return makeHeadList("Alternatives", ctx.expr());
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
		return makeHeadList("Diamond", ctx.expr());
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
		return makeHeadList("CenterDot", ctx.expr());
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
		return makeHeadList("Equivalent", ctx.expr());
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitCoproduct(FoxySheepParser.CoproductContext ctx) {
		return makeHeadList("Coproduct", ctx.expr());
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitSmallCircle(FoxySheepParser.SmallCircleContext ctx) {
		return makeHeadList("SmallCircle", ctx.expr());
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
		return makeHeadList("Times", ctx.expr());
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
		return makeHeadList("Dot", ctx.expr());
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitCircleTimes(FoxySheepParser.CircleTimesContext ctx) {
		return makeHeadList("CircleTimes", ctx.expr());
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitSame(FoxySheepParser.SameContext ctx) {
		if(ctx.TRIPPLEEQUAL() != null){
			return makeHeadList("SameQ", ctx.expr()); 
		}
		return makeHeadList("UnsameQ", ctx.expr());
	}
	/**
	 * {@inheritDoc}
	 *
	 * <p>The default implementation returns the result of calling
	 * {@link #visitChildren} on {@code ctx}.</p>
	 */
	@Override public String visitStar(FoxySheepParser.StarContext ctx) {
		return makeHeadList("Star", ctx.children );
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
