from antlr4.ParserRuleContext import ParserRuleContext
from antlr4 import TerminalNode, ParseTreeWalker, ParseTreeListener
class PrettyPrinter(ParseTreeListener):

    def __init__(self, rule_names):
        self.rule_names = rule_names
        self.builder = ""

    def visitTerminal(self, node: TerminalNode) -> None:
        if self.builder:
            self.builder += ' '

        self.builder += str(node)
        # builder.append(Utils.escapeWhitespace(Trees.getNodeText(node, ruleNames), false));

    def visitErrorNode(self, node) -> None:
        if self.builder:
            self.builder += ' '

        builder += str(node)
        # builder.append(Utils.escapeWhitespace(Trees.getNodeText(node, ruleNames), false));

    def enterEveryRule(self, ctx: ParserRuleContext) -> None:
        if self.builder:
            self.builder += ' '

        if ctx.getChildCount():
            self.builder += '('

        rule_index = ctx.getRuleIndex()
        if rule_index is not None and rule_index < len(self.rule_names):
            rule_name = self.rule_names[rule_index]
        else:
            rule_name = str(rule_index)

        self.builder += rule_name

    def exitEveryRule(self, ctx: ParserRuleContext) -> None:
        if ctx.getChildCount():
            self.builder += ')'

def pretty_print(tree, rule_names):
    walker = ParseTreeWalker()
    pretty_printer = PrettyPrinter(rule_names)
    walker.walk(pretty_printer, tree)
    print(pretty_printer.builder)
