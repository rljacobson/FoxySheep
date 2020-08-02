from FoxySheep.generated.InputFormLexer import InputFormLexer
from antlr4 import InputStream, CommonTokenStream
from FoxySheep.generated.InputFormParser import InputFormParser

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
    return tree


pp_fn = lambda tree, rule_names: pretty_print_string(tree, rule_names, compact=True)

show_tests = True


def do_test(input_base: str, translation_fn: Callable, test_attr: str):
    testdata_path = osp.join(testdata_dir, input_base)
    with open(testdata_path, "r") as yaml_file:
        test_data = yaml.load(yaml_file, Loader=yaml.FullLoader)
        # print(test_data)

    for section, test_list in test_data.items():
        print(f'{"*" * 10} {section} {"*" * 10}')
        for test_item in test_list:
            expr = str(test_item["InputForm"])
            tree_str_expect = test_item["tree"]
            full_form_expect = str(test_item.get(test_attr, expr))
            s = translation_fn(expr, parse_tree_fn, pp_fn)
            if show_tests:
                print(s)
                print(full_form_expect)
                print(last_tree_str)
                print("=" * 30)

            assert s.replace("\n", "").strip() == full_form_expect
            assert last_tree_str == tree_str_expect


def test_FullForm():
    do_test("input2full.yaml", input_form_to_full_form, "FullForm")


def test_python():
    do_test("input2py.yaml", input_form_to_python, "python")


def test_fast_intro_for_math():
    do_test("fi4mspy.yaml", input_form_to_python, "python")


if __name__ == "__main__":
    # test_python()
    # test_FullForm()
    test_fast_intro_for_math()
