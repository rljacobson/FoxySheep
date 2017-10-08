from antlr4 import *

from FoxySheep.generated.FoxySheepLexer import FoxySheepLexer
from FoxySheep.generated.FoxySheepParser import FoxySheepParser
from FoxySheep.FullFormEmitter import FullFormEmitter
from FoxySheep.PostParser import PostParser


def postParse(intree):
    """Post process the parse tree (flattens flat operators)."""
    tree = intree
    walker = ParseTreeWalker()
    postParser = PostParser()
    walker.walk(postParser, tree)
    # The PostParser can restructure the tree in a way that changes the root.
    if tree.parentCtx is not None:
        tree = tree.parentCtx
    return tree


def parseString(input:str, postprocees=True):

    # Boilerplate
    lexer = FoxySheepLexer(InputStream(input))
    stream = CommonTokenStream(lexer)
    parser = FoxySheepParser(stream)

    # global parser
    # if not parser:
    #     # Boilerplate
    #     lexer = FoxySheepLexer(InputStream(input))
    #     stream = CommonTokenStream(lexer)
    #     parser = FoxySheepParser(stream)
    # else:
    #     # Don't create a new parser. Just reset the input stream.
    #     parser.setInputStream(InputStream(input))
    tree = parser.prog()
    if postprocees:
        tree = postParse(tree)
    return tree


def getFullForm(input:str):
    # Parse the input.
    tree = parseString(input)

    # Emit FullForm.
    emitter = FullFormEmitter()
    return emitter.visit(tree)


def main():

    while True:
        instring = input('in:= ')
        if instring == '':
            break
        print(getFullForm(instring))


if __name__ == '__main__':
    main()