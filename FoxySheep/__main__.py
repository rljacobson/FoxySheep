import click
from antlr4 import InputStream, CommonTokenStream
from typing import Callable
from FoxySheep.emitter.full_form import input_form_to_full_form
from FoxySheep.emitter.python import input_form_to_python
from FoxySheep.generated.InputFormLexer import InputFormLexer
from FoxySheep.generated.InputFormParser import InputFormParser
from FoxySheep.transform.if_transform import input_form_post
from FoxySheep.tree.pretty_printer import pretty_print
from FoxySheep.generated.FullFormLexer import FullFormLexer
from FoxySheep.generated.FullFormParser import FullFormParser
from FoxySheep.version import VERSION

# Cache the utility objects.
parser = None
lexer = None
ff_parser = None
ff_lexer = None
emitter = None


def parse_tree_from_string(input_form: str, post_process=True, show_tree_fn=None):

    # Boilerplate
    # lexer = InputFormLexer(InputStream(input))
    # stream = CommonTokenStream(lexer)
    # parser = InputFormParser(stream)

    global parser, lexer

    # Reuse any existing parser or lexer.
    if not lexer:
        lexer = InputFormLexer(InputStream(input_form))
    else:
        lexer.inputStream = InputStream(input_form)
    if not parser:
        parser = InputFormParser(CommonTokenStream(lexer))
    else:
        parser.setTokenStream(CommonTokenStream(lexer))

    # Parse!
    tree = parser.prog()
    if post_process:
        if show_tree_fn:
            show_tree_fn(tree, parser.ruleNames)
        post_tree = input_form_post(tree)
        if post_tree != tree:
            show_tree_fn(post_tree, parser.ruleNames)
            tree = post_tree
    return tree


def ff_parse_tree_from_string(input: str, post_process=True, show_tree_fn=False):
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
    if post_process:
        if show_tree_fn:
            show_tree_fn(tree, ff_parser.ruleNames)
        post_tree = input_form_post(tree)
        if post_tree != tree:
            show_tree_fn(post_tree, parser.ruleNames)
            tree = post_tree
    return tree


def REPL(parse_tree_fn: Callable, output_style_fn, show_tree_fn=None) -> None:
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

        print(output_style_fn(user_in, parse_tree_fn, show_tree_fn))


@click.command()
@click.option(
    "--repl/--no-repl", default=True, required=False, type=bool, help="Go into REPL",
)
@click.option(
    "-t", "--tree",
    type=click.Choice(["full", "compact"], case_sensitive=False),
    required=False,
    help="show parse tree(s) created",
)
@click.option(
    "-i",
    "--input-style",
    type=click.Choice(["InputForm", "FullForm"], case_sensitive=False),
    required=False,
)
@click.option(
    "-o",
    "--output-style",
    type=click.Choice(["Python", "FullForm"], case_sensitive=False),
    required=False,
)
@click.option("-e", "--expr", help="translate *expr*", required=False)
@click.version_option(version=VERSION)
def main(repl: bool, tree, input_style, output_style, expr: str):
    parse_tree_fn = (
        ff_parse_tree_from_string
        if input_style and input_style.lower() == "fullform"
        else parse_tree_from_string
    )

    if tree == "full":
        show_tree_fn = lambda tree, rule_names: pretty_print(tree, rule_names, compact=False)
    elif tree == "compact":
        show_tree_fn = lambda tree, rule_names: pretty_print(tree, rule_names, compact=True)
    else:
        show_tree_fn = None

    output_style_fn = input_form_to_full_form
    if output_style and output_style.lower() == "python":
        output_style_fn = input_form_to_python

    if expr:
        print(output_style_fn(expr, parse_tree_fn, show_tree_fn))
    elif repl:
        REPL(parse_tree_fn, output_style_fn, show_tree_fn)
    else:
        print("Something went wrong")


if __name__ == "__main__":
    main()
