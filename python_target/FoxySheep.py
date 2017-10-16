from antlr4 import *

from FoxySheep.generated.FoxySheepLexer import FoxySheepLexer
from FoxySheep.generated.FoxySheepParser import FoxySheepParser
from FoxySheep.FullFormEmitter import FullFormEmitter
from FoxySheep.PostParser import PostParser
from FoxySheep.generated.FullFormLexer import FullFormLexer
from FoxySheep.generated.FullFormParser import FullFormParser

# Cache the utility objects.
parser = None
lexer = None
ff_parser = None
ff_lexer = None
emitter = None


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


def parse_tree_from_string(input:str, postprocess=True):

    # Boilerplate
    # lexer = FoxySheepLexer(InputStream(input))
    # stream = CommonTokenStream(lexer)
    # parser = FoxySheepParser(stream)

    global parser, lexer

    # Reuse any existing parser or lexer.
    if not lexer:
        lexer = FoxySheepLexer(InputStream(input))
    else:
        lexer.inputStream = InputStream(input)
    if not parser:
        parser = FoxySheepParser(CommonTokenStream(lexer))
    else:
        parser.setTokenStream(CommonTokenStream(lexer))

    # Parse!
    tree = parser.prog()
    if postprocess:
        tree = postParse(tree)
    return tree


def ff_parse_tree_from_string(input:str):
    global ff_parser, ff_lexer

    # Reuse any existing parser or lexer.
    if not ff_lexer:
        ff_lexer = FullFormLexer(InputStream(input))
    else:
        ff_lexer.InputStream = InputStream(input)
        ff_lexer.reset()
    if not ff_parser:
        stream = CommonTokenStream(ff_lexer)
        ff_parser = FullFormParser(stream)
    else:
        # Don't create a new parser. Just reset the input stream.
        ff_parser.setTokenStream(CommonTokenStream(ff_lexer))
        ff_parser.reset()

    # Parse!
    return ff_parser.prog()


def FullForm_from_string(input:str):
    global emitter

    # Reuse existing emitter.
    if not emitter:
        emitter = FullFormEmitter()

    # Parse the input.
    tree = parse_tree_from_string(input)

    # Emit FullForm.
    return emitter.visit(tree)


def main():
    #Simple REPL
    while True:
        try:
            user_in = input('in:= ')
        except KeyboardInterrupt:
            break
        if user_in == '':
            break

        print(FullForm_from_string(user_in))


if __name__ == '__main__':
    main()
