# TARGET LANGUAGE DEPENDENT CODE.

# Binary plus follows a complete expression. Complete
# expressions always end with one of the following
# tokens. On the other hand, unary plus never follows
# these tokens. Distinguishing unary plus from binary
# plus disambiguates the grammar and allows us to use
# implicit multiplication.

closeExprTokens = [
    FoxySheepParser.NumberLiteral,
    FoxySheepParser.Name,
    FoxySheepParser.StringLiteral,
    FoxySheepParser.RPAREN,
    FoxySheepParser.RBRACE,
    FoxySheepParser.HASH,
    FoxySheepParser.PERCENT,
    FoxySheepParser.TRIPPLEBLANK,
    FoxySheepParser.DOUBLEBLANK,
    FoxySheepParser.BLANK,
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

# To determine if a newline separates expressions, we keep
# track of the bracketing level. Note that we treat all
# bracket-like characters as the same.
bracketLevel = 0

# Curiously, the lexer does not allow us to inspect previous
# tokens. Thus we need to keep track of the previous token
# so that we can use it to disambiguate unary/binary plus.
lastToken = None

def getToken():
    lt = super.getToken()

    if lt.getChannel() != HIDDEN:
        lastToken = lt
    return lt

def nextToken():
    lt = super.nextToken()
    if lt.getChannel() != HIDDEN:
        lastToken = lt
    return lt

# The following checks to see if the previous token likely
# ended an expr. If so, it returns true. We use this method
# in an action on plus to disambiguate between unary plus
# and binary plus.
def precededByExpr():
    #Returns true if the previous token ended a complete expr.
    if lastToken is None:
        return False
    tokenType = lastToken.getType()

    return tokenType in closeExprTokens

# The following checks to see if the current token (a newline)
# separates two expressions using the following heuristic:
# If the token follows a complete expression and all bracket-
# like characters have been matched, then the token is an
# expression separator, and we return true.
def expressionSeparator():
    return precededByExpr() and bracketLevel == 0