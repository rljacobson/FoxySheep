#!/usr/bin/env python
"""Show off translating Simple Form to Full Form"""
import os
import os.path as osp
import inspect
from FoxySheep import input_form_to_full_form, parse_tree_from_string

# IMHO this should be built-into a Python library. Perhaps it is, and I'm just not
# aware of it.
def get_srcdir():
    return osp.normcase(
        osp.dirname(osp.abspath(inspect.currentframe().f_back.f_code.co_filename))
    )

expression_dir_path = osp.join(get_srcdir(), "pytest", "parse_expressions")
for mma_path in os.scandir(expression_dir_path):
    print("=" * 30, mma_path.name)
    mma_expression = open(mma_path, "r").read()
    print(mma_expression)
    print('-' * 10)
    print(input_form_to_full_form(mma_expression, parse_tree_from_string))
    print()
