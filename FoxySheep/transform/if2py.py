import astor
from antlr4 import TerminalNode
from antlr4.ParserRuleContext import ParserRuleContext
from FoxySheep.generated.InputFormVisitor import InputFormVisitor
from FoxySheep.transform.if_transform import input_form_post
import ast

IF_name_to_pyop = {
    "DivideContext": ast.Div,
    "MinusOpContext": ast.Sub,
    "NonCommutativeMultiplyContext": ast.Mult,
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

    def visitProg(self, ctx: ParserRuleContext) -> ast.AST:
        return self.visit(ctx.expr(0))

    def visitNumberBaseTen(self, ctx: ParserRuleContext) -> ast.AST:
        digits = ctx.getText()
        if digits.find(".") >= 0:
            ast_top = ast.parse(f"Decimal({digits})")
            node = ast_top.body[0]
        else:
            node = ast.Constant()
            node.lineno = 0
            node.col_offset = 0
            node.value = int(ctx.getText(), 10)
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

    def visitPlusOp(self, ctx: ParserRuleContext) -> ast.AST:
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

    visitMinusOp = visitDivide = visitNonCommutativeMultiply = visitPlusOp


def input_form_to_python_ast(tree, show_tree_fn) -> ast.AST:
    transform = InputForm2PyAst()
    return transform.visit(tree)

def input_form_to_python(input_form_str: str, parse_tree_fn, show_tree_fn) -> str:

    tree = parse_tree_fn(input_form_str, show_tree_fn=show_tree_fn)
    pyast = input_form_to_python_ast(tree, show_tree_fn)
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
        tree = input_form_post(tree)
        return tree

    from FoxySheep.tree.pretty_printer import pretty_print_compact
    print(input_form_to_python("1", parse_tree_fn, pretty_print_compact))
