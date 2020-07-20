from FoxySheep.generated.InputFormLexer import InputFormLexer
from antlr4 import InputStream, CommonTokenStream
from FoxySheep.generated.InputFormParser import InputFormParser
from FoxySheep.transform.if_transform import input_form_post

from FoxySheep.tree.pretty_printer import pretty_print_string
from FoxySheep.emitter.full_form import input_form_to_full_form
from FoxySheep.transform.if2py import input_form_to_python

from typing import Callable
import yaml
import os.path as osp

def get_srcdir():
    filename = osp.normcase(osp.dirname(osp.abspath(__file__)))
    return osp.realpath(filename)


srcdir = get_srcdir()
testdata_dir = osp.join(srcdir, "parse_expressions")

last_tree_str = ""

def parse_tree_fn(expr: str, show_tree_fn):
    global last_tree_str
    lexer = InputFormLexer(InputStream(expr))
    parser = InputFormParser(CommonTokenStream(lexer))
    tree = parser.prog()
    last_tree_str = show_tree_fn(tree, parser.ruleNames)
    tree = input_form_post(tree)
    return tree

pp_fn = lambda tree, rule_names: pretty_print_string(tree, rule_names, compact=True)

show_tests=True

def do_test(input_base: str, translation_fn: Callable):
    testdata_path = osp.join(testdata_dir, "input2full.yaml")
    with open(testdata_path, "r") as yaml_file:
        test_data = yaml.load(yaml_file, Loader=yaml.FullLoader)
        # print(test_data)

    for section, test_list in test_data.items():
        print(f'{"*" * 10} {section} {"*" * 10}')
        for test_item in test_list:
            expr = str(test_item["InputForm"])
            tree_str_expect = test_item["tree"]
            full_form_expect = str(test_item.get("FullForm", expr))
            s = translation_fn(expr, parse_tree_fn, pp_fn)
            if show_tests:
                print(s)
                print(full_form_expect)
                print(last_tree_str)
                print("=" * 30)

            assert s == full_form_expect
            assert last_tree_str == tree_str_expect

def test_FullForm():
    do_test("input2full.yaml", input_form_to_full_form)

def test_numberLiteral2Py():

    for expr, tree_str_expect, output_expect in (
        ("1", "(prog (expr (numberLiteral '1')))", "(1)"),
        ("12", "(prog (expr (numberLiteral '12')))", "(12)"),
        ("167.5", "(prog (expr (numberLiteral '167.5')))", "Decimal(167.5)"),
        ("15^^8", "(prog (expr (numberLiteral '15' '^^8')))", "int(15, 8)"),
        # ("55*^2", "(prog (expr (numberLiteral '55' (numberLiteralExponent '*^' '2'))))"),
        # ("10^^3.58.3", "(expr (numberLiteral '55' '^^8.3')))"),
        # ("132`", "(prog (expr (numberLiteral '132' (numberLiteralPrecision '`'))))"),
        # (
        #     "167^^8``5",
        #     "(prog (expr (numberLiteral '167' '^^8' (numberLiteralPrecision '``' '5'))))",
        # ),
    ):
        s = input_form_to_python(expr, parse_tree_fn, pp_fn)
        # print(s)
        # print("-" * 30)
        # print(last_tree_str)
        # print("=" * 30)

        assert output_expect == s.strip()
        assert last_tree_str == tree_str_expect

def test_binOp2Py():

    for expr, tree_str_expect, full_form_expect in (
        (
            "1 ** 10",
            "(prog (expr (expr (numberLiteral '1')) '**' (expr (numberLiteral '10'))))",
            "(1 * 10)",
        ),
        (
            "(1 / 10) 3",
            "(prog (expr (expr '(' (expr (expr (numberLiteral '1')) '/' (expr (numberLiteral '10'))) ')') (expr (numberLiteral '3'))))",
            "(1 / 10 * 3)",
        ),
    ):
        s = input_form_to_python(expr, parse_tree_fn, pp_fn)
        # print(s)
        # print("-" * 30)
        # print(last_tree_str)
        # print("=" * 30)

        assert s.strip() == full_form_expect
        assert last_tree_str == tree_str_expect


if __name__ == "__main__":
    test_FullForm()
