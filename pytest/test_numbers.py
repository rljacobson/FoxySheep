from FoxySheep.generated.InputFormLexer import InputFormLexer
from antlr4 import InputStream, CommonTokenStream
from FoxySheep.generated.InputFormParser import InputFormParser

from FoxySheep.tree.pretty_printer import pretty_print_string
from FoxySheep.emitter.full_form import input_form_to_full_form

last_tree_str = ""


def test_numbers():
    def parse_tree_fn(expr: str, show_tree_fn):
        global last_tree_str
        lexer = InputFormLexer(InputStream(expr))
        parser = InputFormParser(CommonTokenStream(lexer))
        tree = parser.prog()
        last_tree_str = show_tree_fn(tree, parser.ruleNames)
        # tree = postParse(tree)
        return tree

    pp_fn = lambda tree, rule_names: pretty_print_string(tree, rule_names, compact=True)
    for expr, expect_tree_str, expect_full_form in (
        (
            "1 ** 10",
            "(prog (expr (expr (numberLiteral '1')) '**' (expr (numberLiteral '10'))))",
            "NonCommutativeMultiply[1,10]",
        ),
    ):
        s = input_form_to_full_form(expr, parse_tree_fn, pp_fn)
        # print(s)
        # print("-" * 30)
        # print(last_tree_str)
        # print("=" * 30)
        assert expect_full_form == input_form_to_full_form(expr, parse_tree_fn, pp_fn)
        assert last_tree_str == expect_tree_str
