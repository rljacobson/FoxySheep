import astor
from antlr4 import TerminalNode
from antlr4.ParserRuleContext import ParserRuleContext
from FoxySheep.generated.InputFormVisitor import InputFormVisitor
from FoxySheep.transform.if_transform import input_form_post
import ast

IF_name_to_pyop = {
    "DivideContext": ast.Div,
    "MinusOpContext": ast.Sub,
    "TimesContext": ast.Mult,
    "PowerContext": ast.Pow,
    "NonCommutativeMultiplyContext": ast.Mult,  # Not quite right: doesn't capture non-commutativenewss
    "PlusOpContext": ast.Add,
}


class InputForm2PyAst(InputFormVisitor):
    def get_full_form(self, e) -> ast.AST:
        """
        Returns a Python AST for the ParseTree `e`
        """
        if isinstance(e, TerminalNode):
            return e.getText()

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

    def visitExpressionListed(self, ctx: ParserRuleContext) -> ast.AST:
        from trepan.api import debug; debug()
        return self.visitChildren(ctx)

    def visitProg(self, ctx: ParserRuleContext) -> ast.AST:
        exprs = ctx.expr()
        n = len(exprs)
        if n > 0:
            if n == 1:
                return self.visit(exprs[0])
            else:
                expr_list = map(self.visit, exprs)
                pass
            pass
        elif n == 0:
            expr_list = []
            for expr in ctx.expressionList().getChildren():
                if expr.getText() == ",":
                    continue
                expr_list.append(self.visit(expr))
        return ast.Tuple(expr_list, 5)

    def visitParentheses(self, ctx:ParserRuleContext) -> ast.AST:
        return self.visit(ctx.getChild(1))

    def visitNumberBaseTen(self, ctx: ParserRuleContext) -> ast.AST:
        digits = ctx.getText()
        if digits.find(".") >= 0:
            ast_top = ast.parse(f"Decimal({digits})")
            node = ast_top.body[0]
        else:
            if digits.endswith("`"):
                # Python doesn't have machine-specific representation. So drop
                # off the indicator.
                digits = digits[:-1]
            node = ast.Constant()
            node.lineno = 0
            node.col_offset = 0
            node.value = int(digits, 10)
        return node

    def visitNumberBaseN(self, ctx: ParserRuleContext) -> ast.AST:
        digits = ctx.getChild(0).getText()
        base = ctx.getChild(1).getText()
        if base.startswith("^^"):
            ast_top = ast.parse(f"int({digits}, {base[2:]})")
            node = ast_top.body[0]
        else:
            node = ast.Constant()
            node.lineno = 0
            node.col_offset = 0
            node.value = int(ctx.getText(), 10)
        return node

    def visitOutNumbered(self, ctx: ParserRuleContext) -> ast.AST:
        fn_name = ast.Name(id="Out", ctx="Load()")
        args = [ast.Constant(number)]
        return ast.Call(func=fn_name, args=args, keywords=[])

    def visitOutUnnumbered(self, ctx: ParserRuleContext) -> ast.AST:
        fn_name = ast.Name(id="Out", ctx="Load()")
        return ast.Call(func=fn_name, args=[], keywords=[])

    def visitPlusOp(self, ctx: ParserRuleContext) -> ast.AST:
        """
        Handles infix binary operators. Function binary operators are different.
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
    ) = visitNonCommutativeMultiply = visitTimes = visitPower = visitPlusOp


    def visitUnaryPlusMinus(self, ctx: ParserRuleContext) -> ast.AST:
        """Handles prefix + and - operators. Note +- (plus or minus) and -+
        are different.
        """
        node = ast.UnaryOp()
        node.lineno = 0
        node.col_offset = 0
        ctx_name = type(ctx).__name__

        if ctx.MINUS() is not None:
            node.op = ast.USub()
        elif ctx.PLUS() is not None:
            node.op = ast.UAdd()
        elif ctx.PLUSMINUS() or ctx.MINUSPLUS():
            # We don't handle these
            return self.visitChildren(ctx)
        node.operand = self.visit(ctx.expr())
        return node

    def visitSymbolLiteral(self, ctx:ParserRuleContext) -> ast.AST:
        return ast.Name(ctx.getText())


def input_form_to_python_ast(tree) -> ast.AST:
    transform = InputForm2PyAst()
    return transform.visit(tree)


def input_form_to_python(input_form_str: str, parse_tree_fn, show_tree_fn=None) -> str:

    tree = parse_tree_fn(input_form_str, show_tree_fn=show_tree_fn)
    pyast = input_form_to_python_ast(tree)
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

    print(input_form_to_python("1 + 2 + 3 + 4", parse_tree_fn, pretty_print_compact))
