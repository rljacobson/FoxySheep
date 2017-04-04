# In order for the generated lexer to subclass our lexer base
# class, we have to add the lines
#       from generated.FoxySheepParser import FoxySheepParser
#       from FoxySheep.Lexer import Lexer
# to the generated lexer.

import antlr4
from generated.FoxySheepParser import FoxySheepParser

class Lexer(antlr4.Lexer):

    def __init__(self, input):
        super(Lexer, self).__init__(input)
        self.bracketLevel = 0
        self.lastToken = None
        
    # Binary plus follows a complete expression. Complete
    # expressions always end with one of the following
    # tokens. On the other hand, unary plus never follows
    # these tokens. Distinguishing unary plus from binary
    # plus disambiguates the grammar and allows us to use
    # implicit multiplication.
    
    closeExprTokens = [
        FoxySheepParser.DecimalNumber,
        FoxySheepParser.NumberInBase,
        FoxySheepParser.Name,
        FoxySheepParser.StringLiteral,
        FoxySheepParser.RPAREN,
        FoxySheepParser.RBRACE,
        FoxySheepParser.HASH,
        FoxySheepParser.PERCENTDIGITS,
        FoxySheepParser.PERCENTS,
        FoxySheepParser.TRIPPLEBLANK,
        FoxySheepParser.DOUBLEBLANK,
        FoxySheepParser.BLANKDOT,
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
        ]
    
    # Curiously, the lexer does not allow us to inspect previous
    # tokens. Thus we need to keep track of the previous token
    # so that we can use it to disambiguate unary/binary plus.
    def getToken(self):
        lt = super(Lexer, self).getToken()
    
        if lt.channel != self.HIDDEN:
            self.lastToken = lt
        return lt
    
    def nextToken(self):
        lt = super(Lexer, self).nextToken()
        if lt.channel != self.HIDDEN:
            self.lastToken = lt
        return lt
    
    # The following checks to see if the previous token likely
    # ended an expr. If so, it returns true. We use this method
    # in an action on plus to disambiguate between unary plus
    # and binary plus.
    def precededByExpr(self):
        #Returns true if the previous token ended a complete expr.
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
            self.setType(FoxySheepParser.SPANSEMICOLONS)

    # We distinguish between unary plus and binary plus.
    def checkAdditiveOp(self, type):
        if self.precededByExpr():
            self.setType(type)

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
            self.setChannel(self.HIDDEN)