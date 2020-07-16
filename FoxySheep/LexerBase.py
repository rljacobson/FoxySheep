# In order for the generated lexer to subclass our lexer base
# class, we have to add the lines
#       from generated.FoxySheepParser import FoxySheepParser
#       from FoxySheep.LexerBase import LexerBase
# to the generated lexer.

import sys

from antlr4 import Lexer
from FoxySheep.generated.InputFormParser import InputFormParser


class LexerBase(Lexer):
    def __init__(self, input_, output=sys.stdout):
        super(LexerBase, self).__init__(input_, output=output)
        self.bracketLevel = 0
        self.lastToken = None

    # Binary plus follows a complete expression. Complete
    # expressions always end with one of the following
    # tokens. On the other hand, unary plus never follows
    # these tokens. Distinguishing unary plus from binary
    # plus disambiguates the grammar and allows us to use
    # implicit multiplication.

    closeExprTokens = [
        InputFormParser.DecimalNumber,
        InputFormParser.NumberInBase,
        InputFormParser.Name,
        InputFormParser.StringLiteral,
        InputFormParser.RPAREN,
        InputFormParser.RBRACE,
        InputFormParser.HASH,
        InputFormParser.PERCENTDIGITS,
        InputFormParser.PERCENTS,
        InputFormParser.TRIPPLEBLANK,
        InputFormParser.DOUBLEBLANK,
        InputFormParser.BLANKDOT,
        InputFormParser.BLANK,
        InputFormParser.HASHDIGITS,
        InputFormParser.HASHStringLiteral,
        InputFormParser.DOUBLEHASHDIGITS,
        InputFormParser.HASH,
        InputFormParser.DOUBLEHASH,
        InputFormParser.DIGITS,
        InputFormParser.RBRACKET,
        InputFormParser.RBARBRACKET,
        InputFormParser.BoxRightBoxParenthesis,
        InputFormParser.DOUBLEPLUS,
        InputFormParser.DOUBLEMINUS,
        InputFormParser.BANG,
        InputFormParser.DOUBLEBANG,
        InputFormParser.CONJUGATE,
        InputFormParser.TRANSPOSE,
        InputFormParser.CONJUGATETRANSPOSE,
        InputFormParser.HERMITIANCONJUGATE,
        InputFormParser.SINGLEQUOTE,
        InputFormParser.DOUBLESEMICOLON,
        InputFormParser.DOUBLEDOT,
        InputFormParser.TRIPPLEDOT,
        InputFormParser.AMP,
        InputFormParser.DOT,
        InputFormParser.SEMICOLON,
    ]

    # Curiously, the lexer does not allow us to inspect previous
    # tokens. Thus we need to keep track of the previous token
    # so that we can use it to disambiguate unary/binary plus.
    # I don't think getToken consumes a token, so I don't think we need to record lastToken here.
    # def getToken(self):
    #     lt = super(LexerBase, self)._token
    #     if lt.channel != self.HIDDEN:
    #         self.lastToken = lt
    #     return lt
    def nextToken(self):
        lt = super(LexerBase, self).nextToken()
        if lt.channel != self.HIDDEN:
            self.lastToken = lt
        return lt

    # The following checks to see if the previous token likely
    # ended an expr. If so, it returns true. We use this method
    # in an action on plus to disambiguate between unary plus
    # and binary plus.
    def precededByExpr(self):
        # Returns true if the previous token ended a complete expr.
        if self.lastToken is None:
            return False
        tokenType = self.lastToken.type

        return tokenType in self.closeExprTokens

    # To determine if a newline separates expressions, we keep
    # track of the bracketing level. Note that we treat all
    # bracket-like characters as the same.
    def incrementBracketLevel(self, i):
        self.bracketLevel += i

    # We need to differentiate between ";;" when it follows a complete
    # expression or not in order to solve a context sensitivity
    # problem in the parser. See the Span parser rules for details.
    def checkDoubleSemicolon(self):
        if not self.precededByExpr():
            self.type = InputFormParser.SPANSEMICOLONS
            # self.setType(InputFormParser.SPANSEMICOLONS)

    # We distinguish between unary plus and binary plus.
    def checkAdditiveOp(self, type):
        if self.precededByExpr():
            self.type = type
            # self.setType(type)

    # Note that FoxySheep treats newlines the same way Mathematica does:
    # Wolfram Language "treats the input that you give on successive
    # lines as belonging to the same expression whenever no complete
    # expression would be formed without doing this."
    #
    # The following checks to see if the current token (a newline)
    # separates two expressions using the following heuristic:
    # If the token follows a complete expression and all bracket-
    # like characters have been matched, then the token is an
    # expression separator, and we return true.
    def checkNewline(self):
        if not (self.precededByExpr() and self.bracketLevel == 0):
            self._channel = self.HIDDEN
            # self.setChannel(self.HIDDEN)
