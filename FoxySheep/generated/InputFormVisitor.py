# Generated from InputForm.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .InputFormParser import InputFormParser
else:
    from InputFormParser import InputFormParser

# This class defines a complete generic visitor for a parse tree produced by InputFormParser.

class InputFormVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by InputFormParser#prog.
    def visitProg(self, ctx:InputFormParser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#PatternExp.
    def visitPatternExp(self, ctx:InputFormParser.PatternExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Or.
    def visitOr(self, ctx:InputFormParser.OrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Conjugate.
    def visitConjugate(self, ctx:InputFormParser.ConjugateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Ceiling.
    def visitCeiling(self, ctx:InputFormParser.CeilingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Infix.
    def visitInfix(self, ctx:InputFormParser.InfixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Therefore.
    def visitTherefore(self, ctx:InputFormParser.ThereforeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#TagUnset.
    def visitTagUnset(self, ctx:InputFormParser.TagUnsetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Accessor.
    def visitAccessor(self, ctx:InputFormParser.AccessorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#CircleMinus.
    def visitCircleMinus(self, ctx:InputFormParser.CircleMinusContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Divide.
    def visitDivide(self, ctx:InputFormParser.DivideContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Implies.
    def visitImplies(self, ctx:InputFormParser.ImpliesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#PlusOp.
    def visitPlusOp(self, ctx:InputFormParser.PlusOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#RightComposition.
    def visitRightComposition(self, ctx:InputFormParser.RightCompositionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#NonCommutativeMultiply.
    def visitNonCommutativeMultiply(self, ctx:InputFormParser.NonCommutativeMultiplyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#List.
    def visitList(self, ctx:InputFormParser.ListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Cup.
    def visitCup(self, ctx:InputFormParser.CupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Same.
    def visitSame(self, ctx:InputFormParser.SameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Optional.
    def visitOptional(self, ctx:InputFormParser.OptionalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#SuchThat.
    def visitSuchThat(self, ctx:InputFormParser.SuchThatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#DoubleBracketingBar.
    def visitDoubleBracketingBar(self, ctx:InputFormParser.DoubleBracketingBarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#PatternBlankDot.
    def visitPatternBlankDot(self, ctx:InputFormParser.PatternBlankDotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Dot.
    def visitDot(self, ctx:InputFormParser.DotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#VerticalBar.
    def visitVerticalBar(self, ctx:InputFormParser.VerticalBarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Square.
    def visitSquare(self, ctx:InputFormParser.SquareContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Alternatives.
    def visitAlternatives(self, ctx:InputFormParser.AlternativesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Out.
    def visitOut(self, ctx:InputFormParser.OutContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#BoxConstructor.
    def visitBoxConstructor(self, ctx:InputFormParser.BoxConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Not.
    def visitNot(self, ctx:InputFormParser.NotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Postfix.
    def visitPostfix(self, ctx:InputFormParser.PostfixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#PatternBlanks.
    def visitPatternBlanks(self, ctx:InputFormParser.PatternBlanksContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#UnaryPlusMinus.
    def visitUnaryPlusMinus(self, ctx:InputFormParser.UnaryPlusMinusContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Cap.
    def visitCap(self, ctx:InputFormParser.CapContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#CirclePlus.
    def visitCirclePlus(self, ctx:InputFormParser.CirclePlusContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Because.
    def visitBecause(self, ctx:InputFormParser.BecauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#StringLiteral.
    def visitStringLiteral(self, ctx:InputFormParser.StringLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#And.
    def visitAnd(self, ctx:InputFormParser.AndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Get.
    def visitGet(self, ctx:InputFormParser.GetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Equivalent.
    def visitEquivalent(self, ctx:InputFormParser.EquivalentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#CompoundExpression.
    def visitCompoundExpression(self, ctx:InputFormParser.CompoundExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Derivative.
    def visitDerivative(self, ctx:InputFormParser.DerivativeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Slot.
    def visitSlot(self, ctx:InputFormParser.SlotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#RightTee.
    def visitRightTee(self, ctx:InputFormParser.RightTeeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Xor.
    def visitXor(self, ctx:InputFormParser.XorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Rule.
    def visitRule(self, ctx:InputFormParser.RuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#HeadExpression.
    def visitHeadExpression(self, ctx:InputFormParser.HeadExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#ReplaceAll.
    def visitReplaceAll(self, ctx:InputFormParser.ReplaceAllContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Intersection.
    def visitIntersection(self, ctx:InputFormParser.IntersectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#PreIncrement.
    def visitPreIncrement(self, ctx:InputFormParser.PreIncrementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Integrate.
    def visitIntegrate(self, ctx:InputFormParser.IntegrateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Set.
    def visitSet(self, ctx:InputFormParser.SetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#OpEquals.
    def visitOpEquals(self, ctx:InputFormParser.OpEqualsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Message.
    def visitMessage(self, ctx:InputFormParser.MessageContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Cross.
    def visitCross(self, ctx:InputFormParser.CrossContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#PatternTest.
    def visitPatternTest(self, ctx:InputFormParser.PatternTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Prefix.
    def visitPrefix(self, ctx:InputFormParser.PrefixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Backslash.
    def visitBackslash(self, ctx:InputFormParser.BackslashContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Repeated.
    def visitRepeated(self, ctx:InputFormParser.RepeatedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#MapApply.
    def visitMapApply(self, ctx:InputFormParser.MapApplyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Union.
    def visitUnion(self, ctx:InputFormParser.UnionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#VerticalSeparator.
    def visitVerticalSeparator(self, ctx:InputFormParser.VerticalSeparatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Factorial.
    def visitFactorial(self, ctx:InputFormParser.FactorialContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#SpanA.
    def visitSpanA(self, ctx:InputFormParser.SpanAContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Function.
    def visitFunction(self, ctx:InputFormParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Number.
    def visitNumber(self, ctx:InputFormParser.NumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Star.
    def visitStar(self, ctx:InputFormParser.StarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Comparison.
    def visitComparison(self, ctx:InputFormParser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#TagSet.
    def visitTagSet(self, ctx:InputFormParser.TagSetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Increment.
    def visitIncrement(self, ctx:InputFormParser.IncrementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#VerticalTilde.
    def visitVerticalTilde(self, ctx:InputFormParser.VerticalTildeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Colon.
    def visitColon(self, ctx:InputFormParser.ColonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#SmallCircle.
    def visitSmallCircle(self, ctx:InputFormParser.SmallCircleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Parentheses.
    def visitParentheses(self, ctx:InputFormParser.ParenthesesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#SpanB.
    def visitSpanB(self, ctx:InputFormParser.SpanBContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Condition.
    def visitCondition(self, ctx:InputFormParser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Floor.
    def visitFloor(self, ctx:InputFormParser.FloorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Composition.
    def visitComposition(self, ctx:InputFormParser.CompositionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#CircleDot.
    def visitCircleDot(self, ctx:InputFormParser.CircleDotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#SymbolLiteral.
    def visitSymbolLiteral(self, ctx:InputFormParser.SymbolLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#CircleTimes.
    def visitCircleTimes(self, ctx:InputFormParser.CircleTimesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Unset.
    def visitUnset(self, ctx:InputFormParser.UnsetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Del.
    def visitDel(self, ctx:InputFormParser.DelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Diamond.
    def visitDiamond(self, ctx:InputFormParser.DiamondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Wedge.
    def visitWedge(self, ctx:InputFormParser.WedgeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Put.
    def visitPut(self, ctx:InputFormParser.PutContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#StringJoin.
    def visitStringJoin(self, ctx:InputFormParser.StringJoinContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Tee.
    def visitTee(self, ctx:InputFormParser.TeeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#SetContainment.
    def visitSetContainment(self, ctx:InputFormParser.SetContainmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Vee.
    def visitVee(self, ctx:InputFormParser.VeeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#CenterDot.
    def visitCenterDot(self, ctx:InputFormParser.CenterDotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Times.
    def visitTimes(self, ctx:InputFormParser.TimesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#StringExpression.
    def visitStringExpression(self, ctx:InputFormParser.StringExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#BracketingBar.
    def visitBracketingBar(self, ctx:InputFormParser.BracketingBarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Coproduct.
    def visitCoproduct(self, ctx:InputFormParser.CoproductContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#AngleBracket.
    def visitAngleBracket(self, ctx:InputFormParser.AngleBracketContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#Power.
    def visitPower(self, ctx:InputFormParser.PowerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#ContextName.
    def visitContextName(self, ctx:InputFormParser.ContextNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#SimpleContext.
    def visitSimpleContext(self, ctx:InputFormParser.SimpleContextContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#CompoundContext.
    def visitCompoundContext(self, ctx:InputFormParser.CompoundContextContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#NumberBaseN.
    def visitNumberBaseN(self, ctx:InputFormParser.NumberBaseNContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#NumberBaseTen.
    def visitNumberBaseTen(self, ctx:InputFormParser.NumberBaseTenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#numberLiteralPrecision.
    def visitNumberLiteralPrecision(self, ctx:InputFormParser.NumberLiteralPrecisionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#numberLiteralExponent.
    def visitNumberLiteralExponent(self, ctx:InputFormParser.NumberLiteralExponentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#OutNumbered.
    def visitOutNumbered(self, ctx:InputFormParser.OutNumberedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#OutUnnumbered.
    def visitOutUnnumbered(self, ctx:InputFormParser.OutUnnumberedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#SlotDigits.
    def visitSlotDigits(self, ctx:InputFormParser.SlotDigitsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#SlotNamed.
    def visitSlotNamed(self, ctx:InputFormParser.SlotNamedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#SlotSequenceDigits.
    def visitSlotSequenceDigits(self, ctx:InputFormParser.SlotSequenceDigitsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#SlotSequence.
    def visitSlotSequence(self, ctx:InputFormParser.SlotSequenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#SlotUnnamed.
    def visitSlotUnnamed(self, ctx:InputFormParser.SlotUnnamedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#ExpressionListed.
    def visitExpressionListed(self, ctx:InputFormParser.ExpressionListedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#AccessExpressionA.
    def visitAccessExpressionA(self, ctx:InputFormParser.AccessExpressionAContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by InputFormParser#AccessExpressionB.
    def visitAccessExpressionB(self, ctx:InputFormParser.AccessExpressionBContext):
        return self.visitChildren(ctx)



del InputFormParser