from itertools import product
import astor
from antlr4 import TerminalNode
from antlr4.ParserRuleContext import ParserRuleContext
from FoxySheep.generated.InputFormVisitor import InputFormVisitor
import astpretty
import ast
from typing import List, Union

IF_name_to_pyop = {
    "DivideContext": ast.Div,
    "MinusOpContext": ast.Sub,
    "MinusContext": ast.Sub,
    "TimesContext": ast.Mult,
    "PowerContext": ast.Pow,
    "PlusContext": ast.Add,
    "NonCommutativeMultiplyContext": ast.Mult,  # Not quite right: doesn't capture non-commutativenewss
    "PlusOpContext": ast.Add,
}

# FIXME: DRY this
# left: Mathematica, right: Python
fn_translate_py = {
    "Cosh": "math.cosh",
    "Exp": "math.exp",
    "GCD": "math.gcd",
    "List": "list",
    "Log": "math.log",
    "Max": "max",
    "Min": "min",
    "Plot": "matplotlib.pyplot.plot",
    "Sqrt": "math.sqrt",
    "Tanh": "math.tanh",
}

# trigonometric, etc.
for arc, tri, h in product(
    ("", "Arc"), ("Sin", "Cos", "Tan", "Cot", "Sec", "Csc"), ("", "h")
):
    fm = arc + tri + h
    if arc:  # arc func
        fs = "a" + tri.lower() + h
    else:  # non-arc func
        fs = tri.lower() + h
    fn_translate_py.update({fm: "math." + fs})

# left: Mathematica, right: numpy
fn_translate_numpy = {
    "Cosh": "numpy.cosh",
    "Exp": "numpy.exp",
    "GCD": "numpy.gcd",
    "Log": "numpy.log",
    "Mod": "numpy.Mod",
    "Max": "numpy.Max",
    "Min": "numpy.Min",
    "Pochhammer": "numpy.rf",
    "Sqrt": "numpy.sqrt",
    "Tanh": "numpy.tanh",
}

# trigonometric, etc.
for arc, tri, h in product(
    ("", "Arc"), ("Sin", "Cos", "Tan", "Cot", "Sec", "Csc"), ("", "h")
):
    fm = arc + tri + h
    if arc:  # arc func
        fs = "a" + tri.lower() + h
    else:  # non-arc func
        fs = tri.lower() + h
    fn_translate_numpy.update({fm: "numpy." + fs})

# left: Mathematica, right: Sympy
fn_translate_sympy = {
    "Cosh": "sympy.cosh",
    "Exp": "sympy.exp",
    "GCD": "sympy.gcd",
    "Log": "sympy.log",
    "Mod": "sympy.Mod",
    "Max": "sympy.Max",
    "Min": "sympy.Min",
    "Pochhammer": "sympy.rf",
    "Sqrt": "sympy.sqrt",
    "Tanh": "sympy.tanh",
}

# trigonometric, e.t.c.
for arc, tri, h in product(
    ("", "Arc"), ("Sin", "Cos", "Tan", "Cot", "Sec", "Csc"), ("", "h")
):
    fm = arc + tri + h
    if arc:  # arc func
        fs = "a" + tri.lower() + h
    else:  # non-arc func
        fs = tri.lower() + h
    fn_translate_sympy.update({fm: "sympy." + fs})

fn_transform = {}

# left: Mathematica, right: Python
symbol_translate = {
    "E": "math.e",
    "Pi": "math.pi",
    "I": "1j",
}

add_sub_signum = [ast.Add, ast.Sub]


def ast_constant(value, lineno=0, col_offset=0, kind=None):
    node = ast.Constant()
    node.lineno = 0
    node.col_offset = 0
    node.value = value
    node.kind = None
    return node


