import click
from antlr4 import ParseTreeWalker, InputStream, CommonTokenStream
from typing import Callable
from FoxySheep import InputFormLexer
from FoxySheep import InputFormParser
from FoxySheep import FullFormEmitter
from FoxySheep import PostParser
from FoxySheep.pretty_printer import pretty_print
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


def parse_tree_from_string(input: str, post_process=True, show_tree=False):

    # Boilerplate
    # lexer = InputFormLexer(InputStream(input))
    # stream = CommonTokenStream(lexer)
    # parser = InputFormParser(stream)

    global parser, lexer

    # Reuse any existing parser or lexer.
    if not lexer:
        lexer = InputFormLexer(InputStream(input))
    else:
        lexer.inputStream = InputStream(input)
    if not parser:
        parser = InputFormParser(CommonTokenStream(lexer))
    else:
        parser.setTokenStream(CommonTokenStream(lexer))

    # Parse!
    tree = parser.prog()
    if post_process:
        if show_tree:
            pretty_print(tree, parser.ruleNames)
        post_tree = postParse(tree)
        if post_tree != tree:
            pretty_print(post_tree, parser.ruleNames)
            tree = post_tree
    return tree


def ff_parse_tree_from_string(input: str, show_tree=False):
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
    tree = ff_parser.prog()
    if show_tree:
        pretty_print(tree, ff_parser.ruleNames)
    return tree


def FullForm_from_string(
    input: str, parse_tree_fn=parse_tree_from_string, show_tree=False
):
    """Convert Mathematica string `input` into Full-Form input"""
    global emitter

    # Reuse existing emitter.
    if not emitter:
        emitter = FullFormEmitter()

    # Parse the input.
    tree = parse_tree_fn(input, show_tree)

    # Emit FullForm.
    return emitter.visit(tree)


def FullForm_from_file(path: str, parse_tree_fn=parse_tree_from_string):
    """Convert Mathematica string `input` into Full-Form input"""
    return FullForm_from_string(open(path, "r").read(), parse_tree_fn)


def REPL(parse_tree_fn: Callable = parse_tree_from_string, show_tree=False):
    # Simple REPL
    print(
        "Enter a Mathematica expression. Enter either an empty line, Ctrl-C, or Ctrl-D to exit."
    )
    while True:
        try:
            user_in = input("in:= ")
        except (KeyboardInterrupt, EOFError):
            break
        if user_in == "":
            break

        print(FullForm_from_string(user_in, parse_tree_fn, show_tree))


@click.command()
@click.option(
    "--repl/--no-repl", default=True, required=False, type=bool, help="Go into REPL",
)
@click.option(
    "--ast/--no-ast",
    default=False,
    required=False,
    type=bool,
    help="show AST(s) created",
)
@click.option(
    "-i",
    "--input-style",
    type=click.Choice(["InputForm", "FullForm"], case_sensitive=False),
    required=False,
)
@click.option("-e", "--expr", help="translate *expr*", required=False)
@click.version_option(version=VERSION)
def main(repl: bool, ast: bool, input_style, expr: str):
    parse_tree_fn = (
        ff_parse_tree_from_string
        if input_style and input_style.lower() == "fullform"
        else parse_tree_from_string
    )
    if expr:
        print(FullForm_from_string(expr, parse_tree_fn, ast))
    elif repl:
        REPL(parse_tree_fn, ast)
    else:
        print("Something went wrong")


if __name__ == "__main__":
    main()
