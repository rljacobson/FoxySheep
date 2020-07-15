# Generated from FoxySheep.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .FoxySheepParser import FoxySheepParser
else:
    from FoxySheepParser import FoxySheepParser

# This class defines a complete generic visitor for a parse tree produced by FoxySheepParser.

class FoxySheepVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by FoxySheepParser#prog.
    def visitProg(self, ctx:FoxySheepParser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#PatternExp.
    def visitPatternExp(self, ctx:FoxySheepParser.PatternExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Or.
    def visitOr(self, ctx:FoxySheepParser.OrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Conjugate.
    def visitConjugate(self, ctx:FoxySheepParser.ConjugateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Ceiling.
    def visitCeiling(self, ctx:FoxySheepParser.CeilingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Infix.
    def visitInfix(self, ctx:FoxySheepParser.InfixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Therefore.
    def visitTherefore(self, ctx:FoxySheepParser.ThereforeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#TagUnset.
    def visitTagUnset(self, ctx:FoxySheepParser.TagUnsetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Accessor.
    def visitAccessor(self, ctx:FoxySheepParser.AccessorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#CircleMinus.
    def visitCircleMinus(self, ctx:FoxySheepParser.CircleMinusContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Divide.
    def visitDivide(self, ctx:FoxySheepParser.DivideContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Implies.
    def visitImplies(self, ctx:FoxySheepParser.ImpliesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#PlusOp.
    def visitPlusOp(self, ctx:FoxySheepParser.PlusOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#RightComposition.
    def visitRightComposition(self, ctx:FoxySheepParser.RightCompositionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#NonCommutativeMultiply.
    def visitNonCommutativeMultiply(self, ctx:FoxySheepParser.NonCommutativeMultiplyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#List.
    def visitList(self, ctx:FoxySheepParser.ListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Cup.
    def visitCup(self, ctx:FoxySheepParser.CupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Same.
    def visitSame(self, ctx:FoxySheepParser.SameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Optional.
    def visitOptional(self, ctx:FoxySheepParser.OptionalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#SuchThat.
    def visitSuchThat(self, ctx:FoxySheepParser.SuchThatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#DoubleBracketingBar.
    def visitDoubleBracketingBar(self, ctx:FoxySheepParser.DoubleBracketingBarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#PatternBlankDot.
    def visitPatternBlankDot(self, ctx:FoxySheepParser.PatternBlankDotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Dot.
    def visitDot(self, ctx:FoxySheepParser.DotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#VerticalBar.
    def visitVerticalBar(self, ctx:FoxySheepParser.VerticalBarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Square.
    def visitSquare(self, ctx:FoxySheepParser.SquareContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Alternatives.
    def visitAlternatives(self, ctx:FoxySheepParser.AlternativesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Out.
    def visitOut(self, ctx:FoxySheepParser.OutContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#BoxConstructor.
    def visitBoxConstructor(self, ctx:FoxySheepParser.BoxConstructorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Not.
    def visitNot(self, ctx:FoxySheepParser.NotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Postfix.
    def visitPostfix(self, ctx:FoxySheepParser.PostfixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#PatternBlanks.
    def visitPatternBlanks(self, ctx:FoxySheepParser.PatternBlanksContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#UnaryPlusMinus.
    def visitUnaryPlusMinus(self, ctx:FoxySheepParser.UnaryPlusMinusContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Cap.
    def visitCap(self, ctx:FoxySheepParser.CapContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#CirclePlus.
    def visitCirclePlus(self, ctx:FoxySheepParser.CirclePlusContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Because.
    def visitBecause(self, ctx:FoxySheepParser.BecauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#StringLiteral.
    def visitStringLiteral(self, ctx:FoxySheepParser.StringLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#And.
    def visitAnd(self, ctx:FoxySheepParser.AndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Get.
    def visitGet(self, ctx:FoxySheepParser.GetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Equivalent.
    def visitEquivalent(self, ctx:FoxySheepParser.EquivalentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#CompoundExpression.
    def visitCompoundExpression(self, ctx:FoxySheepParser.CompoundExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Derivative.
    def visitDerivative(self, ctx:FoxySheepParser.DerivativeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Slot.
    def visitSlot(self, ctx:FoxySheepParser.SlotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#RightTee.
    def visitRightTee(self, ctx:FoxySheepParser.RightTeeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Xor.
    def visitXor(self, ctx:FoxySheepParser.XorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Rule.
    def visitRule(self, ctx:FoxySheepParser.RuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#HeadExpression.
    def visitHeadExpression(self, ctx:FoxySheepParser.HeadExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#ReplaceAll.
    def visitReplaceAll(self, ctx:FoxySheepParser.ReplaceAllContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Intersection.
    def visitIntersection(self, ctx:FoxySheepParser.IntersectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#PreIncrement.
    def visitPreIncrement(self, ctx:FoxySheepParser.PreIncrementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Integrate.
    def visitIntegrate(self, ctx:FoxySheepParser.IntegrateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Set.
    def visitSet(self, ctx:FoxySheepParser.SetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#OpEquals.
    def visitOpEquals(self, ctx:FoxySheepParser.OpEqualsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Message.
    def visitMessage(self, ctx:FoxySheepParser.MessageContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Cross.
    def visitCross(self, ctx:FoxySheepParser.CrossContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#PatternTest.
    def visitPatternTest(self, ctx:FoxySheepParser.PatternTestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Prefix.
    def visitPrefix(self, ctx:FoxySheepParser.PrefixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Backslash.
    def visitBackslash(self, ctx:FoxySheepParser.BackslashContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Repeated.
    def visitRepeated(self, ctx:FoxySheepParser.RepeatedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#MapApply.
    def visitMapApply(self, ctx:FoxySheepParser.MapApplyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Union.
    def visitUnion(self, ctx:FoxySheepParser.UnionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#VerticalSeparator.
    def visitVerticalSeparator(self, ctx:FoxySheepParser.VerticalSeparatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Factorial.
    def visitFactorial(self, ctx:FoxySheepParser.FactorialContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#SpanA.
    def visitSpanA(self, ctx:FoxySheepParser.SpanAContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Function.
    def visitFunction(self, ctx:FoxySheepParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Number.
    def visitNumber(self, ctx:FoxySheepParser.NumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Star.
    def visitStar(self, ctx:FoxySheepParser.StarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Comparison.
    def visitComparison(self, ctx:FoxySheepParser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#TagSet.
    def visitTagSet(self, ctx:FoxySheepParser.TagSetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Increment.
    def visitIncrement(self, ctx:FoxySheepParser.IncrementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#VerticalTilde.
    def visitVerticalTilde(self, ctx:FoxySheepParser.VerticalTildeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Colon.
    def visitColon(self, ctx:FoxySheepParser.ColonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#SmallCircle.
    def visitSmallCircle(self, ctx:FoxySheepParser.SmallCircleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Parentheses.
    def visitParentheses(self, ctx:FoxySheepParser.ParenthesesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#SpanB.
    def visitSpanB(self, ctx:FoxySheepParser.SpanBContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Condition.
    def visitCondition(self, ctx:FoxySheepParser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Floor.
    def visitFloor(self, ctx:FoxySheepParser.FloorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Composition.
    def visitComposition(self, ctx:FoxySheepParser.CompositionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#CircleDot.
    def visitCircleDot(self, ctx:FoxySheepParser.CircleDotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#SymbolLiteral.
    def visitSymbolLiteral(self, ctx:FoxySheepParser.SymbolLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#CircleTimes.
    def visitCircleTimes(self, ctx:FoxySheepParser.CircleTimesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Unset.
    def visitUnset(self, ctx:FoxySheepParser.UnsetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Del.
    def visitDel(self, ctx:FoxySheepParser.DelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Diamond.
    def visitDiamond(self, ctx:FoxySheepParser.DiamondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Wedge.
    def visitWedge(self, ctx:FoxySheepParser.WedgeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Put.
    def visitPut(self, ctx:FoxySheepParser.PutContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#StringJoin.
    def visitStringJoin(self, ctx:FoxySheepParser.StringJoinContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Tee.
    def visitTee(self, ctx:FoxySheepParser.TeeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#SetContainment.
    def visitSetContainment(self, ctx:FoxySheepParser.SetContainmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Vee.
    def visitVee(self, ctx:FoxySheepParser.VeeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#CenterDot.
    def visitCenterDot(self, ctx:FoxySheepParser.CenterDotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Times.
    def visitTimes(self, ctx:FoxySheepParser.TimesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#StringExpression.
    def visitStringExpression(self, ctx:FoxySheepParser.StringExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#BracketingBar.
    def visitBracketingBar(self, ctx:FoxySheepParser.BracketingBarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Coproduct.
    def visitCoproduct(self, ctx:FoxySheepParser.CoproductContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#AngleBracket.
    def visitAngleBracket(self, ctx:FoxySheepParser.AngleBracketContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#Power.
    def visitPower(self, ctx:FoxySheepParser.PowerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#ContextName.
    def visitContextName(self, ctx:FoxySheepParser.ContextNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#SimpleContext.
    def visitSimpleContext(self, ctx:FoxySheepParser.SimpleContextContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#CompoundContext.
    def visitCompoundContext(self, ctx:FoxySheepParser.CompoundContextContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#NumberBaseN.
    def visitNumberBaseN(self, ctx:FoxySheepParser.NumberBaseNContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#NumberBaseTen.
    def visitNumberBaseTen(self, ctx:FoxySheepParser.NumberBaseTenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#numberLiteralPrecision.
    def visitNumberLiteralPrecision(self, ctx:FoxySheepParser.NumberLiteralPrecisionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#numberLiteralExponent.
    def visitNumberLiteralExponent(self, ctx:FoxySheepParser.NumberLiteralExponentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#OutNumbered.
    def visitOutNumbered(self, ctx:FoxySheepParser.OutNumberedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#OutUnnumbered.
    def visitOutUnnumbered(self, ctx:FoxySheepParser.OutUnnumberedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#SlotDigits.
    def visitSlotDigits(self, ctx:FoxySheepParser.SlotDigitsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#SlotNamed.
    def visitSlotNamed(self, ctx:FoxySheepParser.SlotNamedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#SlotSequenceDigits.
    def visitSlotSequenceDigits(self, ctx:FoxySheepParser.SlotSequenceDigitsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#SlotSequence.
    def visitSlotSequence(self, ctx:FoxySheepParser.SlotSequenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#SlotUnnamed.
    def visitSlotUnnamed(self, ctx:FoxySheepParser.SlotUnnamedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#ExpressionListed.
    def visitExpressionListed(self, ctx:FoxySheepParser.ExpressionListedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#AccessExpressionA.
    def visitAccessExpressionA(self, ctx:FoxySheepParser.AccessExpressionAContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FoxySheepParser#AccessExpressionB.
    def visitAccessExpressionB(self, ctx:FoxySheepParser.AccessExpressionBContext):
        return self.visitChildren(ctx)



del FoxySheepParser