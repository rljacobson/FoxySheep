# Generated from FullForm.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .FullFormParser import FullFormParser
else:
    from FullFormParser import FullFormParser

# This class defines a complete generic visitor for a parse tree produced by FullFormParser.

class FullFormVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by FullFormParser#prog.
    def visitProg(self, ctx:FullFormParser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FullFormParser#Number.
    def visitNumber(self, ctx:FullFormParser.NumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FullFormParser#StringLiteral.
    def visitStringLiteral(self, ctx:FullFormParser.StringLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FullFormParser#SymbolLiteral.
    def visitSymbolLiteral(self, ctx:FullFormParser.SymbolLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FullFormParser#HeadExpression.
    def visitHeadExpression(self, ctx:FullFormParser.HeadExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FullFormParser#ExpressionListed.
    def visitExpressionListed(self, ctx:FullFormParser.ExpressionListedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FullFormParser#ContextName.
    def visitContextName(self, ctx:FullFormParser.ContextNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FullFormParser#SimpleContext.
    def visitSimpleContext(self, ctx:FullFormParser.SimpleContextContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FullFormParser#CompoundContext.
    def visitCompoundContext(self, ctx:FullFormParser.CompoundContextContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FullFormParser#NumberBaseN.
    def visitNumberBaseN(self, ctx:FullFormParser.NumberBaseNContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FullFormParser#NumberBaseTen.
    def visitNumberBaseTen(self, ctx:FullFormParser.NumberBaseTenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FullFormParser#numberLiteralPrecision.
    def visitNumberLiteralPrecision(self, ctx:FullFormParser.NumberLiteralPrecisionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FullFormParser#numberLiteralExponent.
    def visitNumberLiteralExponent(self, ctx:FullFormParser.NumberLiteralExponentContext):
        return self.visitChildren(ctx)



del FullFormParser