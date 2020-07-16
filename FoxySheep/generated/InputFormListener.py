# Generated from InputForm.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .InputFormParser import InputFormParser
else:
    from InputFormParser import InputFormParser

# This class defines a complete listener for a parse tree produced by InputFormParser.
class InputFormListener(ParseTreeListener):

    # Enter a parse tree produced by InputFormParser#prog.
    def enterProg(self, ctx:InputFormParser.ProgContext):
        pass

    # Exit a parse tree produced by InputFormParser#prog.
    def exitProg(self, ctx:InputFormParser.ProgContext):
        pass


    # Enter a parse tree produced by InputFormParser#PatternExp.
    def enterPatternExp(self, ctx:InputFormParser.PatternExpContext):
        pass

    # Exit a parse tree produced by InputFormParser#PatternExp.
    def exitPatternExp(self, ctx:InputFormParser.PatternExpContext):
        pass


    # Enter a parse tree produced by InputFormParser#Or.
    def enterOr(self, ctx:InputFormParser.OrContext):
        pass

    # Exit a parse tree produced by InputFormParser#Or.
    def exitOr(self, ctx:InputFormParser.OrContext):
        pass


    # Enter a parse tree produced by InputFormParser#Conjugate.
    def enterConjugate(self, ctx:InputFormParser.ConjugateContext):
        pass

    # Exit a parse tree produced by InputFormParser#Conjugate.
    def exitConjugate(self, ctx:InputFormParser.ConjugateContext):
        pass


    # Enter a parse tree produced by InputFormParser#Ceiling.
    def enterCeiling(self, ctx:InputFormParser.CeilingContext):
        pass

    # Exit a parse tree produced by InputFormParser#Ceiling.
    def exitCeiling(self, ctx:InputFormParser.CeilingContext):
        pass


    # Enter a parse tree produced by InputFormParser#Infix.
    def enterInfix(self, ctx:InputFormParser.InfixContext):
        pass

    # Exit a parse tree produced by InputFormParser#Infix.
    def exitInfix(self, ctx:InputFormParser.InfixContext):
        pass


    # Enter a parse tree produced by InputFormParser#Therefore.
    def enterTherefore(self, ctx:InputFormParser.ThereforeContext):
        pass

    # Exit a parse tree produced by InputFormParser#Therefore.
    def exitTherefore(self, ctx:InputFormParser.ThereforeContext):
        pass


    # Enter a parse tree produced by InputFormParser#TagUnset.
    def enterTagUnset(self, ctx:InputFormParser.TagUnsetContext):
        pass

    # Exit a parse tree produced by InputFormParser#TagUnset.
    def exitTagUnset(self, ctx:InputFormParser.TagUnsetContext):
        pass


    # Enter a parse tree produced by InputFormParser#Accessor.
    def enterAccessor(self, ctx:InputFormParser.AccessorContext):
        pass

    # Exit a parse tree produced by InputFormParser#Accessor.
    def exitAccessor(self, ctx:InputFormParser.AccessorContext):
        pass


    # Enter a parse tree produced by InputFormParser#CircleMinus.
    def enterCircleMinus(self, ctx:InputFormParser.CircleMinusContext):
        pass

    # Exit a parse tree produced by InputFormParser#CircleMinus.
    def exitCircleMinus(self, ctx:InputFormParser.CircleMinusContext):
        pass


    # Enter a parse tree produced by InputFormParser#Divide.
    def enterDivide(self, ctx:InputFormParser.DivideContext):
        pass

    # Exit a parse tree produced by InputFormParser#Divide.
    def exitDivide(self, ctx:InputFormParser.DivideContext):
        pass


    # Enter a parse tree produced by InputFormParser#Implies.
    def enterImplies(self, ctx:InputFormParser.ImpliesContext):
        pass

    # Exit a parse tree produced by InputFormParser#Implies.
    def exitImplies(self, ctx:InputFormParser.ImpliesContext):
        pass


    # Enter a parse tree produced by InputFormParser#PlusOp.
    def enterPlusOp(self, ctx:InputFormParser.PlusOpContext):
        pass

    # Exit a parse tree produced by InputFormParser#PlusOp.
    def exitPlusOp(self, ctx:InputFormParser.PlusOpContext):
        pass


    # Enter a parse tree produced by InputFormParser#RightComposition.
    def enterRightComposition(self, ctx:InputFormParser.RightCompositionContext):
        pass

    # Exit a parse tree produced by InputFormParser#RightComposition.
    def exitRightComposition(self, ctx:InputFormParser.RightCompositionContext):
        pass


    # Enter a parse tree produced by InputFormParser#NonCommutativeMultiply.
    def enterNonCommutativeMultiply(self, ctx:InputFormParser.NonCommutativeMultiplyContext):
        pass

    # Exit a parse tree produced by InputFormParser#NonCommutativeMultiply.
    def exitNonCommutativeMultiply(self, ctx:InputFormParser.NonCommutativeMultiplyContext):
        pass


    # Enter a parse tree produced by InputFormParser#List.
    def enterList(self, ctx:InputFormParser.ListContext):
        pass

    # Exit a parse tree produced by InputFormParser#List.
    def exitList(self, ctx:InputFormParser.ListContext):
        pass


    # Enter a parse tree produced by InputFormParser#Cup.
    def enterCup(self, ctx:InputFormParser.CupContext):
        pass

    # Exit a parse tree produced by InputFormParser#Cup.
    def exitCup(self, ctx:InputFormParser.CupContext):
        pass


    # Enter a parse tree produced by InputFormParser#Same.
    def enterSame(self, ctx:InputFormParser.SameContext):
        pass

    # Exit a parse tree produced by InputFormParser#Same.
    def exitSame(self, ctx:InputFormParser.SameContext):
        pass


    # Enter a parse tree produced by InputFormParser#Optional.
    def enterOptional(self, ctx:InputFormParser.OptionalContext):
        pass

    # Exit a parse tree produced by InputFormParser#Optional.
    def exitOptional(self, ctx:InputFormParser.OptionalContext):
        pass


    # Enter a parse tree produced by InputFormParser#SuchThat.
    def enterSuchThat(self, ctx:InputFormParser.SuchThatContext):
        pass

    # Exit a parse tree produced by InputFormParser#SuchThat.
    def exitSuchThat(self, ctx:InputFormParser.SuchThatContext):
        pass


    # Enter a parse tree produced by InputFormParser#DoubleBracketingBar.
    def enterDoubleBracketingBar(self, ctx:InputFormParser.DoubleBracketingBarContext):
        pass

    # Exit a parse tree produced by InputFormParser#DoubleBracketingBar.
    def exitDoubleBracketingBar(self, ctx:InputFormParser.DoubleBracketingBarContext):
        pass


    # Enter a parse tree produced by InputFormParser#PatternBlankDot.
    def enterPatternBlankDot(self, ctx:InputFormParser.PatternBlankDotContext):
        pass

    # Exit a parse tree produced by InputFormParser#PatternBlankDot.
    def exitPatternBlankDot(self, ctx:InputFormParser.PatternBlankDotContext):
        pass


    # Enter a parse tree produced by InputFormParser#Dot.
    def enterDot(self, ctx:InputFormParser.DotContext):
        pass

    # Exit a parse tree produced by InputFormParser#Dot.
    def exitDot(self, ctx:InputFormParser.DotContext):
        pass


    # Enter a parse tree produced by InputFormParser#VerticalBar.
    def enterVerticalBar(self, ctx:InputFormParser.VerticalBarContext):
        pass

    # Exit a parse tree produced by InputFormParser#VerticalBar.
    def exitVerticalBar(self, ctx:InputFormParser.VerticalBarContext):
        pass


    # Enter a parse tree produced by InputFormParser#Square.
    def enterSquare(self, ctx:InputFormParser.SquareContext):
        pass

    # Exit a parse tree produced by InputFormParser#Square.
    def exitSquare(self, ctx:InputFormParser.SquareContext):
        pass


    # Enter a parse tree produced by InputFormParser#Alternatives.
    def enterAlternatives(self, ctx:InputFormParser.AlternativesContext):
        pass

    # Exit a parse tree produced by InputFormParser#Alternatives.
    def exitAlternatives(self, ctx:InputFormParser.AlternativesContext):
        pass


    # Enter a parse tree produced by InputFormParser#Out.
    def enterOut(self, ctx:InputFormParser.OutContext):
        pass

    # Exit a parse tree produced by InputFormParser#Out.
    def exitOut(self, ctx:InputFormParser.OutContext):
        pass


    # Enter a parse tree produced by InputFormParser#BoxConstructor.
    def enterBoxConstructor(self, ctx:InputFormParser.BoxConstructorContext):
        pass

    # Exit a parse tree produced by InputFormParser#BoxConstructor.
    def exitBoxConstructor(self, ctx:InputFormParser.BoxConstructorContext):
        pass


    # Enter a parse tree produced by InputFormParser#Not.
    def enterNot(self, ctx:InputFormParser.NotContext):
        pass

    # Exit a parse tree produced by InputFormParser#Not.
    def exitNot(self, ctx:InputFormParser.NotContext):
        pass


    # Enter a parse tree produced by InputFormParser#Postfix.
    def enterPostfix(self, ctx:InputFormParser.PostfixContext):
        pass

    # Exit a parse tree produced by InputFormParser#Postfix.
    def exitPostfix(self, ctx:InputFormParser.PostfixContext):
        pass


    # Enter a parse tree produced by InputFormParser#PatternBlanks.
    def enterPatternBlanks(self, ctx:InputFormParser.PatternBlanksContext):
        pass

    # Exit a parse tree produced by InputFormParser#PatternBlanks.
    def exitPatternBlanks(self, ctx:InputFormParser.PatternBlanksContext):
        pass


    # Enter a parse tree produced by InputFormParser#UnaryPlusMinus.
    def enterUnaryPlusMinus(self, ctx:InputFormParser.UnaryPlusMinusContext):
        pass

    # Exit a parse tree produced by InputFormParser#UnaryPlusMinus.
    def exitUnaryPlusMinus(self, ctx:InputFormParser.UnaryPlusMinusContext):
        pass


    # Enter a parse tree produced by InputFormParser#Cap.
    def enterCap(self, ctx:InputFormParser.CapContext):
        pass

    # Exit a parse tree produced by InputFormParser#Cap.
    def exitCap(self, ctx:InputFormParser.CapContext):
        pass


    # Enter a parse tree produced by InputFormParser#CirclePlus.
    def enterCirclePlus(self, ctx:InputFormParser.CirclePlusContext):
        pass

    # Exit a parse tree produced by InputFormParser#CirclePlus.
    def exitCirclePlus(self, ctx:InputFormParser.CirclePlusContext):
        pass


    # Enter a parse tree produced by InputFormParser#Because.
    def enterBecause(self, ctx:InputFormParser.BecauseContext):
        pass

    # Exit a parse tree produced by InputFormParser#Because.
    def exitBecause(self, ctx:InputFormParser.BecauseContext):
        pass


    # Enter a parse tree produced by InputFormParser#StringLiteral.
    def enterStringLiteral(self, ctx:InputFormParser.StringLiteralContext):
        pass

    # Exit a parse tree produced by InputFormParser#StringLiteral.
    def exitStringLiteral(self, ctx:InputFormParser.StringLiteralContext):
        pass


    # Enter a parse tree produced by InputFormParser#And.
    def enterAnd(self, ctx:InputFormParser.AndContext):
        pass

    # Exit a parse tree produced by InputFormParser#And.
    def exitAnd(self, ctx:InputFormParser.AndContext):
        pass


    # Enter a parse tree produced by InputFormParser#Get.
    def enterGet(self, ctx:InputFormParser.GetContext):
        pass

    # Exit a parse tree produced by InputFormParser#Get.
    def exitGet(self, ctx:InputFormParser.GetContext):
        pass


    # Enter a parse tree produced by InputFormParser#Equivalent.
    def enterEquivalent(self, ctx:InputFormParser.EquivalentContext):
        pass

    # Exit a parse tree produced by InputFormParser#Equivalent.
    def exitEquivalent(self, ctx:InputFormParser.EquivalentContext):
        pass


    # Enter a parse tree produced by InputFormParser#CompoundExpression.
    def enterCompoundExpression(self, ctx:InputFormParser.CompoundExpressionContext):
        pass

    # Exit a parse tree produced by InputFormParser#CompoundExpression.
    def exitCompoundExpression(self, ctx:InputFormParser.CompoundExpressionContext):
        pass


    # Enter a parse tree produced by InputFormParser#Derivative.
    def enterDerivative(self, ctx:InputFormParser.DerivativeContext):
        pass

    # Exit a parse tree produced by InputFormParser#Derivative.
    def exitDerivative(self, ctx:InputFormParser.DerivativeContext):
        pass


    # Enter a parse tree produced by InputFormParser#Slot.
    def enterSlot(self, ctx:InputFormParser.SlotContext):
        pass

    # Exit a parse tree produced by InputFormParser#Slot.
    def exitSlot(self, ctx:InputFormParser.SlotContext):
        pass


    # Enter a parse tree produced by InputFormParser#RightTee.
    def enterRightTee(self, ctx:InputFormParser.RightTeeContext):
        pass

    # Exit a parse tree produced by InputFormParser#RightTee.
    def exitRightTee(self, ctx:InputFormParser.RightTeeContext):
        pass


    # Enter a parse tree produced by InputFormParser#Xor.
    def enterXor(self, ctx:InputFormParser.XorContext):
        pass

    # Exit a parse tree produced by InputFormParser#Xor.
    def exitXor(self, ctx:InputFormParser.XorContext):
        pass


    # Enter a parse tree produced by InputFormParser#Rule.
    def enterRule(self, ctx:InputFormParser.RuleContext):
        pass

    # Exit a parse tree produced by InputFormParser#Rule.
    def exitRule(self, ctx:InputFormParser.RuleContext):
        pass


    # Enter a parse tree produced by InputFormParser#HeadExpression.
    def enterHeadExpression(self, ctx:InputFormParser.HeadExpressionContext):
        pass

    # Exit a parse tree produced by InputFormParser#HeadExpression.
    def exitHeadExpression(self, ctx:InputFormParser.HeadExpressionContext):
        pass


    # Enter a parse tree produced by InputFormParser#ReplaceAll.
    def enterReplaceAll(self, ctx:InputFormParser.ReplaceAllContext):
        pass

    # Exit a parse tree produced by InputFormParser#ReplaceAll.
    def exitReplaceAll(self, ctx:InputFormParser.ReplaceAllContext):
        pass


    # Enter a parse tree produced by InputFormParser#Intersection.
    def enterIntersection(self, ctx:InputFormParser.IntersectionContext):
        pass

    # Exit a parse tree produced by InputFormParser#Intersection.
    def exitIntersection(self, ctx:InputFormParser.IntersectionContext):
        pass


    # Enter a parse tree produced by InputFormParser#PreIncrement.
    def enterPreIncrement(self, ctx:InputFormParser.PreIncrementContext):
        pass

    # Exit a parse tree produced by InputFormParser#PreIncrement.
    def exitPreIncrement(self, ctx:InputFormParser.PreIncrementContext):
        pass


    # Enter a parse tree produced by InputFormParser#Integrate.
    def enterIntegrate(self, ctx:InputFormParser.IntegrateContext):
        pass

    # Exit a parse tree produced by InputFormParser#Integrate.
    def exitIntegrate(self, ctx:InputFormParser.IntegrateContext):
        pass


    # Enter a parse tree produced by InputFormParser#Set.
    def enterSet(self, ctx:InputFormParser.SetContext):
        pass

    # Exit a parse tree produced by InputFormParser#Set.
    def exitSet(self, ctx:InputFormParser.SetContext):
        pass


    # Enter a parse tree produced by InputFormParser#OpEquals.
    def enterOpEquals(self, ctx:InputFormParser.OpEqualsContext):
        pass

    # Exit a parse tree produced by InputFormParser#OpEquals.
    def exitOpEquals(self, ctx:InputFormParser.OpEqualsContext):
        pass


    # Enter a parse tree produced by InputFormParser#Message.
    def enterMessage(self, ctx:InputFormParser.MessageContext):
        pass

    # Exit a parse tree produced by InputFormParser#Message.
    def exitMessage(self, ctx:InputFormParser.MessageContext):
        pass


    # Enter a parse tree produced by InputFormParser#Cross.
    def enterCross(self, ctx:InputFormParser.CrossContext):
        pass

    # Exit a parse tree produced by InputFormParser#Cross.
    def exitCross(self, ctx:InputFormParser.CrossContext):
        pass


    # Enter a parse tree produced by InputFormParser#PatternTest.
    def enterPatternTest(self, ctx:InputFormParser.PatternTestContext):
        pass

    # Exit a parse tree produced by InputFormParser#PatternTest.
    def exitPatternTest(self, ctx:InputFormParser.PatternTestContext):
        pass


    # Enter a parse tree produced by InputFormParser#Prefix.
    def enterPrefix(self, ctx:InputFormParser.PrefixContext):
        pass

    # Exit a parse tree produced by InputFormParser#Prefix.
    def exitPrefix(self, ctx:InputFormParser.PrefixContext):
        pass


    # Enter a parse tree produced by InputFormParser#Backslash.
    def enterBackslash(self, ctx:InputFormParser.BackslashContext):
        pass

    # Exit a parse tree produced by InputFormParser#Backslash.
    def exitBackslash(self, ctx:InputFormParser.BackslashContext):
        pass


    # Enter a parse tree produced by InputFormParser#Repeated.
    def enterRepeated(self, ctx:InputFormParser.RepeatedContext):
        pass

    # Exit a parse tree produced by InputFormParser#Repeated.
    def exitRepeated(self, ctx:InputFormParser.RepeatedContext):
        pass


    # Enter a parse tree produced by InputFormParser#MapApply.
    def enterMapApply(self, ctx:InputFormParser.MapApplyContext):
        pass

    # Exit a parse tree produced by InputFormParser#MapApply.
    def exitMapApply(self, ctx:InputFormParser.MapApplyContext):
        pass


    # Enter a parse tree produced by InputFormParser#Union.
    def enterUnion(self, ctx:InputFormParser.UnionContext):
        pass

    # Exit a parse tree produced by InputFormParser#Union.
    def exitUnion(self, ctx:InputFormParser.UnionContext):
        pass


    # Enter a parse tree produced by InputFormParser#VerticalSeparator.
    def enterVerticalSeparator(self, ctx:InputFormParser.VerticalSeparatorContext):
        pass

    # Exit a parse tree produced by InputFormParser#VerticalSeparator.
    def exitVerticalSeparator(self, ctx:InputFormParser.VerticalSeparatorContext):
        pass


    # Enter a parse tree produced by InputFormParser#Factorial.
    def enterFactorial(self, ctx:InputFormParser.FactorialContext):
        pass

    # Exit a parse tree produced by InputFormParser#Factorial.
    def exitFactorial(self, ctx:InputFormParser.FactorialContext):
        pass


    # Enter a parse tree produced by InputFormParser#SpanA.
    def enterSpanA(self, ctx:InputFormParser.SpanAContext):
        pass

    # Exit a parse tree produced by InputFormParser#SpanA.
    def exitSpanA(self, ctx:InputFormParser.SpanAContext):
        pass


    # Enter a parse tree produced by InputFormParser#Function.
    def enterFunction(self, ctx:InputFormParser.FunctionContext):
        pass

    # Exit a parse tree produced by InputFormParser#Function.
    def exitFunction(self, ctx:InputFormParser.FunctionContext):
        pass


    # Enter a parse tree produced by InputFormParser#Number.
    def enterNumber(self, ctx:InputFormParser.NumberContext):
        pass

    # Exit a parse tree produced by InputFormParser#Number.
    def exitNumber(self, ctx:InputFormParser.NumberContext):
        pass


    # Enter a parse tree produced by InputFormParser#Star.
    def enterStar(self, ctx:InputFormParser.StarContext):
        pass

    # Exit a parse tree produced by InputFormParser#Star.
    def exitStar(self, ctx:InputFormParser.StarContext):
        pass


    # Enter a parse tree produced by InputFormParser#Comparison.
    def enterComparison(self, ctx:InputFormParser.ComparisonContext):
        pass

    # Exit a parse tree produced by InputFormParser#Comparison.
    def exitComparison(self, ctx:InputFormParser.ComparisonContext):
        pass


    # Enter a parse tree produced by InputFormParser#TagSet.
    def enterTagSet(self, ctx:InputFormParser.TagSetContext):
        pass

    # Exit a parse tree produced by InputFormParser#TagSet.
    def exitTagSet(self, ctx:InputFormParser.TagSetContext):
        pass


    # Enter a parse tree produced by InputFormParser#Increment.
    def enterIncrement(self, ctx:InputFormParser.IncrementContext):
        pass

    # Exit a parse tree produced by InputFormParser#Increment.
    def exitIncrement(self, ctx:InputFormParser.IncrementContext):
        pass


    # Enter a parse tree produced by InputFormParser#VerticalTilde.
    def enterVerticalTilde(self, ctx:InputFormParser.VerticalTildeContext):
        pass

    # Exit a parse tree produced by InputFormParser#VerticalTilde.
    def exitVerticalTilde(self, ctx:InputFormParser.VerticalTildeContext):
        pass


    # Enter a parse tree produced by InputFormParser#Colon.
    def enterColon(self, ctx:InputFormParser.ColonContext):
        pass

    # Exit a parse tree produced by InputFormParser#Colon.
    def exitColon(self, ctx:InputFormParser.ColonContext):
        pass


    # Enter a parse tree produced by InputFormParser#SmallCircle.
    def enterSmallCircle(self, ctx:InputFormParser.SmallCircleContext):
        pass

    # Exit a parse tree produced by InputFormParser#SmallCircle.
    def exitSmallCircle(self, ctx:InputFormParser.SmallCircleContext):
        pass


    # Enter a parse tree produced by InputFormParser#Parentheses.
    def enterParentheses(self, ctx:InputFormParser.ParenthesesContext):
        pass

    # Exit a parse tree produced by InputFormParser#Parentheses.
    def exitParentheses(self, ctx:InputFormParser.ParenthesesContext):
        pass


    # Enter a parse tree produced by InputFormParser#SpanB.
    def enterSpanB(self, ctx:InputFormParser.SpanBContext):
        pass

    # Exit a parse tree produced by InputFormParser#SpanB.
    def exitSpanB(self, ctx:InputFormParser.SpanBContext):
        pass


    # Enter a parse tree produced by InputFormParser#Condition.
    def enterCondition(self, ctx:InputFormParser.ConditionContext):
        pass

    # Exit a parse tree produced by InputFormParser#Condition.
    def exitCondition(self, ctx:InputFormParser.ConditionContext):
        pass


    # Enter a parse tree produced by InputFormParser#Floor.
    def enterFloor(self, ctx:InputFormParser.FloorContext):
        pass

    # Exit a parse tree produced by InputFormParser#Floor.
    def exitFloor(self, ctx:InputFormParser.FloorContext):
        pass


    # Enter a parse tree produced by InputFormParser#Composition.
    def enterComposition(self, ctx:InputFormParser.CompositionContext):
        pass

    # Exit a parse tree produced by InputFormParser#Composition.
    def exitComposition(self, ctx:InputFormParser.CompositionContext):
        pass


    # Enter a parse tree produced by InputFormParser#CircleDot.
    def enterCircleDot(self, ctx:InputFormParser.CircleDotContext):
        pass

    # Exit a parse tree produced by InputFormParser#CircleDot.
    def exitCircleDot(self, ctx:InputFormParser.CircleDotContext):
        pass


    # Enter a parse tree produced by InputFormParser#SymbolLiteral.
    def enterSymbolLiteral(self, ctx:InputFormParser.SymbolLiteralContext):
        pass

    # Exit a parse tree produced by InputFormParser#SymbolLiteral.
    def exitSymbolLiteral(self, ctx:InputFormParser.SymbolLiteralContext):
        pass


    # Enter a parse tree produced by InputFormParser#CircleTimes.
    def enterCircleTimes(self, ctx:InputFormParser.CircleTimesContext):
        pass

    # Exit a parse tree produced by InputFormParser#CircleTimes.
    def exitCircleTimes(self, ctx:InputFormParser.CircleTimesContext):
        pass


    # Enter a parse tree produced by InputFormParser#Unset.
    def enterUnset(self, ctx:InputFormParser.UnsetContext):
        pass

    # Exit a parse tree produced by InputFormParser#Unset.
    def exitUnset(self, ctx:InputFormParser.UnsetContext):
        pass


    # Enter a parse tree produced by InputFormParser#Del.
    def enterDel(self, ctx:InputFormParser.DelContext):
        pass

    # Exit a parse tree produced by InputFormParser#Del.
    def exitDel(self, ctx:InputFormParser.DelContext):
        pass


    # Enter a parse tree produced by InputFormParser#Diamond.
    def enterDiamond(self, ctx:InputFormParser.DiamondContext):
        pass

    # Exit a parse tree produced by InputFormParser#Diamond.
    def exitDiamond(self, ctx:InputFormParser.DiamondContext):
        pass


    # Enter a parse tree produced by InputFormParser#Wedge.
    def enterWedge(self, ctx:InputFormParser.WedgeContext):
        pass

    # Exit a parse tree produced by InputFormParser#Wedge.
    def exitWedge(self, ctx:InputFormParser.WedgeContext):
        pass


    # Enter a parse tree produced by InputFormParser#Put.
    def enterPut(self, ctx:InputFormParser.PutContext):
        pass

    # Exit a parse tree produced by InputFormParser#Put.
    def exitPut(self, ctx:InputFormParser.PutContext):
        pass


    # Enter a parse tree produced by InputFormParser#StringJoin.
    def enterStringJoin(self, ctx:InputFormParser.StringJoinContext):
        pass

    # Exit a parse tree produced by InputFormParser#StringJoin.
    def exitStringJoin(self, ctx:InputFormParser.StringJoinContext):
        pass


    # Enter a parse tree produced by InputFormParser#Tee.
    def enterTee(self, ctx:InputFormParser.TeeContext):
        pass

    # Exit a parse tree produced by InputFormParser#Tee.
    def exitTee(self, ctx:InputFormParser.TeeContext):
        pass


    # Enter a parse tree produced by InputFormParser#SetContainment.
    def enterSetContainment(self, ctx:InputFormParser.SetContainmentContext):
        pass

    # Exit a parse tree produced by InputFormParser#SetContainment.
    def exitSetContainment(self, ctx:InputFormParser.SetContainmentContext):
        pass


    # Enter a parse tree produced by InputFormParser#Vee.
    def enterVee(self, ctx:InputFormParser.VeeContext):
        pass

    # Exit a parse tree produced by InputFormParser#Vee.
    def exitVee(self, ctx:InputFormParser.VeeContext):
        pass


    # Enter a parse tree produced by InputFormParser#CenterDot.
    def enterCenterDot(self, ctx:InputFormParser.CenterDotContext):
        pass

    # Exit a parse tree produced by InputFormParser#CenterDot.
    def exitCenterDot(self, ctx:InputFormParser.CenterDotContext):
        pass


    # Enter a parse tree produced by InputFormParser#Times.
    def enterTimes(self, ctx:InputFormParser.TimesContext):
        pass

    # Exit a parse tree produced by InputFormParser#Times.
    def exitTimes(self, ctx:InputFormParser.TimesContext):
        pass


    # Enter a parse tree produced by InputFormParser#StringExpression.
    def enterStringExpression(self, ctx:InputFormParser.StringExpressionContext):
        pass

    # Exit a parse tree produced by InputFormParser#StringExpression.
    def exitStringExpression(self, ctx:InputFormParser.StringExpressionContext):
        pass


    # Enter a parse tree produced by InputFormParser#BracketingBar.
    def enterBracketingBar(self, ctx:InputFormParser.BracketingBarContext):
        pass

    # Exit a parse tree produced by InputFormParser#BracketingBar.
    def exitBracketingBar(self, ctx:InputFormParser.BracketingBarContext):
        pass


    # Enter a parse tree produced by InputFormParser#Coproduct.
    def enterCoproduct(self, ctx:InputFormParser.CoproductContext):
        pass

    # Exit a parse tree produced by InputFormParser#Coproduct.
    def exitCoproduct(self, ctx:InputFormParser.CoproductContext):
        pass


    # Enter a parse tree produced by InputFormParser#AngleBracket.
    def enterAngleBracket(self, ctx:InputFormParser.AngleBracketContext):
        pass

    # Exit a parse tree produced by InputFormParser#AngleBracket.
    def exitAngleBracket(self, ctx:InputFormParser.AngleBracketContext):
        pass


    # Enter a parse tree produced by InputFormParser#Power.
    def enterPower(self, ctx:InputFormParser.PowerContext):
        pass

    # Exit a parse tree produced by InputFormParser#Power.
    def exitPower(self, ctx:InputFormParser.PowerContext):
        pass


    # Enter a parse tree produced by InputFormParser#ContextName.
    def enterContextName(self, ctx:InputFormParser.ContextNameContext):
        pass

    # Exit a parse tree produced by InputFormParser#ContextName.
    def exitContextName(self, ctx:InputFormParser.ContextNameContext):
        pass


    # Enter a parse tree produced by InputFormParser#SimpleContext.
    def enterSimpleContext(self, ctx:InputFormParser.SimpleContextContext):
        pass

    # Exit a parse tree produced by InputFormParser#SimpleContext.
    def exitSimpleContext(self, ctx:InputFormParser.SimpleContextContext):
        pass


    # Enter a parse tree produced by InputFormParser#CompoundContext.
    def enterCompoundContext(self, ctx:InputFormParser.CompoundContextContext):
        pass

    # Exit a parse tree produced by InputFormParser#CompoundContext.
    def exitCompoundContext(self, ctx:InputFormParser.CompoundContextContext):
        pass


    # Enter a parse tree produced by InputFormParser#NumberBaseN.
    def enterNumberBaseN(self, ctx:InputFormParser.NumberBaseNContext):
        pass

    # Exit a parse tree produced by InputFormParser#NumberBaseN.
    def exitNumberBaseN(self, ctx:InputFormParser.NumberBaseNContext):
        pass


    # Enter a parse tree produced by InputFormParser#NumberBaseTen.
    def enterNumberBaseTen(self, ctx:InputFormParser.NumberBaseTenContext):
        pass

    # Exit a parse tree produced by InputFormParser#NumberBaseTen.
    def exitNumberBaseTen(self, ctx:InputFormParser.NumberBaseTenContext):
        pass


    # Enter a parse tree produced by InputFormParser#numberLiteralPrecision.
    def enterNumberLiteralPrecision(self, ctx:InputFormParser.NumberLiteralPrecisionContext):
        pass

    # Exit a parse tree produced by InputFormParser#numberLiteralPrecision.
    def exitNumberLiteralPrecision(self, ctx:InputFormParser.NumberLiteralPrecisionContext):
        pass


    # Enter a parse tree produced by InputFormParser#numberLiteralExponent.
    def enterNumberLiteralExponent(self, ctx:InputFormParser.NumberLiteralExponentContext):
        pass

    # Exit a parse tree produced by InputFormParser#numberLiteralExponent.
    def exitNumberLiteralExponent(self, ctx:InputFormParser.NumberLiteralExponentContext):
        pass


    # Enter a parse tree produced by InputFormParser#OutNumbered.
    def enterOutNumbered(self, ctx:InputFormParser.OutNumberedContext):
        pass

    # Exit a parse tree produced by InputFormParser#OutNumbered.
    def exitOutNumbered(self, ctx:InputFormParser.OutNumberedContext):
        pass


    # Enter a parse tree produced by InputFormParser#OutUnnumbered.
    def enterOutUnnumbered(self, ctx:InputFormParser.OutUnnumberedContext):
        pass

    # Exit a parse tree produced by InputFormParser#OutUnnumbered.
    def exitOutUnnumbered(self, ctx:InputFormParser.OutUnnumberedContext):
        pass


    # Enter a parse tree produced by InputFormParser#SlotDigits.
    def enterSlotDigits(self, ctx:InputFormParser.SlotDigitsContext):
        pass

    # Exit a parse tree produced by InputFormParser#SlotDigits.
    def exitSlotDigits(self, ctx:InputFormParser.SlotDigitsContext):
        pass


    # Enter a parse tree produced by InputFormParser#SlotNamed.
    def enterSlotNamed(self, ctx:InputFormParser.SlotNamedContext):
        pass

    # Exit a parse tree produced by InputFormParser#SlotNamed.
    def exitSlotNamed(self, ctx:InputFormParser.SlotNamedContext):
        pass


    # Enter a parse tree produced by InputFormParser#SlotSequenceDigits.
    def enterSlotSequenceDigits(self, ctx:InputFormParser.SlotSequenceDigitsContext):
        pass

    # Exit a parse tree produced by InputFormParser#SlotSequenceDigits.
    def exitSlotSequenceDigits(self, ctx:InputFormParser.SlotSequenceDigitsContext):
        pass


    # Enter a parse tree produced by InputFormParser#SlotSequence.
    def enterSlotSequence(self, ctx:InputFormParser.SlotSequenceContext):
        pass

    # Exit a parse tree produced by InputFormParser#SlotSequence.
    def exitSlotSequence(self, ctx:InputFormParser.SlotSequenceContext):
        pass


    # Enter a parse tree produced by InputFormParser#SlotUnnamed.
    def enterSlotUnnamed(self, ctx:InputFormParser.SlotUnnamedContext):
        pass

    # Exit a parse tree produced by InputFormParser#SlotUnnamed.
    def exitSlotUnnamed(self, ctx:InputFormParser.SlotUnnamedContext):
        pass


    # Enter a parse tree produced by InputFormParser#ExpressionListed.
    def enterExpressionListed(self, ctx:InputFormParser.ExpressionListedContext):
        pass

    # Exit a parse tree produced by InputFormParser#ExpressionListed.
    def exitExpressionListed(self, ctx:InputFormParser.ExpressionListedContext):
        pass


    # Enter a parse tree produced by InputFormParser#AccessExpressionA.
    def enterAccessExpressionA(self, ctx:InputFormParser.AccessExpressionAContext):
        pass

    # Exit a parse tree produced by InputFormParser#AccessExpressionA.
    def exitAccessExpressionA(self, ctx:InputFormParser.AccessExpressionAContext):
        pass


    # Enter a parse tree produced by InputFormParser#AccessExpressionB.
    def enterAccessExpressionB(self, ctx:InputFormParser.AccessExpressionBContext):
        pass

    # Exit a parse tree produced by InputFormParser#AccessExpressionB.
    def exitAccessExpressionB(self, ctx:InputFormParser.AccessExpressionBContext):
        pass


