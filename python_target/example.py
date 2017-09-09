from antlr4 import *

from FoxySheep.FullFormEmitter import FullFormEmitter
from FoxySheep.generated.FoxySheepLexer import FoxySheepLexer
from FoxySheep.generated.FoxySheepParser import FoxySheepParser


def main():
    inputFile = "../unit_tests/ParseExpressions/NumberLiterals.m"

    #Boilerplate
    input = FileStream(inputFile)
    lexer = FoxySheepLexer(input)
    stream = CommonTokenStream(lexer)
    parser = FoxySheepParser(stream)

    tree = parser.prog()

    # Emit FullForm[]
    emitter = FullFormEmitter()
    print emitter.visit(tree)
 
if __name__ == '__main__':
    main()