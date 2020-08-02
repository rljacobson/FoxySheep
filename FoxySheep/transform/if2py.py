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
    "TimesContext": ast.Mult,
    "PowerContext": ast.Pow,
    "NonCommutativeMultiplyContext": ast.Mult,  # Not quite right: doesn't capture non-commutativenewss
    "PlusOpContext": ast.Add,
}

fn_translate = {
    "Range": "range",
    "List": "list",
    "GCD": "math.gcd",
    "Sin": "math.sin",
    "Plot": "matplotlib.pyplot.plot",
}

symbol_translate = {
    "E": "math.e",
}

def ast_constant(value, lineno=0, col_offset=0, kind=None):
    node = ast.Constant()
    node.lineno = 0
    node.col_offset = 0
    node.value = value
    node.kind = None
    return node

class InputForm2PyAst(InputFormVisitor):

    def adjust_subscript_index(self, ctx) -> ast.AST:
        node = ast.BinOp()
        child0 =  ctx.getChild(0)
        if child0.getText()[0] == "-":
            node.op = ast.Add()
        else:
            node.op = ast.Sub()
            node.left = self.visit(ctx)
            node.right = ast_constant(1)

        return node

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
        fn_name = fn_translate.get(fn_name, fn_name)
        fn_name_node = ast.Name(id=fn_name, ctx="Load()")
        args = []
        for arg in ctx.expressionList().getChildren():
            if arg.getText() == ",":
                continue
            args.append(self.visit(arg))
        return ast.Call(func=fn_name_node, args=args, keywords=[])

        # return self.make_head(self.get_full_form(ctx.expr()), ctx.expressionList())
        return None

    def visitList(self, ctx: ParserRuleContext) -> ast.AST:
        node = ast.List(ctx=ast.Load())
        expr_list = []
        for expr in ctx.expressionList().getChildren():
            if str(expr)== ",":
                continue
            expr_list.append(self.visit(expr))
        node.elts = expr_list
        return node

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
                raise RuntimeError("Can't handle NumberBaseTen with numberLiteralPrecision yet")
            mantissa_node = get_digits_constant(ctx.getChild(0))
            child1 = ctx.getChild(1)
            if child1.getText() == "`":
                # Machine-specific precision. Ignore it
                return mantissa_node
            node = ast.BinOp()
            node.op = ast.Mult()
            node.left = mantissa_node
            node.right = self.visit(child1)
            return node

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
            lit_exp_node = ast.BinOp()
            lit_exp_node.left = ast_constant(10)
            lit_exp_node.op = ast.Pow()
            lit_exp_node.right = number_node
            return lit_exp_node

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
        node = ast.BinOp()
        if ctx.BINARYMINUS():
            node.op = ast.Sub()
        elif ctx.BINARYPLUS():
            node.op = ast.Add()
        elif ctx.BINARYMINUSPLUS() or ctx.BINARYPLUSMINUS():
            raise RuntimeError("Can't handle +- or -+")
        else:
            raise RuntimeError(f"Unknown op context {ctx}")

        node.left = self.visit(ctx.expr(0))
        node.right = self.visit(ctx.expr(1))
        return node

    def visitPower(self, ctx: ParserRuleContext) -> ast.AST:
        """
        Translates infix binary operators. Function binary operators are different.
        """
        node = ast.BinOp()
        ctx_name = type(ctx).__name__
        ast_op_fn = IF_name_to_pyop.get(ctx_name, None)
        if ast_op_fn:
            node.op = ast_op_fn()
        else:
            raise RuntimeError(f"Unknown op context {type(ctx_name)}")

        node.left = self.visit(ctx.expr(0))
        node.right = self.visit(ctx.expr(1))
        return node

    visitMinusOp = (
        visitDivide
    ) = visitNonCommutativeMultiply = visitPower

    def visitSpanA(self, ctx: ParserRuleContext) -> ast.AST:
        node = ast.Slice()
        child0 = ctx.getChild(0)
        numeric_literal = self.get_numeric_literal(child0)
        if numeric_literal:
            numeric_literal.value -= 1
            node.lower = numeric_literal
        else:
            node.lower = self.adjust_subscript_index(child0)
        child2 = ctx.getChild(2)
        numeric_literal = self.get_numeric_literal(child2)
        if numeric_literal:
            numeric_literal.value -= 1
            node.upper = numeric_literal
        else:
            node.upper = self.adjust_subscript_index(child2)
        node.step = None
        return node

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
        node = ast.BinOp()
        ctx_name = type(ctx).__name__
        ast_op_fn = IF_name_to_pyop.get(ctx_name, None)
        if ast_op_fn:
            node.op = ast_op_fn()
        else:
            raise RuntimeError(f"Unknown op context {type(ctx_name)}")

        node.left = self.visit(ctx.expr(0))
        node.right = self.visit(ctx.expr(1))
        return node

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

def input_form_to_python_ast(tree) -> ast.AST:
    transform = InputForm2PyAst()
    return transform.visit(tree)


def input_form_to_python(input_form_str: str, parse_tree_fn, show_tree_fn=None, debug=False) -> str:

    tree = parse_tree_fn(input_form_str, show_tree_fn=show_tree_fn)
    pyast = input_form_to_python_ast(tree)
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
