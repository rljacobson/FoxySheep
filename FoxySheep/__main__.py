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
# Initializing with `None` is a simple way to force 1 origin.
out_results = [None]

eval_namespace = {
    "out_results": out_results,
    "missing_modules": [],
}


def add_imports(optional_imports=[]):
    for importname in ["decimal", "math"] + optional_imports:
        try:
            eval_namespace[importname] = importlib.import_module(importname)
        except ImportError:
            print(
                f"Error importing {importname}; translations using this module will fail."
            )
            eval_namespace["missing_modules"].append(importname)
    return


def Out(i: Optional[int] = None) -> Any:
    if i is None:
        i = -1
    if not len(out_results):
        raise RuntimeError("No prior input")
    return out_results[i]


def eval_one(
    in_str: str,
    parse_tree_fn: Callable,
    output_style_fn: Callable,
    session: bool,
    mode: str,
    show_tree_fn,
    debug=False,
) -> None:
    try:
        results = output_style_fn(in_str, parse_tree_fn, show_tree_fn, mode, debug)
    except:
        traceback.print_exc(5)
        return

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
    return


def REPL(
    parse_tree_fn: Callable,
    output_style_fn: Callable,
    session: bool,
    mode: str,
    show_tree_fn=None,
    debug=False,
) -> None:
    """
    Read Eval Print Loop (REPL) for Mathematica translations
    """
    print(
        "Enter a Mathematica expression. Enter either an empty line, Ctrl-C, or Ctrl-D to exit."
    )
    in_count = 1
    while True:
        try:
            user_in = input(f"In[{in_count}] := ")
        except (KeyboardInterrupt, EOFError):
            break
        else:
            in_count += 1
        if user_in == "":
            break

        eval_one(
            in_str=user_in,
            parse_tree_fn=parse_tree_fn,
            output_style_fn=output_style_fn,
            mode=mode,
            session=session,
            show_tree_fn=show_tree_fn,
            debug=debug,
        )
        pass
    return

def REPL_file(
    input,
    parse_tree_fn: Callable,
    output_style_fn: Callable,
    session: bool,
    mode: str,
    show_tree_fn=None,
    debug=False,
) -> None:
    """
    Read Eval Print Loop (REPL) for Mathematica translations
    """
    in_count = 0
    for lineno, line in enumerate(open(input, "r").readlines()):
        line = line.strip()
        print("%3d: %s" % (lineno + 1, line))
        if not line or line.startswith("(*"):
            continue
        in_count += 1
        eval_one(
            in_str=line,
            parse_tree_fn=parse_tree_fn,
            output_style_fn=output_style_fn,
            mode=mode,
            session=session,
            show_tree_fn=show_tree_fn,
            debug=debug,
        )
        pass
    return

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
    type=click.Choice(["inputform", "fullform"], case_sensitive=False),
    required=False,
)
@click.option(
    "-o",
    "--output-style",
    type=click.Choice(["python", "sympy", "numpy", "fullform"], case_sensitive=False),
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
@click.option("-f", "--file", help="file of Mathematica expressions",
              required=False,
              type=click.Path(
                  exists=True,
                  file_okay=True,
                  readable=True,
                  resolve_path=True,
              ))
@click.option("-e", "--expr", help="translate *expr*", required=False)
@click.version_option(version=__version__)
def main(
    repl: bool, tree, input_style, output_style, debug: bool, session: bool, file: click.File, expr: str
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
    mode = output_style.lower() if output_style else None
    optional_imports = []
    if output_style and mode in ("sympy", "numpy", "python"):
        if output_style != "python":
            optional_imports = [output_style]
        output_style_fn = input_form_to_python
        parse_tree_fn = parse_tree_from_string
        if session == None and not expr:
            session = True
            pass
        pass
    elif session:
        print("--session option is only valid for Python output. Option ignored.")
        session = False

    if file and expr:
        print("Use only one of --file or --expr; --expr ignored")
        expr = None
    if expr:
        if session:
            print("--session option is only valid in a REPL. Option ignored.")
        print(
            output_style_fn(
                expr, parse_tree_fn, mode=mode, show_tree_fn=show_tree_fn, debug=debug
            )
        )
    elif file:
        add_imports(optional_imports)
        REPL_file(
            file,
            parse_tree_fn,
            output_style_fn,
            session,
            mode=mode,
            show_tree_fn=show_tree_fn,
            debug=debug,
        )
    elif repl:
        add_imports(optional_imports)
        REPL(
            parse_tree_fn,
            output_style_fn,
            session,
            mode=mode,
            show_tree_fn=show_tree_fn,
            debug=debug,
        )
    else:
        print("Something went wrong")


if __name__ == "__main__":
    main()
