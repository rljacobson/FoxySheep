from antlr4 import TerminalNode
from antlr4.ParserRuleContext import ParserRuleContext
from FoxySheep.generated.InputFormVisitor import InputFormVisitor
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


def input_form_to_pyast(tree) -> ast.AST:
    transform = InputForm2PyAst()
    return transform.visit(tree)


if __name__ == "__main__":
    from antlr4 import InputStream, CommonTokenStream
    from FoxySheep.generated.InputFormLexer import InputFormLexer
    from FoxySheep.generated.InputFormParser import InputFormParser

    lexer = InputFormLexer(InputStream("10**1"))
    parser = InputFormParser(CommonTokenStream(lexer))
    tree = parser.prog()
    from FoxySheep.tree.pretty_printer import pretty_print_compact

    pretty_print_compact(tree, parser.ruleNames)
    pyast = input_form_to_pyast(tree)
    import astor

    print(astor.dump(pyast))
    print(astor.to_source(pyast))
