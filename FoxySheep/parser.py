"""
Driver routines for lexers and parsers

ANTLR4 is used to generate lexers and parsers. Here we glue lexing and parsing together.

"""
from antlr4 import InputStream, CommonTokenStream
from FoxySheep.generated.InputFormLexer import InputFormLexer
from FoxySheep.generated.InputFormParser import InputFormParser
from FoxySheep.generated.FullFormLexer import FullFormLexer
from FoxySheep.generated.FullFormParser import FullFormParser
from FoxySheep.transform.if_transform import input_form_post
from FoxySheep.emitter.full_form import input_form_to_full_form
from FoxySheep.emitter.python import input_form_to_python

# Cache the utility objects.
parser = None
lexer = None
ff_parser = None
ff_lexer = None
emitter = None

# FIXME: post_process is needed to flatten out binary opeators when going from
# InputForm to FullForm. It must not be used when going to Python.
# Probably the post_processing should be done outside of this function,
# and put into something more OutputForm specific.
def parse_tree_from_string(input_form: str, show_tree_fn=None):

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
    if show_tree_fn:
        show_tree_fn(tree, parser.ruleNames)
    return tree


def parse_tree_from_string_pp(input_form: str, show_tree_fn=None):
    tree = parse_tree_from_string(input_form, show_tree_fn)
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


def if2ff(s: str, show_tree_fn=None, mode=None) -> str:
    return input_form_to_full_form(
        s, parse_tree_from_string_pp, mode=mode, show_tree_fn=show_tree_fn
    )


def if2python(s: str, mode="python", show_tree_fn=None, debug=False) -> str:
    return input_form_to_python(
        s, parse_tree_from_string, show_tree_fn, mode=mode, debug=debug
    )


if __name__ == "__main__":
    print(if2ff("x^2-3x+4"))
    print(if2python("x^2-3x+4"))
