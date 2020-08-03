#!/usr/bin/env python
"""Show off translating Simple Form to Full Form"""
import os
import os.path as osp
import inspect
from FoxySheep import input_form_to_full_form, input_form_to_python, parse_tree_from_string

# IMHO this should be built-into a Python library. Perhaps it is, and I'm just not
# aware of it.
def get_srcdir():
    return osp.normcase(
        osp.dirname(osp.abspath(inspect.currentframe().f_back.f_code.co_filename))
    )

expression_dir_path = osp.join(get_srcdir(), "pytest", "parse_expressions")
for mma_path in os.scandir(expression_dir_path):
    if not mma_path.name.endswith(".m"):
        continue
    print("=" * 30, mma_path.name)
    for mma_expression in open(mma_path, "r").readlines():
        print(mma_expression)
        if mma_expression.strip().startswith("(*"):
            continue
        print(input_form_to_full_form(mma_expression, parse_tree_from_string))
        print("python " + ('-' * 10))
        try:
            str = input_form_to_python(mma_expression, parse_tree_from_string, None, debug=False)
        except:
            print("Python conversion failed")
            pass
        else:
            print(str)

        print()
        print('-' * 10)
