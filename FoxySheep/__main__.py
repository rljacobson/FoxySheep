import click
from antlr4 import ParseTreeWalker, InputStream, CommonTokenStream

from FoxySheep import FoxySheepLexer
from FoxySheep import FoxySheepParser
from FoxySheep import FullFormEmitter
from FoxySheep import PostParser
from FoxySheep import FullFormLexer
from FoxySheep import FullFormParser
from FoxySheep.version import VERSION

# Cache the utility objects.
parser = None
lexer = None
ff_parser = None
ff_lexer = None
emitter = None


def postParse(tree):
    """Post process the parse tree. In particular, flatten some flat
    operators. Some operators appear in the source text without any
    explicit associativity, such as `Plus`, and are parsed into arbitrary
    tree structures.
    """

    walker = ParseTreeWalker()
    post_parser = PostParser()
    walker.walk(post_parser, tree)

    # The PostParser can restructure the tree in a way that changes the root.
    if tree.parentCtx is not None:
        tree = tree.parentCtx
    return tree


def parse_tree_from_string(input: str, post_process=True):

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
    if post_process:
        tree = postParse(tree)
    return tree


def ff_parse_tree_from_string(input: str):
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


def FullForm_from_string(input: str):
    """Convert Mathematica string `input` into Full-Form input"""
    global emitter

    # Reuse existing emitter.
    if not emitter:
        emitter = FullFormEmitter()

    # Parse the input.
    tree = parse_tree_from_string(input)

    # Emit FullForm.
    return emitter.visit(tree)

def FullForm_from_file(path: str):
    """Convert Mathematica string `input` into Full-Form input"""
    return FullForm_from_string(open(path, "r").read())


def REPL():
    # Simple REPL
    print("Enter a Mathematica expression. Enter either an empty line or Ctrl-C to exit.")
    while True:
        try:
            user_in = input("in:= ")
        except KeyboardInterrupt:
            break
        if user_in == "":
            break

        print(FullForm_from_string(user_in))

@click.command()
@click.option(
    "--repl/--no-repl",
    default=True,
    required=False,
    type=bool,
    help="Go into REPL")
@click.option("-e", "--expr",
              help="translate *expr*", required=False)
@click.version_option(version=VERSION)
def main(repl: bool, expr: str):
    if expr:
        print(FullForm_from_string(expr))
    elif repl:
        REPL()
    else:
        print("Something went wrong")

if __name__ == "__main__":
    main()
