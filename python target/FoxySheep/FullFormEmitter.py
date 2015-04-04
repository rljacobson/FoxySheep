# Generated from java-escape by ANTLR 4.5
from antlr4 import *
from generated.FoxySheepVisitor import *
from generated.FoxySheepParser import *

# This class defines a complete generic visitor for a parse tree produced by FoxySheepParser.

class FullFormEmitter(FoxySheepVisitor):
    # Gets the FullForm of the ParseTree e.
    def getFullForm(self, e):
        if isinstance(e, TerminalNode):
            return e.getText()

        return self.visit(e)

    # Makes string of the form head[e1, e2, ...]
    def makeHead(self, head, *args):
        argtext = ",".join(map(self.getFullForm, args))
        return "%s[%s]" % (head, argtext)

    # Makes string of the form head[e1, e2, ...]
    def makeHeadList(self, head, efunction):
        # We assume efunction is a function of an integer i. This awkward
        # interface is from antlr4's python api.
        elist = self.getChildList(efunction)
        argtext = ",".join(map(self.getFullForm, elist))
        return "%s[%s]" % (head, argtext)

    # Convert antlr4's awkward functional api to a list.
    def getChildList(self, efunction):
        # We assume efunction is a function of an integer i. This awkward
        # interface is from antlr4's python api.
        elist = []
        i = 0
        e = efunction(i)
        while e is not None:
            elist.append(e)
            i += 1
            e = efunction(i)
        return elist

    # Visit a parse tree produced by FoxySheepParser#prog.
    def visitProg(self, ctx):
        exprList = self.getChildList(ctx.expr)
        return "\n\n".join(map(self.getFullForm, exprList))


    # Visit a parse tree produced by FoxySheepParser#Unset.
    def visitUnset(self, ctx):
        return self.makeHead("Unset", ctx.expr())


    # Visit a parse tree produced by FoxySheepParser#Condition.
    def visitCondition(self, ctx):
        return self.makeHeadList("Condition", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#Implies.
    def visitImplies(self, ctx):
        return self.makeHeadList("Implies", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#CompoundExpression.
    def visitCompoundExpression(self, ctx):
        # Since we need to check for ending in "Null" anyway, we might as
        # well not bother with makeHeadList().
        val = "CompoundExpression["
        val += self.getFullForm(ctx.getChild(0))

        for i in range(2, ctx.getChildCount(), 2):
            val += "," + self.getFullForm(ctx.getChild(i))

        if ctx.getChildCount() % 2 == 0:
            # An even number of children means we ended in a semicolon.
            val += ",Null]"
        else:
            val += "]"

        return val


    # Visit a parse tree produced by FoxySheepParser#VerticalBar.
    def visitVerticalBar(self, ctx):
        if ctx.VERTICALBAR() is not None:
            return self.makeHeadList("VerticalBar", ctx.expr)
        if ctx.NOTVERTICALBAR() is not None:
            return self.makeHeadList("NotVerticalBar", ctx.expr)
        if ctx.DOUBLEVERTICALBAR() is not None:
            return self.makeHeadList("DoubleVerticalBar", ctx.expr)
        # if(ctx.NOTDOUBLEVERTICALBAR() != null){
        return self.makeHeadList("NotDoubleVerticalBar", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#VerticalTilde.
    def visitVerticalTilde(self, ctx):
        return self.makeHeadList("VerticalTilde", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#Vee.
    def visitVee(self, ctx):
        return self.makeHeadList("Vee", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#Cross.
    def visitCross(self, ctx):
        return self.makeHeadList("Cross", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#StringJoin.
    def visitStringJoin(self, ctx):
        return self.makeHeadList("StringJoin", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#Comparison.
    def visitComparison(self, ctx):
        # This is a rather complicated construct, because:
        # 		"x==y" 		-> Equal[x,y]
        # 		"x==y>z" 	-> Inequality[x, Equal, y, Greater, z]
        # 		"x==y==z		-> Equal[x,y,z]
        # 		"x>y>z"		-> Greater[x,y,z]
        # So we need to flatten many different operators at once
        # if necessary.
        #
        # We solve this problem by postprocessing the syntax tree
        # to flatten the tree where appropriate.

        opText = {
            FoxySheepParser.EqualSymbol: "Equal",
            FoxySheepParser.NotEqualSymbol: "Unequal",
            FoxySheepParser.GREATER: "Greater",
            FoxySheepParser.GreaterEqualSymbol: "GreaterEqual",
            FoxySheepParser.LESS: "Less",
            FoxySheepParser.LessEqualSymbol: "LessEqual"
        }

        allSame = True
        opType = ctx.getChild(1).getSymbol().type
        for i in range(3, ctx.getChildCount(), 2):
            allSame = allSame and (opType == ctx.getChild(i).getSymbol().type)

        # If all operators are the same, make a "head" with that operator.
        if allSame:
            return self.makeHeadList(opText[opType], ctx.expr)

        # All operators are not the same. We need to create an Inequality[].
        val = "Inequality["
        val += self.getFullForm(ctx.expr(0))
        for i in range(1, ctx.getChildCount(), 2):
            val += ","
            op = ctx.getChild(i)
            val += opText[ op.getSymbol().type ]
            val += "," + self.getFullForm(ctx.getChild(i+1))
        val += "]"

        return val


    # Visit a parse tree produced by FoxySheepParser#CirclePlus.
    def visitCirclePlus(self, ctx):
        return self.makeHeadList("CirclePlus", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#Tee.
    def visitTee(self, ctx):
        if ctx.LEFTTEE() is not None:
            return self.makeHeadList("LeftTee", ctx.expr)
        if ctx.DOUBLELEFTTEE() is not None:
            return self.makeHeadList("DoubleLeftTee", ctx.expr)
        if ctx.UPTEE() is not None:
            return self.makeHeadList("UpTee", ctx.expr)
        return self.makeHeadList("DownTee", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#Intersection.
    def visitIntersection(self, ctx):
        return self.makeHeadList("Intersection", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#Increment.
    def visitIncrement(self, ctx):
        if ctx.DOUBLEMINUS() is None:
            return self.makeHead("Increment", ctx.expr())

        return self.makeHead("Decrement", ctx.expr())


    # Visit a parse tree produced by FoxySheepParser#Slot.
    def visitSlot(self, ctx):
        return self.getFullForm(ctx.slotExpression())


    # Visit a parse tree produced by FoxySheepParser#Set.
    def visitSet(self, ctx):
        if ctx.EQUAL() is not None:
            return self.makeHeadList("Set", ctx.expr)
        if ctx.COLONEQUAL() is not None:
            return self.makeHeadList("SetDelayed", ctx.expr)
        if ctx.CARETEQUAL() is not None:
            return self.makeHeadList("UpSet", ctx.expr)
        if ctx.CARETCOLONEQUAL() is not None:
            return self.makeHeadList("UpSetDelayed", ctx.expr)

        #if(ctx.FUNCTIONARROW() != null)
        val = "Function[{"
        val += self.getFullForm(ctx.expr(0))
        val += "},"
        val += self.getFullForm(ctx.expr(1))
        val +="]"

        return val

    # Visit a parse tree produced by FoxySheepParser#Xor.
    def visitXor(self, ctx):
        if ctx.XOR() is not None:
            return self.makeHeadList("Xor", ctx.expr)
        return self.makeHeadList("Xnor", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#Composition.
    def visitComposition(self, ctx):
        return self.makeHeadList("Composition", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#Out.
    def visitOut(self, ctx):
        return self.getFullForm(ctx.outExpression())


    # Visit a parse tree produced by FoxySheepParser#Integrate.
    def visitIntegrate(self, ctx):
        return self.makeHeadList("Integrate", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#Accessor.
    def visitAccessor(self, ctx):
        return self.makeHead("Part", ctx.expr(), ctx.accessExpression())


    # Visit a parse tree produced by FoxySheepParser#HeadExpression.
    def visitHeadExpression(self, ctx):
        return self.makeHead(self.getFullForm(ctx.expr()), ctx.expressionList())


    # Visit a parse tree produced by FoxySheepParser#Therefore.
    def visitTherefore(self, ctx):
        return self.makeHeadList("Therefore", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#Square.
    def visitSquare(self, ctx):
        return self.makeHead("Square", ctx.expr())


    # Visit a parse tree produced by FoxySheepParser#Put.
    def visitPut(self, ctx):
        if ctx.DOUBLEGREATER() is not None:
            return self.makeHead("Put", ctx.expr(), ctx.StringLiteral())
        return self.makeHead("PutAppend", ctx.expr(), ctx.StringLiteral())


    # Visit a parse tree produced by FoxySheepParser#PlusOp.
    def visitPlusOp(self, ctx):
        if ctx.BINARYPLUS() is not None:
            return self.makeHeadList("Plus", ctx.expr)
        if ctx.BINARYMINUS() is not None:
            val = "Plus["
            exprList = self.getChildList(ctx.expr)
            val += self.getFullForm(exprList[0])
            for e in exprList[1:]:
                val += ",Times[-1,"
                val += self.getFullForm(e)
                val += "]"
            val += "]"
            return val

        if ctx.BINARYPLUSMINUS() is not None:
            return self.makeHeadList("PlusMinus", ctx.expr)

        # if ctx.BINARYMINUSPLUS() is not None:
        return self.makeHeadList("MinusPlus", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#Power.
    def visitPower(self, ctx):
        return self.makeHeadList("Power", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#VerticalSeparator.
    def visitVerticalSeparator(self, ctx):
        return self.makeHeadList("VerticalSeparator", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#Union.
    def visitUnion(self, ctx):
        return self.makeHeadList("Union", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#PreIncrement.
    def visitPreIncrement(self, ctx):
        if ctx.DOUBLEMINUS() is None:
            return self.makeHead("PreIncrement", ctx.expr())
        return self.makeHead("PreDecrement", ctx.expr())


    # Visit a parse tree produced by FoxySheepParser#Prefix.
    def visitPrefix(self, ctx):
        return self.makeHead( self.getFullForm(ctx.expr(0)), ctx.expr(1) )


    # Visit a parse tree produced by FoxySheepParser#Floor.
    def visitFloor(self, ctx):
        return self.makeHead("Floor", ctx.expr() )

    # Visit a parse tree produced by FoxySheepParser#Because.
    def visitBecause(self, ctx):
        return self.makeHeadList("Because", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#BracketingBar.
    def visitBracketingBar(self, ctx):
        return self.makeHead("BracketingBar", ctx.expressionList())


    # Visit a parse tree produced by FoxySheepParser#RightTee.
    def visitRightTee(self, ctx):
        if ctx.RIGHTTEE() is not None:
            return self.makeHeadList("RightTee", ctx.expr)
        return self.makeHeadList("DoubleRightTee", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#Or.
    def visitOr(self, ctx):
        if ctx.NOR() is not None:
            return self.makeHeadList("Nor", ctx.expr)
        return self.makeHeadList("Or", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#Cup.
    def visitCup(self, ctx):
        return self.makeHeadList("Cup", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#BoxParen.
    def visitBoxParen(self, ctx):
        return ctx.getText()


    # Visit a parse tree produced by FoxySheepParser#StringExpression.
    def visitStringExpression(self, ctx):
        return self.makeHeadList("StringExpression", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#Postfix.
    def visitPostfix(self, ctx):
        val = self.getFullForm(ctx.expr(1))
        val += "["
        val += self.getFullForm(ctx.expr(0))
        val += "]"
        return val


    # Visit a parse tree produced by FoxySheepParser#And.
    def visitAnd(self, ctx):
        if ctx.NAND() != None:
            return self.makeHeadList("Nand", ctx.expr)

        return self.makeHeadList("And", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#Optional.
    def visitOptional(self, ctx):
        return self.makeHeadList("Optional", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#PatternTest.
    def visitPatternTest(self, ctx):
        return self.makeHeadList("PatternTest", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#RightComposition.
    def visitRightComposition(self, ctx):
        return self.makeHeadList("RightComposition", ctx.expr())


    # Visit a parse tree produced by FoxySheepParser#NonCommutativeMultiply.
    def visitNonCommutativeMultiply(self, ctx):
        return self.makeHeadList("NonCommutativeMultiply", ctx.expr)


    # This is code factored out of both visitSpanA and visitSpanB.
    def visitSpan(self, ctx):
        val = "Span["
        curChild = 0

        # Because this SpanA might have been created by a subtree rewrite, we
        # cannot guarantee it begins with an expr.
        if ctx.getChild(curChild).getText() == ";;":
            # Begins with ";;", implicit start of 1.
            val += "1"
            curChild += 1
        else:
            # Begins with expr
            val += self.getFullForm(ctx.getChild(curChild))
            curChild += 2

        # Cursor now points to one past the first ";;".
        if ctx.getChild(curChild) is not None and ctx.getChild(curChild).getText() != ";;":
            # The middle expr has not been omitted
            val += ","
            val += self.getFullForm(ctx.getChild(curChild))
            curChild += 1
        else:
            val += ",All"

        # Cursor now points to either the second ";;" or past the end of the expr.
        if ctx.getChild(curChild) is not None and ctx.getChild(curChild).getText() == ";;":
            # There is a skip amount.
            val += ","
            val += self.getFullForm(ctx.getChild(curChild + 1))

        val += "]"
        return val

    # Visit a parse tree produced by FoxySheepParser#SpanA.
    def visitSpanA(self, ctx):
        return self.visitSpan(ctx)

    # Visit a parse tree produced by FoxySheepParser#SpanB.
    def visitSpanB(self, ctx):
        return self.visitSpan(ctx)

    # Visit a parse tree produced by FoxySheepParser#Parentheses.
    def visitParentheses(self, ctx):
        return self.getFullForm(ctx.expr())


    # Visit a parse tree produced by FoxySheepParser#Infix.
    def visitInfix(self, ctx):
        return self.makeHead( self.getFullForm(ctx.expr(1)), ctx.expr(0), ctx.expr(2) )


    # Visit a parse tree produced by FoxySheepParser#Factorial.
    def visitFactorial(self, ctx):
        if ctx.BANG() is None:
            return self.makeHead("Factorial", ctx.expr())

        return self.makeHead("Factorial2", ctx.expr())


    # Visit a parse tree produced by FoxySheepParser#SuchThat.
    def visitSuchThat(self, ctx):
        return self.makeHeadList("SuchThat", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#DoubleBracketingBar.
    def visitDoubleBracketingBar(self, ctx):
        return self.makeHead("DoubleBracketingBar", ctx.expressionList())


    # Visit a parse tree produced by FoxySheepParser#NumberLiteral.
    def visitNumberLiteral(self, ctx):
        return ctx.getText()


    # Visit a parse tree produced by FoxySheepParser#SetContainment.
    def visitSetContainment(self, ctx):
        if ctx.ELEMENT() is not None:
            return self.makeHeadList("Element", ctx.expr)
        if ctx.NOTELEMENT() is not None:
            return self.makeHeadList("NotElement", ctx.expr)
        if ctx.SUBSET() is not None:
            return self.makeHeadList("Subset", ctx.expr)

        # if(ctx.SUPERSET() != null)
        return self.makeHeadList("Superset", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#CircleDot.
    def visitCircleDot(self, ctx):
        return self.makeHeadList("CircleDot", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#Del.
    def visitDel(self, ctx):
        return self.makeHead("Del", ctx.expr())


    # Visit a parse tree produced by FoxySheepParser#Wedge.
    def visitWedge(self, ctx):
        return self.makeHeadList("Wedge", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#Colon.
    def visitColon(self, ctx):
        return self.makeHeadList("Colon", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#BoxConstructor.
    def visitBoxConstructor(self, ctx):
        return ctx.getText()


    # Visit a parse tree produced by FoxySheepParser#OpEquals.
    def visitOpEquals(self, ctx):
        if ctx.PLUSEQUAL() is not None:
            return self.makeHeadList("AddTo", ctx.expr)
        if ctx.MINUSEQUAL() is not None:
            return self.makeHeadList("SubtractFrom", ctx.expr)
        if ctx.ASTERISKEQUAL() is not None:
            return self.makeHeadList("TimesBy", ctx.expr)

        # if(ctx.SLASHEQUAL() != null){
        return self.makeHeadList("DivideBy", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#Cap.
    def visitCap(self, ctx):
        return self.makeHeadList("Cap", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#Alternatives.
    def visitAlternatives(self, ctx):
        return self.makeHeadList("Alternatives", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#AngleBracket.
    def visitAngleBracket(self, ctx):
        return self.makeHead("AngleBracket", ctx.expressionList())


    # Visit a parse tree produced by FoxySheepParser#ReplaceAll.
    def visitReplaceAll(self, ctx):
        if ctx.SLASHDOT() is not None:
            return self.makeHeadList("ReplaceAll", ctx.expr)
        return self.makeHeadList("ReplaceRepeated", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#TagUnset.
    def visitTagUnset(self, ctx):
        return self.makeHead("TagUnset", ctx.symbol(), ctx.expr())


    # Visit a parse tree produced by FoxySheepParser#Divide.
    def visitDivide(self, ctx):
        if ctx.DIVIDE() is not None:
            return self.makeHeadList("Divide", ctx.expr)

        # Mathematica treats x/y as Times[x,Power[y,-1]].
        val = "Times["
        val += self.getFullForm(ctx.expr(0))
        val += ",Power["
        val += self.getFullForm(ctx.expr(1))
        val += ",-1]]"

        return val


    # Visit a parse tree produced by FoxySheepParser#Diamond.
    def visitDiamond(self, ctx):
        return self.makeHeadList("Diamond", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#List.
    def visitList(self, ctx):
        return self.makeHead("List", ctx.expressionList())


    # Visit a parse tree produced by FoxySheepParser#MapApply.
    def visitMapApply(self, ctx):
        # expr (MAP | MAPALL | DOUBLEAT | TRIPPLEAT) expr
        if ctx.MAP() is not None:
            return self.makeHeadList("Map", ctx.expr)
        if ctx.MAPALL() is not None:
            return self.makeHeadList("MapAll", ctx.expr)
        if ctx.DOUBLEAT() is not None:
            return self.makeHeadList("Apply", ctx.expr)
        # if(ctx.TRIPPLEAT()!=null)
        # We can't use makeHead because the third argument isn't a ParseTree.
        # Apply[expr1,expr2,{1}]
        val = "Apply["
        val += self.getFullForm(ctx.expr(0))
        val += ","
        val += self.getFullForm(ctx.expr(1))
        val += ",List[1]]"

        return val


    # Visit a parse tree produced by FoxySheepParser#CenterDot.
    def visitCenterDot(self, ctx):
        return self.makeHeadList("CenterDot", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#Conjugate.
    def visitConjugate(self, ctx):
        if ctx.CONJUGATE() is not None:
            return self.makeHead("Conjugate", ctx.expr())
        if ctx.TRANSPOSE() is not None:
            return self.makeHead("Transpose", ctx.expr())

        # The other two are the same.
        # if(ctx.CONJUGATETRANSPOSE()!=null)
        # if(ctx.HERMITIANCONJUGATE()!=null)

        return self.makeHead("ConjugateTranspose", ctx.expr())


    # Visit a parse tree produced by FoxySheepParser#StringLiteral.
    def visitStringLiteral(self, ctx):
        return ctx.getText()


    # Visit a parse tree produced by FoxySheepParser#Equivalent.
    def visitEquivalent(self, ctx):
        return self.makeHeadList("Equivalent", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#Coproduct.
    def visitCoproduct(self, ctx):
        return self.makeHeadList("Coproduct", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#Message.
    def visitMessage(self, ctx):
        # One string literal.
        if ctx.StringLiteral(1) is None:
            return self.makeHead("MessageName", ctx.expr(), ctx.StringLiteral(0))
        # Two string literals.
        return self.makeHead("MessageName", ctx.expr(), ctx.StringLiteral(0), ctx.StringLiteral(1))


    # Visit a parse tree produced by FoxySheepParser#SmallCircle.
    def visitSmallCircle(self, ctx):
        return self.makeHeadList("SmallCircle", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#Function.
    def visitFunction(self, ctx):
        return self.makeHead("Function", ctx.expr())


    # Visit a parse tree produced by FoxySheepParser#PatternExp.
    def visitPatternExp(self, ctx):
        # symb:expr
        return self.makeHead("Pattern", ctx.symbol(), ctx.expr())


    # Visit a parse tree produced by FoxySheepParser#Times.
    def visitTimes(self, ctx):
        return self.makeHeadList("Times", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#Rule.
    def visitRule(self, ctx):
        if ctx.MINUSGREATER() is not None or ctx.RARROW() is not None:
            return self.makeHeadList("Rule", ctx.expr)
        return self.makeHeadList("RuleDelayed", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#SymbolLiteral.
    def visitSymbolLiteral(self, ctx):
        # FullForm of a symbol is itself.
        return ctx.getText()


    # Visit a parse tree produced by FoxySheepParser#TagSet.
    def visitTagSet(self, ctx):
        if ctx.EQUAL() is not None:
            return self.makeHead("TagSet", ctx.symbol(), ctx.expr(0), ctx.expr(1))
        # Must be TagSetDelated.
        return self.makeHead("TagSetDelayed", ctx.symbol(), ctx.expr(0), ctx.expr(1))


    # Visit a parse tree produced by FoxySheepParser#Ceiling.
    def visitCeiling(self, ctx):
        return self.makeHead("Ceiling", ctx.expr())


    # Visit a parse tree produced by FoxySheepParser#Not.
    def visitNot(self, ctx):
        return self.makeHead("Not", ctx.expr())


    # Visit a parse tree produced by FoxySheepParser#Backslash.
    def visitBackslash(self, ctx):
        return self.makeHeadList("Backslash", ctx.expr);


    # Visit a parse tree produced by FoxySheepParser#Dot.
    def visitDot(self, ctx):
        return self.makeHeadList("Dot", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#UnaryPlusMinus.
    def visitUnaryPlusMinus(self, ctx):
        if ctx.MINUS() is not None:
            val = "Times[-1,"
            val += self.getFullForm(ctx.expr())
            val += "]"
            return val
        if ctx.PLUS() is not None:
            return self.makeHead("Plus", ctx.expr())
        if ctx.PLUSMINUS() is not None:
            return self.makeHead("PlusMinus", ctx.expr())

        return self.makeHead("MinusPlus", ctx.expr())


    # Visit a parse tree produced by FoxySheepParser#CircleTimes.
    def visitCircleTimes(self, ctx):
        return self.makeHeadList("CircleTimes", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#Same.
    def visitSame(self, ctx):
        if ctx.TRIPPLEEQUAL() is not None:
            return self.makeHeadList("SameQ", ctx.expr)
        return self.makeHeadList("UnsameQ", ctx.expr)

    # Visit a parse tree produced by FoxySheepParser#Star.
    def visitStar(self, ctx):
        return self.makeHeadList("Star", ctx.expr )


    # Visit a parse tree produced by FoxySheepParser#Derivative.
    def visitDerivative(self, ctx):
        val = "Derivative["

        # We have to count the single quotes. The antlr4 python api
        # makes this awkward.
        count = 0
        while ctx.SINGLEQUOTE(count) is not None:
            count +=1
        val += str(count)

        val += "]["
        val += self.getFullForm(ctx.expr())
        val += "]"

        return val


    # Visit a parse tree produced by FoxySheepParser#Get.
    def visitGet(self, ctx):
        return self.makeHead("Get", ctx.StringLiteral())


    # Visit a parse tree produced by FoxySheepParser#Repeated.
    def visitRepeated(self, ctx):
        if ctx.DOUBLEDOT() is not None:
            return self.makeHead("Repeated", ctx.expr())
        return self.makeHead("RepeatedNull", ctx.expr())


    # Visit a parse tree produced by FoxySheepParser#CircleMinus.
    def visitCircleMinus(self, ctx):
        return self.makeHeadList("CircleMinus", ctx.expr)


    # Visit a parse tree produced by FoxySheepParser#ContextName.
    def visitContextName(self, ctx):
        return ctx.getText()


    # Visit a parse tree produced by FoxySheepParser#SimpleContext.
    def visitSimpleContext(self, ctx):
        return ctx.getText()


    # Visit a parse tree produced by FoxySheepParser#CompoundContext.
    def visitCompoundContext(self, ctx):
        return ctx.getText()


    # Visit a parse tree produced by FoxySheepParser#PatternBlanks.
    def visitPatternBlanks(self, ctx):
        val = ""
        if ctx.TRIPPLEBLANK() is not None:
            val += "BlankNullSequence["
            if ctx.expr() is not None:
                val += self.getFullForm(ctx.expr())
            val += "]"
        if ctx.DOUBLEBLANK() is not None:
            val += "BlankSequence["
            if ctx.expr() is not None:
                val += self.getFullForm(ctx.expr())
            val += "]"
        if ctx.BLANK() is not None:
            val += "Blank["
            if ctx.expr() is not None:
                val += self.getFullForm(ctx.expr())
            val += "]"

        # If there is a symbol, we wrap the whole expression in Pattern[]
        if ctx.symbol() is not None:
            wrap = "Pattern["
            wrap += self.getFullForm(ctx.symbol())
            wrap += ","
            val = wrap + val + "]"

        return val


    # Visit a parse tree produced by FoxySheepParser#PatternBlankDot.
    def visitPatternBlankDot(self, ctx):
        val = ""
        if ctx.symbol() is not None:
            val = "Optional[Pattern["
            val += self.getFullForm(ctx.symbol())
            val += ",Blank[]]]"
        else:
            val = "Optional[Blank[]]"

        return val


    # Visit a parse tree produced by FoxySheepParser#OutNumbered.
    def visitOutNumbered(self, ctx):
        val = "Out["
        val += ctx.getText()[1:]
        val += "]"
        return val


    # Visit a parse tree produced by FoxySheepParser#OutUnnumbered.
    def visitOutUnnumbered(self, ctx):
        textLen = len(ctx.getText())
        if textLen == 1:
            return "Out[]"
        return "Out[-" + str(textLen) + "]"


    # Visit a parse tree produced by FoxySheepParser#SlotDigits.
    def visitSlotDigits(self, ctx):
        val = "Slot["
        val += ctx.getText()[1:]
        val += "]"
        return val


    # Visit a parse tree produced by FoxySheepParser#SlotNamed.
    def visitSlotNamed(self, ctx):
        val = "Slot["
        val += ctx.getText()[1:]
        val += "]"
        return val


    # Visit a parse tree produced by FoxySheepParser#SlotSequenceDigits.
    def visitSlotSequenceDigits(self, ctx):
        val = "SlotSequence["
        val += ctx.getText()[2:]
        val += "]"
        return val


    # Visit a parse tree produced by FoxySheepParser#SlotSequence.
    def visitSlotSequence(self, ctx):
        return "SlotSequence[1]"


    # Visit a parse tree produced by FoxySheepParser#SlotUnnamed.
    def visitSlotUnnamed(self, ctx):
        return "Slot[1]"


    # Visit a parse tree produced by FoxySheepParser#ExpressionListed.
    def visitExpressionListed(self, ctx):
        # expressionList can be empty.
        if not hasattr(ctx, "children") or ctx.getChildCount()==0:
            return ""

        val = ""
        exprCounter = 0

        # We need a c-style for-loop here, because we need to be able to
        # increment the counter inside the loop.
        childCounter = 0
        while childCounter < ctx.getChildCount():
            # Separate with comma.
            if childCounter > 0:
                val += ","

            child = ctx.getChild(childCounter)
            if child is ctx.expr(exprCounter):
                val += self.getFullForm(child)
                exprCounter += 1
                # //The next child is a comma (or end of list) which we skip.
                childCounter += 1
            else:
                # Must have been a comma indicating Null.
                val += "Null"
            childCounter += 1

        # If the comma is the last child, it needs to be followed by a Null, too.
        if not isinstance(ctx.getChild(ctx.getChildCount() - 1), FoxySheepParser.ExprContext):
            val += ",Null"

        return val


    # Visit a parse tree produced by FoxySheepParser#AccessExpressionA.
    def visitAccessExpressionA(self, ctx):
        return self.getFullForm(ctx.expressionList())


    # Visit a parse tree produced by FoxySheepParser#AccessExpressionB.
    def visitAccessExpressionB(self, ctx):
        return self.getFullForm(ctx.expressionList())


    # Visit a parse tree produced by FoxySheepParser#box.
    def visitBox(self, ctx):
        return ctx.getText()