class InputForm2PyAst(InputFormVisitor):
    def __init__(self, mode="python"):
        if mode == "python":
            self.fn_translate = fn_translate_py
        elif mode == "sympy":
            self.fn_translate = fn_translate_sympy
        elif mode == "numpy":
            self.fn_translate = fn_translate_numpy
        else:
            raise RuntimeError(f"mode should be python, numpy or sympy; got {mode}")

    def adjust_index(self, ctx, sig_num=0) -> ast.AST:
        """Adjust for origin 0 (Python) vs. origin 1 (Mathematica) indexing"""
        numeric_literal = self.get_numeric_literal(ctx)
        if numeric_literal:
            return self.adjust_ast_const(numeric_literal, sig_num)
        else:
            node = ast.BinOp()
            child0 = ctx.getChild(0)
            if child0.getText()[0] == "-":
                node.op = add_sub_signum[sig_num + 1 % 2]()
            else:
                node.op = add_sub_signum[sig_num]()
                node.left = self.visit(ctx)
                node.right = ast_constant(1)

        return node

    def adjust_ast_const(self, numeric_literal, sig_num=0) -> ast.AST:
        """Adjust for origin 0 (Python) vs. origin 1 (Mathematica) indexing"""
        if sig_num:
            numeric_literal.value += 1
        else:
            numeric_literal.value -= 1
        return numeric_literal

    def get_full_form(self, e) -> Union[str, ast.AST]:
        """
        Returns a Python AST for the ParseTree `e`
        """
        if isinstance(e, TerminalNode):
            return str(e)

        return self.visit(e)

    def get_child_list(self, efunction) -> ast.AST:
        """
        Convert antlr4's awkward function-call API to a list.

        We assume efunction is a function of an integer i. This awkward
        interface is from antlr4's Python API.
        """

        elist = []
        i = 0
        e = efunction(i)
        while e is not None:
            elist.append(e)
            i += 1
            e = efunction(i)
        return elist

    def range_transform(self, expr_list):
        children = []
        for child in expr_list.expressionList().getChildren():
            if child.getText() == ",":
                continue
            children.append(child)
        n = len(children)
        if n == 1:
            args = [ast_constant(1), self.adjust_index(children[0], 1)]
        elif n == 2:
            args = [self.visit(children[0]), self.adjust_index(children[1], 1)]
        elif n == 3:
            args = [
                self.visit(children[0]),
                self.adjust_index(children[1], 1),
                self.visit(children[2]),
            ]
        else:
            raise RuntimeError(f"range takes 1..3 paramenters, got {n}")

        range_name = ast.Name(id="range", ctx="Load()")
        list_name = ast.Name(id="list", ctx="Load()")
        return ast.Call(
            func=list_name,
            args=[ast.Call(func=range_name, args=args, keywords=[])],
            keywords=[],
        )

        # return self.make_head(self.get_full_form(ctx.expr()), ctx.expressionList())
        child0 = expr_list.getChild(0)
        if hasattr(child0, "numberLiteral") or hasattr(child0, "DecimalNumber"):
            return self.visit(child0)
        return None

    fn_transform["Range"] = range_transform

    def table_transform(self, expr_list):
        children = []
        for child in expr_list.expressionList().getChildren():
            if child.getText() == ",":
                continue
            children.append(child)
        n = len(children)
        assert n == 2, f"Expecting 2 args for Table; got {n}"

        node = ast.ListComp()
        node.elt = self.visit(children[0])
        ast_list = self.visit(children[1])
        name_elt = ast_list.elts[0]
        assert isinstance(
            name_elt, ast.Name
        ), "Expecting first argument of Table to be a name"
        if isinstance(ast_list.elts[1], ast.Constant):
            args = [ast_constant(1), self.adjust_ast_const(ast_list.elts[1], 1)]
            range_name = ast.Name(id="range", ctx=ast.Load())
            iter = ast.Call(func=range_name, args=args, keywords=[])
            comprehension = ast.comprehension(
                iter=iter,
                ifs=[],
                is_sync=0,
                target=ast.Name(id=name_elt.id, ctx=ast.Store()),
            )
            node.generators = [comprehension]
        else:
            raise RuntimeError(
                "Can't handle Table expression which doesn't have a range constant yet"
            )
        return node

    fn_transform["Table"] = table_transform

    def get_numeric_literal(self, expr_list):
        child0 = expr_list.getChild(0)
        if hasattr(child0, "numberLiteral") or hasattr(child0, "DecimalNumber"):
            return self.visit(child0)
        return None

    def visitProg(self, ctx: ParserRuleContext) -> ast.AST:
        exprs = ctx.expr()
        n = len(exprs)
        expr_list: List[ast.AST] = []
        if n > 0:
            if n == 1:
                return self.visit(exprs[0])
            else:
                expr_list = list(map(self.visit, exprs))
                pass
            pass
        elif n == 0 and ctx.expressionList:
            for expr in ctx.expressionList().getChildren():
                if str(expr) == ",":
                    continue
                expr_list.append(self.visit(expr))
            return ast.Tuple(expr_list, ast.Load())

        # FIXME: Figure out what to do here.
        return None

    # The rest of the visitXXX routines are in alphabetical order

    def visitAccessor(self, ctx: ParserRuleContext) -> ast.AST:
        node = ast.Subscript()
        node.ctx = ast.Load()
        node.value = self.visit(ctx.getChild(0))
        node.slice = self.visit(ctx.getChild(1))
        return node

    def visitAccessExpressionA(self, ctx: ParserRuleContext) -> ast.AST:
        expressionList = ctx.getChild(2)
        assert expressionList.getChildCount() == 1
        numeric_literal = self.get_numeric_literal(expressionList)
        if numeric_literal:
            numeric_literal.value -= 1
            node = ast.Index()
            value = numeric_literal
            node.value = value
        else:
            node = self.visit(expressionList.getChild(0))

        return node

    def visitHeadExpression(self, ctx: ParserRuleContext) -> ast.AST:
        "Translates function calls"
        fn_name = ctx.expr().getText()

        if fn_name in fn_transform:
            return fn_transform[fn_name](self, ctx)

        fn_name = self.fn_translate.get(fn_name, fn_name)
        fn_name_node = ast.Name(id=fn_name, ctx=ast.Load())
        args = []
        for arg in ctx.expressionList().getChildren():
            if arg.getText() == ",":
                continue
            args.append(self.visit(arg))
        return ast.Call(func=fn_name_node, args=args, keywords=[])

        # return self.make_head(self.get_full_form(ctx.expr()), ctx.expressionList())
        return None

    def visitList(self, ctx: ParserRuleContext) -> ast.AST:
        expr_list = []
        for expr in ctx.expressionList().getChildren():
            if str(expr) == ",":
                continue
            expr_list.append(self.visit(expr))
        return ast.List(elts=expr_list, ctx=ast.Load())

    def visitNumberBaseTen(self, ctx: ParserRuleContext) -> ast.AST:
        def get_digits_constant(ctx):
            digits = ctx.getText()
            if digits.find(".") >= 0:
                ast_top = ast.parse(f"decimal.Decimal({digits})")
                node = ast_top.body[0]
            else:
                if digits.endswith("`"):
                    # Python doesn't have machine-specific representation. So drop
                    # off the indicator.
                    digits = digits[:-1]
                node = ast_constant(int(digits, 10))
            return node

        child_count = ctx.getChildCount()
        if child_count == 1:
            return get_digits_constant(ctx)
        else:
            if child_count == 3:
                raise RuntimeError(
                    "Can't handle NumberBaseTen with numberLiteralPrecision yet"
                )
            mantissa_node = get_digits_constant(ctx.getChild(0))
            child1 = ctx.getChild(1)
            if child1.getText() == "`":
                # Machine-specific precision. Ignore it
                return mantissa_node
            node = ast.BinOp(
                op=ast.Mult(), left=mantissa_node, right=self.visit(child1)
            )

        return node

    def visitNumberBaseN(self, ctx: ParserRuleContext) -> ast.AST:
        digits = ctx.getChild(0).getText()
        base = ctx.getChild(1).getText()
        if base.startswith("^^"):
            ast_top = ast.parse(f"int({digits}, {base[2:]})")
            node = ast_top.body[0]
        else:
            node = ast_constant(int(ctx.getText(), 10))
        return node

    def visitNumberLiteralExponent(self, ctx: ParserRuleContext) -> ast.AST:
        last_child = ctx.getChild(ctx.getChildCount() - 1)
        number_node = ast_constant(int(last_child.getText(), 10))

        if ctx.getChild(0).getText() == "*^":
            # we have 10**last_child.
            return ast.BinOp(left=ast_constant(10), op=ast.Pow(), right=number_node)

        return number_node

    def visitOutNumbered(self, ctx: ParserRuleContext) -> ast.AST:
        fn_name_node = ast.Name(id="Out", ctx=ast.Load())
        number_str = str(ctx.getChild(0))
        assert number_str[0] == "%"
        args = [ast_constant(int(number_str[1:], 10))]
        return ast.Call(func=fn_name_node, args=args, keywords=[])

    def visitOutUnnumbered(self, ctx: ParserRuleContext) -> ast.AST:
        fn_name_node = ast.Name(id="Out", ctx=ast.Load())
        return ast.Call(func=fn_name_node, args=[], keywords=[])

    def visitParentheses(self, ctx: ParserRuleContext) -> ast.AST:
        return self.visit(ctx.getChild(1))

    def visitPlusOp(self, ctx: ParserRuleContext) -> ast.AST:
        """
        Translates infix binary operators. Function binary operators are different.
        """
        node = ast.BinOp(left=self.visit(ctx.expr(0)), right=self.visit(ctx.expr(1)))
        if ctx.BINARYMINUS():
            node.op = ast.Sub()
        elif ctx.BINARYPLUS():
            node.op = ast.Add()
        elif ctx.BINARYMINUSPLUS() or ctx.BINARYPLUSMINUS():
            raise RuntimeError("Can't handle +- or -+")
        else:
            raise RuntimeError(f"Unknown op context {ctx}")

        return node

    def visitPower(self, ctx: ParserRuleContext) -> ast.AST:
        """
        Translates infix binary operators. Function binary operators are different.
        """
        node = ast.BinOp(left=self.visit(ctx.expr(0)), right=self.visit(ctx.expr(1)))
        ctx_name = type(ctx).__name__
        ast_op_fn = IF_name_to_pyop.get(ctx_name, None)
        if ast_op_fn:
            node.op = ast_op_fn()
        else:
            raise RuntimeError(f"Unknown op context {type(ctx_name)}")

        return node

    visitMinusOp = visitDivide = visitNonCommutativeMultiply = visitPower

    def visitSpanA(self, ctx: ParserRuleContext) -> ast.AST:
        return ast.Slice(
            lower=self.adjust_index(ctx.getChild(0)),
            upper=self.adjust_index(ctx.getChild(2)),
            step=None,
        )

    def visitStringLiteral(self, ctx: ParserRuleContext) -> ast.AST:
        val = ctx.getText()
        # Strip quotes
        if val[0] == val[-1] and val[0] in ["'", '"']:
            val = val.strip(val[0])
        return ast_constant(val)

    def visitSymbolLiteral(self, ctx: ParserRuleContext) -> ast.AST:
        symbol_name = ctx.getText()
        symbol_name = symbol_translate.get(symbol_name, symbol_name)
        return ast.Name(symbol_name)

    def visitTimes(self, ctx: ParserRuleContext) -> ast.AST:
        """
        Translates infix multiplcation.
        """
        node = ast.BinOp(left=self.visit(ctx.expr(0)), right=self.visit(ctx.expr(1)))
        ctx_name = type(ctx).__name__
        ast_op_fn = IF_name_to_pyop.get(ctx_name, None)
        if ast_op_fn:
            node.op = ast_op_fn()
        else:
            raise RuntimeError(f"Unknown op context {type(ctx_name)}")

        return node

    def binop_transform(self, ctx: ParserRuleContext) -> ast.AST:
        expr_list = ctx.expressionList()
        ctx_name = ctx.expr().getText() + "Context"
        ast_op_fn = IF_name_to_pyop.get(ctx_name, None)
        if ast_op_fn:
            op = ast_op_fn()
        else:
            raise RuntimeError(f"Unknown op context {type(ctx_name)}")

        return ast.BinOp(left=self.visit(expr_list.expr(0)),
                         right=self.visit(expr_list.expr(1)),
                         op=op
                         )

    fn_transform["Plus"] = binop_transform
    fn_transform["Minus"] = binop_transform
    fn_transform["Power"] = binop_transform
    fn_transform["Times"] = binop_transform

    def visitUnaryPlusMinus(self, ctx: ParserRuleContext) -> ast.AST:
        """Translates prefix + and - operators. Note +- (plus or minus) and -+
        are different.
        """
        node = ast.UnaryOp()
        node.lineno = 0
        node.col_offset = 0

        if ctx.MINUS() is not None:
            node.op = ast.USub()
        elif ctx.PLUS() is not None:
            node.op = ast.UAdd()
        elif ctx.PLUSMINUS() or ctx.MINUSPLUS():
            # We don't handle these
            return self.visitChildren(ctx)
        node.operand = self.visit(ctx.expr())
        return node


def input_form_to_python_ast(tree, mode="python") -> ast.AST:
    transform = InputForm2PyAst(mode)
    return transform.visit(tree)


def input_form_to_python(
    input_form_str: str, parse_tree_fn, mode="python", show_tree_fn=None, debug=False
) -> str:

    tree = parse_tree_fn(input_form_str, show_tree_fn=show_tree_fn)
    pyast = input_form_to_python_ast(tree, mode)
    if debug:
        print(astpretty.pformat(pyast, show_offsets=False))
    return astor.to_source(pyast)


if __name__ == "__main__":

    def parse_tree_fn(expr: str, show_tree_fn):
        from FoxySheep.generated.InputFormLexer import InputFormLexer
        from FoxySheep.generated.InputFormParser import InputFormParser
        from antlr4 import InputStream, CommonTokenStream

        lexer = InputFormLexer(InputStream(expr))
        parser = InputFormParser(CommonTokenStream(lexer))
        tree = parser.prog()
        show_tree_fn(tree, parser.ruleNames)
        return tree

    from FoxySheep.tree.pretty_printer import pretty_print_compact

    print(input_form_to_python("1 + 2 - 3 + 4", parse_tree_fn, pretty_print_compact))
