"""
A command line program to perform Mathematica translations.

When installed run `foxy-sheep --help` for options
"""
import click
from typing import Callable
from FoxySheep.parser import ff_parse_tree_from_string, parse_tree_from_string
from FoxySheep.emitter.python import input_form_to_python
from FoxySheep.emitter.full_form import input_form_to_full_form
from FoxySheep.transform.if_transform import input_form_post
from FoxySheep.tree.pretty_printer import pretty_print
from FoxySheep.version import VERSION as __version__

def REPL(parse_tree_fn: Callable, output_style_fn, show_tree_fn=None) -> None:
    """
    Read Eval Print Loop (REPL) for Mathematica translations
    """
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
@click.version_option(version=__version__)
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
