from antlr4 import TerminalNode
from FoxySheep.generated.InputFormVisitor import InputFormVisitor
from FoxySheep.generated.InputFormParser import InputFormParser

emitter = None


class FullFormEmitter(InputFormVisitor):
    """
    This class defines a complete generic visitor for a parse tree produced by InputFormParser.
    """

    def get_full_form(self, e) -> str:
        """
        Returns FullForm string for ParseTree `e`.
        """
        if isinstance(e, TerminalNode):
            return e.getText()

        return self.visit(e)

    #
    def make_head(self, head, *args):
        """
        Makes string of the form `"head[e1, e2, ...]"`.

        :param head: The head as a string.
        :param args: SyntatTree nodes `e1`, `e2`, ..., that will be converted to FullForm.
        :return: "head[e1, e2, ...]"
        """
        argtext = ",".join(map(self.get_full_form, args))
        return "%s[%s]" % (head, argtext)

    def make_head_list(self, head, efunction):
        """
        Makes string of the form `"head[e1, e2, ...]"`.

        We assume efunction is a function of an integer i. This awkward
        interface is from antlr4's python api.

        :param head: The head as a string.
        :param efunction: An ANTLR efunction giving efunction(i)=ei.
        :return: "head[e1, e2, ...]"
        """

        elist = self.get_children(efunction)
        argtext = ",".join(map(self.get_full_form, elist))
        return "%s[%s]" % (head, argtext)

    def get_children(self, efunction):
        """
        Convert antlr4's awkward functional api to a list.

        We assume efunction is a function of an integer i. This awkward
        interface is from antlr4's python api.

        :param efunction:
        :return:
        """

        elist = []
        i = 0
        e = efunction(i)
        while e is not None:
            elist.append(e)
            i += 1
            e = efunction(i)
        return elist

    # Visit a parse tree produced by InputFormParser#prog.
    def visitProg(self, ctx):
        exprList = self.get_children(ctx.expr)
        return "\n\n".join(map(self.get_full_form, exprList))

    # Visit a parse tree produced by InputFormParser#Unset.
    def visitUnset(self, ctx):
        return self.make_head("Unset", ctx.expr())

    # Visit a parse tree produced by InputFormParser#Condition.
    def visitCondition(self, ctx):
        return self.make_head_list("Condition", ctx.expr)

    # Visit a parse tree produced by InputFormParser#Implies.
    def visitImplies(self, ctx):
        return self.make_head_list("Implies", ctx.expr)

    # Visit a parse tree produced by InputFormParser#CompoundExpression.
    def visitCompoundExpression(self, ctx):
        # Since we need to check for ending in "Null" anyway, we might as
        # well not bother with make_head_list().
        val = "CompoundExpression["
        val += self.get_full_form(ctx.getChild(0))

        for i in range(2, ctx.getChildCount(), 2):
            val += "," + self.get_full_form(ctx.getChild(i))

        if ctx.getChildCount() % 2 == 0:
            # An even number of children means we ended in a semicolon.
            val += ",Null]"
        else:
            val += "]"

        return val

    # Visit a parse tree produced by InputFormParser#VerticalBar.
    def visitVerticalBar(self, ctx):
        if ctx.VERTICALBAR() is not None:
            return self.make_head_list("VerticalBar", ctx.expr)
        if ctx.NOTVERTICALBAR() is not None:
            return self.make_head_list("NotVerticalBar", ctx.expr)
        if ctx.DOUBLEVERTICALBAR() is not None:
            return self.make_head_list("DoubleVerticalBar", ctx.expr)
        # if(ctx.NOTDOUBLEVERTICALBAR() != null){
        return self.make_head_list("NotDoubleVerticalBar", ctx.expr)

    # Visit a parse tree produced by InputFormParser#VerticalTilde.
    def visitVerticalTilde(self, ctx):
        return self.make_head_list("VerticalTilde", ctx.expr)

    # Visit a parse tree produced by InputFormParser#Vee.
    def visitVee(self, ctx):
        return self.make_head_list("Vee", ctx.expr)

    # Visit a parse tree produced by InputFormParser#Cross.
    def visitCross(self, ctx):
        return self.make_head_list("Cross", ctx.expr)

    # Visit a parse tree produced by InputFormParser#StringJoin.
    def visitStringJoin(self, ctx):
        return self.make_head_list("StringJoin", ctx.expr)

    # Visit a parse tree produced by InputFormParser#Comparison.
    def visitComparison(self, ctx):
        """
        Visit a parse tree produced by InputFormParser#Comparison.

        This is a rather complicated construct, because:
        		"x==y" 		-> Equal[x,y]
        		"x==y>z" 	-> Inequality[x, Equal, y, Greater, z]
        		"x==y==z		-> Equal[x,y,z]
        		"x>y>z"		-> Greater[x,y,z]
        So we need to flatten many different operators at once
        if necessary.

        We solve this problem by postprocessing the syntax tree
        to flatten the tree where appropriate.

        :param ctx:
        :return: FullForm as a string.
        """

        op_text = {
            InputFormParser.EqualSymbol: "Equal",
            InputFormParser.NotEqualSymbol: "Unequal",
            InputFormParser.GREATER: "Greater",
            InputFormParser.GreaterEqualSymbol: "GreaterEqual",
            InputFormParser.LESS: "Less",
            InputFormParser.LessEqualSymbol: "LessEqual",
        }

        all_same = True
        opType = ctx.getChild(1).getSymbol().type
        for i in range(3, ctx.getChildCount(), 2):
            all_same = all_same and (opType == ctx.getChild(i).getSymbol().type)

        # If all operators are the same, make a "head" with that operator.
        if all_same:
            return self.make_head_list(op_text[opType], ctx.expr)

        # All operators are not the same. We need to create an Inequality[].
        val = "Inequality["
        val += self.get_full_form(ctx.expr(0))
        for i in range(1, ctx.getChildCount(), 2):
            val += ","
            op = ctx.getChild(i)
            val += op_text[op.getSymbol().type]
            val += "," + self.get_full_form(ctx.getChild(i + 1))
        val += "]"

        return val

    # Visit a parse tree produced by InputFormParser#CirclePlus.
    def visitCirclePlus(self, ctx):
        return self.make_head_list("CirclePlus", ctx.expr)

    # Visit a parse tree produced by InputFormParser#Tee.
    def visitTee(self, ctx):
        if ctx.LEFTTEE() is not None:
            return self.make_head_list("LeftTee", ctx.expr)
        if ctx.DOUBLELEFTTEE() is not None:
            return self.make_head_list("DoubleLeftTee", ctx.expr)
        if ctx.UPTEE() is not None:
            return self.make_head_list("UpTee", ctx.expr)
        return self.make_head_list("DownTee", ctx.expr)

    # Visit a parse tree produced by InputFormParser#Intersection.
    def visitIntersection(self, ctx):
        return self.make_head_list("Intersection", ctx.expr)

    # Visit a parse tree produced by InputFormParser#Increment.
    def visitIncrement(self, ctx):
        if ctx.DOUBLEMINUS() is None:
            return self.make_head("Increment", ctx.expr())

        return self.make_head("Decrement", ctx.expr())

    # Visit a parse tree produced by InputFormParser#Slot.
    def visitSlot(self, ctx):
        return self.get_full_form(ctx.slotExpression())

    # Visit a parse tree produced by InputFormParser#Set.
    def visitSet(self, ctx):
        if ctx.EQUAL() is not None:
            return self.make_head_list("Set", ctx.expr)
        if ctx.COLONEQUAL() is not None:
            return self.make_head_list("SetDelayed", ctx.expr)
        if ctx.CARETEQUAL() is not None:
            return self.make_head_list("UpSet", ctx.expr)
        if ctx.CARETCOLONEQUAL() is not None:
            return self.make_head_list("UpSetDelayed", ctx.expr)

        # if(ctx.FUNCTIONARROW() != null)
        val = "Function[{"
        val += self.get_full_form(ctx.expr(0))
        val += "},"
        val += self.get_full_form(ctx.expr(1))
        val += "]"

        return val

    # Visit a parse tree produced by InputFormParser#Xor.
    def visitXor(self, ctx):
        if ctx.XOR() is not None:
            return self.make_head_list("Xor", ctx.expr)
        return self.make_head_list("Xnor", ctx.expr)

    # Visit a parse tree produced by InputFormParser#Composition.
    def visitComposition(self, ctx):
        return self.make_head_list("Composition", ctx.expr)

    # Visit a parse tree produced by InputFormParser#Out.
    def visitOut(self, ctx):
        return self.get_full_form(ctx.outExpression())

    # Visit a parse tree produced by InputFormParser#Integrate.
    def visitIntegrate(self, ctx):
        return self.make_head_list("Integrate", ctx.expr)

    # Visit a parse tree produced by InputFormParser#Accessor.
    def visitAccessor(self, ctx):
        return self.make_head("Part", ctx.expr(), ctx.accessExpression())

    # Visit a parse tree produced by InputFormParser#HeadExpression.
    def visitHeadExpression(self, ctx):
        return self.make_head(self.get_full_form(ctx.expr()), ctx.expressionList())

    # Visit a parse tree produced by InputFormParser#Therefore.
    def visitTherefore(self, ctx):
        return self.make_head_list("Therefore", ctx.expr)

    # Visit a parse tree produced by InputFormParser#Square.
    def visitSquare(self, ctx):
        return self.make_head("Square", ctx.expr())

    # Visit a parse tree produced by InputFormParser#Put.
    def visitPut(self, ctx):
        if ctx.DOUBLEGREATER() is not None:
            return self.make_head("Put", ctx.expr(), ctx.StringLiteral())
        return self.make_head("PutAppend", ctx.expr(), ctx.StringLiteral())

    # Visit a parse tree produced by InputFormParser#PlusOp.
    def visitPlusOp(self, ctx):
        if ctx.BINARYPLUS() is not None:
            return self.make_head_list("Plus", ctx.expr)
        if ctx.BINARYMINUS() is not None:
            val = "Plus["
            exprList = self.get_children(ctx.expr)
            val += self.get_full_form(exprList[0])
            for e in exprList[1:]:
                val += ",Times[-1,"
                val += self.get_full_form(e)
                val += "]"
            val += "]"
            return val

        if ctx.BINARYPLUSMINUS() is not None:
            return self.make_head_list("PlusMinus", ctx.expr)

        # if ctx.BINARYMINUSPLUS() is not None:
        return self.make_head_list("MinusPlus", ctx.expr)

    # Visit a parse tree produced by InputFormParser#Power.
    def visitPower(self, ctx):
        return self.make_head_list("Power", ctx.expr)

    # Visit a parse tree produced by InputFormParser#VerticalSeparator.
    def visitVerticalSeparator(self, ctx):
        return self.make_head_list("VerticalSeparator", ctx.expr)

    # Visit a parse tree produced by InputFormParser#Union.
    def visitUnion(self, ctx):
        return self.make_head_list("Union", ctx.expr)

    # Visit a parse tree produced by InputFormParser#PreIncrement.
    def visitPreIncrement(self, ctx):
        if ctx.DOUBLEMINUS() is None:
            return self.make_head("PreIncrement", ctx.expr())
        return self.make_head("PreDecrement", ctx.expr())

    # Visit a parse tree produced by InputFormParser#Prefix.
    def visitPrefix(self, ctx):
        return self.make_head(self.get_full_form(ctx.expr(0)), ctx.expr(1))

    # Visit a parse tree produced by InputFormParser#Floor.
    def visitFloor(self, ctx):
        return self.make_head("Floor", ctx.expr())

    # Visit a parse tree produced by InputFormParser#Because.
    def visitBecause(self, ctx):
        return self.make_head_list("Because", ctx.expr)

    # Visit a parse tree produced by InputFormParser#BracketingBar.
    def visitBracketingBar(self, ctx):
        return self.make_head("BracketingBar", ctx.expressionList())

    # Visit a parse tree produced by InputFormParser#RightTee.
    def visitRightTee(self, ctx):
        if ctx.RIGHTTEE() is not None:
            return self.make_head_list("RightTee", ctx.expr)
        return self.make_head_list("DoubleRightTee", ctx.expr)

    # Visit a parse tree produced by InputFormParser#Or.
    def visitOr(self, ctx):
        if ctx.NOR() is not None:
            return self.make_head_list("Nor", ctx.expr)
        return self.make_head_list("Or", ctx.expr)

    # Visit a parse tree produced by InputFormParser#Cup.
    def visitCup(self, ctx):
        return self.make_head_list("Cup", ctx.expr)

    # Visit a parse tree produced by InputFormParser#BoxParen.
    def visitBoxParen(self, ctx):
        return ctx.getText()

    # Visit a parse tree produced by InputFormParser#StringExpression.
    def visitStringExpression(self, ctx):
        return self.make_head_list("StringExpression", ctx.expr)

    # Visit a parse tree produced by InputFormParser#Postfix.
    def visitPostfix(self, ctx):
        val = self.get_full_form(ctx.expr(1))
        val += "["
        val += self.get_full_form(ctx.expr(0))
        val += "]"
        return val

    # Visit a parse tree produced by InputFormParser#And.
    def visitAnd(self, ctx):
        if ctx.NAND() != None:
            return self.make_head_list("Nand", ctx.expr)

        return self.make_head_list("And", ctx.expr)

    # Visit a parse tree produced by InputFormParser#Optional.
    def visitOptional(self, ctx):
        return self.make_head_list("Optional", ctx.expr)

    # Visit a parse tree produced by InputFormParser#PatternTest.
    def visitPatternTest(self, ctx):
        return self.make_head_list("PatternTest", ctx.expr)

    # Visit a parse tree produced by InputFormParser#RightComposition.
    def visitRightComposition(self, ctx):
        return self.make_head_list("RightComposition", ctx.expr())

    # Visit a parse tree produced by InputFormParser#NonCommutativeMultiply.
    def visitNonCommutativeMultiply(self, ctx):
        return self.make_head_list("NonCommutativeMultiply", ctx.expr)

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
            val += self.get_full_form(ctx.getChild(curChild))
            curChild += 2

        # Cursor now points to one past the first ";;".
        if (
            ctx.getChild(curChild) is not None
            and ctx.getChild(curChild).getText() != ";;"
        ):
            # The middle expr has not been omitted
            val += ","
            val += self.get_full_form(ctx.getChild(curChild))
            curChild += 1
        else:
            val += ",All"

        # Cursor now points to either the second ";;" or past the end of the expr.
        if (
            ctx.getChild(curChild) is not None
            and ctx.getChild(curChild).getText() == ";;"
        ):
            # There is a skip amount.
            val += ","
            val += self.get_full_form(ctx.getChild(curChild + 1))

        val += "]"
        return val

    # Visit a parse tree produced by InputFormParser#SpanA.
    def visitSpanA(self, ctx):
        return self.visitSpan(ctx)

    # Visit a parse tree produced by InputFormParser#SpanB.
    def visitSpanB(self, ctx):
        return self.visitSpan(ctx)

    # Visit a parse tree produced by InputFormParser#Parentheses.
    def visitParentheses(self, ctx):
        return self.get_full_form(ctx.expr())

    # Visit a parse tree produced by InputFormParser#Infix.
    def visitInfix(self, ctx):
        return self.make_head(self.get_full_form(ctx.expr(1)), ctx.expr(0), ctx.expr(2))

    # Visit a parse tree produced by InputFormParser#Factorial.
    def visitFactorial(self, ctx):
        if ctx.BANG() is None:
            return self.make_head("Factorial", ctx.expr())

        return self.make_head("Factorial2", ctx.expr())

    # Visit a parse tree produced by InputFormParser#SuchThat.
    def visitSuchThat(self, ctx):
        return self.make_head_list("SuchThat", ctx.expr)

    # Visit a parse tree produced by InputFormParser#DoubleBracketingBar.
    def visitDoubleBracketingBar(self, ctx):
        return self.make_head("DoubleBracketingBar", ctx.expressionList())

    # Visit a parse tree produced by InputFormParser#NumberLiteral.
    def visitNumber(self, ctx):
        """
        Frustratingly, number literals have no FullForm[] in Mathematica.
        Mathematica will automatically compute the value of a number
        literal. Since we do no computation in the parser, the only
        "correct" option for us is to reproduce the number form as-is.

        :param ctx: A NumberLiteral SyntaxTree node.
        :return: The text of the number literal as is.
        """

        return ctx.getText()

    # Visit a parse tree produced by InputFormParser#SetContainment.
    def visitSetContainment(self, ctx):
        if ctx.ELEMENT() is not None:
            return self.make_head_list("Element", ctx.expr)
        if ctx.NOTELEMENT() is not None:
            return self.make_head_list("NotElement", ctx.expr)
        if ctx.SUBSET() is not None:
            return self.make_head_list("Subset", ctx.expr)

        # if(ctx.SUPERSET() != null)
        return self.make_head_list("Superset", ctx.expr)

    # Visit a parse tree produced by InputFormParser#CircleDot.
    def visitCircleDot(self, ctx):
        return self.make_head_list("CircleDot", ctx.expr)

    # Visit a parse tree produced by InputFormParser#Del.
    def visitDel(self, ctx):
        return self.make_head("Del", ctx.expr())

    # Visit a parse tree produced by InputFormParser#Wedge.
    def visitWedge(self, ctx):
        return self.make_head_list("Wedge", ctx.expr)

    # Visit a parse tree produced by InputFormParser#Colon.
    def visitColon(self, ctx):
        return self.make_head_list("Colon", ctx.expr)

    # Visit a parse tree produced by InputFormParser#BoxConstructor.
    def visitBoxConstructor(self, ctx):
        return ctx.getText()

    # Visit a parse tree produced by InputFormParser#OpEquals.
    def visitOpEquals(self, ctx):
        if ctx.PLUSEQUAL() is not None:
            return self.make_head_list("AddTo", ctx.expr)
        if ctx.MINUSEQUAL() is not None:
            return self.make_head_list("SubtractFrom", ctx.expr)
        if ctx.ASTERISKEQUAL() is not None:
            return self.make_head_list("TimesBy", ctx.expr)

        # if(ctx.SLASHEQUAL() != null){
        return self.make_head_list("DivideBy", ctx.expr)

    # Visit a parse tree produced by InputFormParser#Cap.
    def visitCap(self, ctx):
        return self.make_head_list("Cap", ctx.expr)

    # Visit a parse tree produced by InputFormParser#Alternatives.
    def visitAlternatives(self, ctx):
        return self.make_head_list("Alternatives", ctx.expr)

    # Visit a parse tree produced by InputFormParser#AngleBracket.
    def visitAngleBracket(self, ctx):
        return self.make_head("AngleBracket", ctx.expressionList())

    # Visit a parse tree produced by InputFormParser#ReplaceAll.
    def visitReplaceAll(self, ctx):
        if ctx.SLASHDOT() is not None:
            return self.make_head_list("ReplaceAll", ctx.expr)
        return self.make_head_list("ReplaceRepeated", ctx.expr)

    # Visit a parse tree produced by InputFormParser#TagUnset.
    def visitTagUnset(self, ctx):
        return self.make_head("TagUnset", ctx.symbol(), ctx.expr())

    # Visit a parse tree produced by InputFormParser#Divide.
    def visitDivide(self, ctx):
        if ctx.DIVIDE() is not None:
            return self.make_head_list("Divide", ctx.expr)

        # Mathematica treats x/y as Times[x,Power[y,-1]].
        val = "Times["
        val += self.get_full_form(ctx.expr(0))
        val += ",Power["
        val += self.get_full_form(ctx.expr(1))
        val += ",-1]]"

        return val

    # Visit a parse tree produced by InputFormParser#Diamond.
    def visitDiamond(self, ctx):
        return self.make_head_list("Diamond", ctx.expr)

    # Visit a parse tree produced by InputFormParser#List.
    def visitList(self, ctx):
        return self.make_head("List", ctx.expressionList())

    # Visit a parse tree produced by InputFormParser#MapApply.
    def visitMapApply(self, ctx):
        # expr (MAP | MAPALL | DOUBLEAT | TRIPPLEAT) expr
        if ctx.MAP() is not None:
            return self.make_head_list("Map", ctx.expr)
        if ctx.MAPALL() is not None:
            return self.make_head_list("MapAll", ctx.expr)
        if ctx.DOUBLEAT() is not None:
            return self.make_head_list("Apply", ctx.expr)
        # if(ctx.TRIPPLEAT()!=null)
        # We can't use make_head because the third argument isn't a ParseTree.
        # Apply[expr1,expr2,{1}]
        val = "Apply["
        val += self.get_full_form(ctx.expr(0))
        val += ","
        val += self.get_full_form(ctx.expr(1))
        val += ",List[1]]"

        return val

    # Visit a parse tree produced by InputFormParser#CenterDot.
    def visitCenterDot(self, ctx):
        return self.make_head_list("CenterDot", ctx.expr)

    # Visit a parse tree produced by InputFormParser#Conjugate.
    def visitConjugate(self, ctx):
        if ctx.CONJUGATE() is not None:
            return self.make_head("Conjugate", ctx.expr())
        if ctx.TRANSPOSE() is not None:
            return self.make_head("Transpose", ctx.expr())

        # The other two are the same.
        # if(ctx.CONJUGATETRANSPOSE()!=null)
        # if(ctx.HERMITIANCONJUGATE()!=null)

        return self.make_head("ConjugateTranspose", ctx.expr())

    # Visit a parse tree produced by InputFormParser#StringLiteral.
    def visitStringLiteral(self, ctx):
        return ctx.getText()

    # Visit a parse tree produced by InputFormParser#Equivalent.
    def visitEquivalent(self, ctx):
        return self.make_head_list("Equivalent", ctx.expr)

    # Visit a parse tree produced by InputFormParser#Coproduct.
    def visitCoproduct(self, ctx):
        return self.make_head_list("Coproduct", ctx.expr)

    # Visit a parse tree produced by InputFormParser#Message.
    def visitMessage(self, ctx):
        # One string literal.
        if ctx.StringLiteral(1) is None:
            return self.make_head("MessageName", ctx.expr(), ctx.StringLiteral(0))
        # Two string literals.
        return self.make_head(
            "MessageName", ctx.expr(), ctx.StringLiteral(0), ctx.StringLiteral(1)
        )

    # Visit a parse tree produced by InputFormParser#SmallCircle.
    def visitSmallCircle(self, ctx):
        return self.make_head_list("SmallCircle", ctx.expr)

    # Visit a parse tree produced by InputFormParser#Function.
    def visitFunction(self, ctx):
        return self.make_head("Function", ctx.expr())

    # Visit a parse tree produced by InputFormParser#PatternExp.
    def visitPatternExp(self, ctx):
        # symb:expr
        return self.make_head("Pattern", ctx.symbol(), ctx.expr())

    # Visit a parse tree produced by InputFormParser#Times.
    def visitTimes(self, ctx):
        return self.make_head_list("Times", ctx.expr)

    # Visit a parse tree produced by InputFormParser#Rule.
    def visitRule(self, ctx):
        if ctx.MINUSGREATER() is not None or ctx.RARROW() is not None:
            return self.make_head_list("Rule", ctx.expr)
        return self.make_head_list("RuleDelayed", ctx.expr)

    # Visit a parse tree produced by InputFormParser#SymbolLiteral.
    def visitSymbolLiteral(self, ctx):
        """
        FullForm of a symbol is itself.

        :param ctx: SymbolLiteral
        :return: SymbolLiteral as a string.
        """
        return ctx.getText()

    # Visit a parse tree produced by InputFormParser#TagSet.
    def visitTagSet(self, ctx):
        if ctx.EQUAL() is not None:
            return self.make_head("TagSet", ctx.symbol(), ctx.expr(0), ctx.expr(1))
        # Must be TagSetDelated.
        return self.make_head("TagSetDelayed", ctx.symbol(), ctx.expr(0), ctx.expr(1))

    # Visit a parse tree produced by InputFormParser#Ceiling.
    def visitCeiling(self, ctx):
        return self.make_head("Ceiling", ctx.expr())

    # Visit a parse tree produced by InputFormParser#Not.
    def visitNot(self, ctx):
        return self.make_head("Not", ctx.expr())

    # Visit a parse tree produced by InputFormParser#Backslash.
    def visitBackslash(self, ctx):
        return self.make_head_list("Backslash", ctx.expr)

    # Visit a parse tree produced by InputFormParser#Dot.
    def visitDot(self, ctx):
        return self.make_head_list("Dot", ctx.expr)

    # Visit a parse tree produced by InputFormParser#UnaryPlusMinus.
    def visitUnaryPlusMinus(self, ctx):
        if ctx.MINUS() is not None:
            val = "Times[-1,"
            val += self.get_full_form(ctx.expr())
            val += "]"
            return val
        if ctx.PLUS() is not None:
            return self.make_head("Plus", ctx.expr())
        if ctx.PLUSMINUS() is not None:
            return self.make_head("PlusMinus", ctx.expr())

        return self.make_head("MinusPlus", ctx.expr())

    # Visit a parse tree produced by InputFormParser#CircleTimes.
    def visitCircleTimes(self, ctx):
        return self.make_head_list("CircleTimes", ctx.expr)

    # Visit a parse tree produced by InputFormParser#Same.
    def visitSame(self, ctx):
        if ctx.TRIPPLEEQUAL() is not None:
            return self.make_head_list("SameQ", ctx.expr)
        return self.make_head_list("UnsameQ", ctx.expr)

    # Visit a parse tree produced by InputFormParser#Star.
    def visitStar(self, ctx):
        return self.make_head_list("Star", ctx.expr)

    # Visit a parse tree produced by InputFormParser#Derivative.
    def visitDerivative(self, ctx):
        val = "Derivative["

        # We have to count the single quotes. The antlr4 python api
        # makes this awkward.
        count = 0
        while ctx.SINGLEQUOTE(count) is not None:
            count += 1
        val += str(count)

        val += "]["
        val += self.get_full_form(ctx.expr())
        val += "]"

        return val

    # Visit a parse tree produced by InputFormParser#Get.
    def visitGet(self, ctx):
        return self.make_head("Get", ctx.StringLiteral())

    # Visit a parse tree produced by InputFormParser#Repeated.
    def visitRepeated(self, ctx):
        if ctx.DOUBLEDOT() is not None:
            return self.make_head("Repeated", ctx.expr())
        return self.make_head("RepeatedNull", ctx.expr())

    # Visit a parse tree produced by InputFormParser#CircleMinus.
    def visitCircleMinus(self, ctx):
        return self.make_head_list("CircleMinus", ctx.expr)

    # Visit a parse tree produced by InputFormParser#ContextName.
    def visitContextName(self, ctx):
        return ctx.getText()

    # Visit a parse tree produced by InputFormParser#SimpleContext.
    def visitSimpleContext(self, ctx):
        return ctx.getText()

    # Visit a parse tree produced by InputFormParser#CompoundContext.
    def visitCompoundContext(self, ctx):
        return ctx.getText()

    # Visit a parse tree produced by InputFormParser#PatternBlanks.
    def visitPatternBlanks(self, ctx):
        val = ""
        if ctx.TRIPPLEBLANK() is not None:
            val += "BlankNullSequence["
            if ctx.expr() is not None:
                val += self.get_full_form(ctx.expr())
            val += "]"
        if ctx.DOUBLEBLANK() is not None:
            val += "BlankSequence["
            if ctx.expr() is not None:
                val += self.get_full_form(ctx.expr())
            val += "]"
        if ctx.BLANK() is not None:
            val += "Blank["
            if ctx.expr() is not None:
                val += self.get_full_form(ctx.expr())
            val += "]"

        # If there is a symbol, we wrap the whole expression in Pattern[]
        if ctx.symbol() is not None:
            wrap = "Pattern["
            wrap += self.get_full_form(ctx.symbol())
            wrap += ","
            val = wrap + val + "]"

        return val

    # Visit a parse tree produced by InputFormParser#PatternBlankDot.
    def visitPatternBlankDot(self, ctx):
        val = ""
        if ctx.symbol() is not None:
            val = "Optional[Pattern["
            val += self.get_full_form(ctx.symbol())
            val += ",Blank[]]]"
        else:
            val = "Optional[Blank[]]"

        return val

    # Visit a parse tree produced by InputFormParser#OutNumbered.
    def visitOutNumbered(self, ctx):
        val = "Out["
        val += ctx.getText()[1:]
        val += "]"
        return val

    # Visit a parse tree produced by InputFormParser#OutUnnumbered.
    def visitOutUnnumbered(self, ctx):
        textLen = len(ctx.getText())
        if textLen == 1:
            return "Out[]"
        return "Out[-" + str(textLen) + "]"

    # Visit a parse tree produced by InputFormParser#SlotDigits.
    def visitSlotDigits(self, ctx):
        val = "Slot["
        val += ctx.getText()[1:]
        val += "]"
        return val

    # Visit a parse tree produced by InputFormParser#SlotNamed.
    def visitSlotNamed(self, ctx):
        val = "Slot["
        val += ctx.getText()[1:]
        val += "]"
        return val

    # Visit a parse tree produced by InputFormParser#SlotSequenceDigits.
    def visitSlotSequenceDigits(self, ctx):
        val = "SlotSequence["
        val += ctx.getText()[2:]
        val += "]"
        return val

    # Visit a parse tree produced by InputFormParser#SlotSequence.
    def visitSlotSequence(self, ctx):
        return "SlotSequence[1]"

    # Visit a parse tree produced by InputFormParser#SlotUnnamed.
    def visitSlotUnnamed(self, ctx):
        return "Slot[1]"

    # Visit a parse tree produced by InputFormParser#ExpressionListed.
    def visitExpressionListed(self, ctx):
        # expressionList can be empty.
        if not hasattr(ctx, "children") or ctx.getChildCount() == 0:
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
                val += self.get_full_form(child)
                exprCounter += 1
                # //The next child is a comma (or end of list) which we skip.
                childCounter += 1
            else:
                # Must have been a comma indicating Null.
                val += "Null"
            childCounter += 1

        # If the comma is the last child, it needs to be followed by a Null, too.
        if not isinstance(
            ctx.getChild(ctx.getChildCount() - 1), InputFormParser.ExprContext
        ):
            val += ",Null"

        return val

    # Visit a parse tree produced by InputFormParser#AccessExpressionA.
    def visitAccessExpressionA(self, ctx):
        return self.get_full_form(ctx.expressionList())

    # Visit a parse tree produced by InputFormParser#AccessExpressionB.
    def visitAccessExpressionB(self, ctx):
        return self.get_full_form(ctx.expressionList())

    # Visit a parse tree produced by InputFormParser#box.
    def visitBox(self, ctx):
        return ctx.getText()


def input_form_to_full_form(
    input_form_str: str, parse_tree_fn, show_tree_fn=None
) -> str:
    """Convert Mathematica string `input_form_str` into Full-Form text"""
    global emitter

    # Reuse existing emitter.
    if not emitter:
        emitter = FullFormEmitter()

    # Parse the input.
    tree = parse_tree_fn(input_form_str, show_tree_fn=show_tree_fn)

    # Emit FullForm.
    return emitter.visit(tree)
