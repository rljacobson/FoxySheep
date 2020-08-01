"""
A command line program to perform Mathematica translations.

When installed run `foxy-sheep --help` for options
"""
import click
import importlib
import sys
import traceback
from typing import Any, Callable, Optional
from FoxySheep.parser import (
    ff_parse_tree_from_string,
    parse_tree_from_string,
    parse_tree_from_string_pp,
)
from FoxySheep.emitter.python import input_form_to_python
from FoxySheep.emitter.full_form import input_form_to_full_form
from FoxySheep.tree.pretty_printer import pretty_print
from FoxySheep.version import VERSION as __version__


# TODO: we could put this in a class and then one could have many REPLs.
out_results = []

eval_namespace = {
    "out_results": out_results,
    "missing_modules": [],
}


def setup_session():
    for importname in ("decimal", "math", "matplotlib.pyplot"):
        try:
            eval_namespace[importname] = importlib.import_module(importname)
        except ImportError:
            print(
                f"Error importing {importname}; translations using this module will fail."
            )
            eval_namespace["missing_modules"].append(importname)


def Out(i: Optional[int] = None) -> Any:
    if i is None:
        i = -1
    if not len(out_results):
        raise RuntimeError("No prior input")
    return out_results[i]


def REPL(
    parse_tree_fn: Callable, output_style_fn, session, show_tree_fn=None, debug=False
) -> None:
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

        try:
            results = output_style_fn(user_in, parse_tree_fn, show_tree_fn, debug)
        except:
            traceback.print_exc(5)
            continue

        print(results)
        if session:
            try:
                x = eval(results, None, eval_namespace)
            except:
                print(sys.exc_info()[1])
            else:
                print(f"Out[{len(out_results)}]={x}")
                out_results.append(x)
                # from pprint import pprint
                # pprint(out_results)
                pass
            pass
        pass


@click.command()
@click.option(
    "--repl/--no-repl", default=True, required=False, type=bool, help="Go into REPL",
)
@click.option(
    "-t",
    "--tree",
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
@click.option(
    "-d",
    "--debug",
    default=False,
    flag_value="debug",
    required=False,
    help="Show extra debugging information",
)
@click.option(
    "-s",
    "--session/--no-session",
    default=None,
    required=False,
    help="In REPL, evaluate the translation and in REPL session",
)
@click.option("-e", "--expr", help="translate *expr*", required=False)
@click.version_option(version=__version__)
def main(
    repl: bool, tree, input_style, output_style, debug: bool, session: bool, expr: str
):
    parse_tree_fn = (
        ff_parse_tree_from_string
        if input_style and input_style.lower() == "fullform"
        else parse_tree_from_string_pp
    )

    if tree == "full":
        show_tree_fn = lambda tree, rule_names: pretty_print(
            tree, rule_names, compact=False
        )
    elif tree == "compact":
        show_tree_fn = lambda tree, rule_names: pretty_print(
            tree, rule_names, compact=True
        )
    else:
        show_tree_fn = None

    output_style_fn = input_form_to_full_form
    if output_style and output_style.lower() == "python":
        output_style_fn = input_form_to_python
        parse_tree_fn = parse_tree_from_string
        if session == None and not expr:
            session = True
            pass
        pass
    elif session:
        print("--session option is only valid for Python output. Option ignored.")
        session = False

    if expr:
        if session:
            print("--session option is only valid in a REPL. Option ignored.")
        print(output_style_fn(expr, parse_tree_fn, show_tree_fn, debug))
    elif repl:
        setup_session()
        REPL(parse_tree_fn, output_style_fn, session, show_tree_fn, debug)
    else:
        print("Something went wrong")


if __name__ == "__main__":
    main()
