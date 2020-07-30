from antlr4.ParserRuleContext import ParserRuleContext
from antlr4 import TerminalNode, ParseTreeWalker, ParseTreeListener
import sys

INDENTATION_SPACE = "  "
class PrettyPrinter(ParseTreeListener):
    def __init__(self, rule_names):
        self.rule_names = rule_names
        self.builder = ""
        self.indentation = 0
        self.kid_number = 0

    def visitTerminal(self, node: TerminalNode) -> None:
        if self.builder:
            if self.indentation:
                self.builder += "\n"

            self.builder += (INDENTATION_SPACE * self.indentation)

        s = str(node)
        if not s.isidentifier():
            s = repr(str(node))
        if self.kid_number:
            self.builder += f"{self.kid_number}. "
        self.kid_number += 1
        self.builder += s + "\n"
        # builder.append(Utils.escapeWhitespace(Trees.getNodeText(node, ruleNames), false));

    def visitErrorNode(self, node) -> None:
        if self.builder:
            if self.indentation:
                self.builder += "\n"
            self.builder += (INDENTATION_SPACE * self.indentation)

        self.builder += f"{self.kid_number}. "
        self.kid_number += 1
        self.builder += str(node)
        # builder.append(Utils.escapeWhitespace(Trees.getNodeText(node, ruleNames), false));

    def enterEveryRule(self, ctx: ParserRuleContext) -> None:
        if self.indentation:
            self.builder += "\n"

        self.builder += (INDENTATION_SPACE * self.indentation)
        self.indentation += 1

        child_count = ctx.getChildCount()
        if child_count and ctx.parentCtx and ctx.parentCtx.getChildCount() > 1:
            self.builder += f"{self.kid_number}. "

        rule_index = ctx.getRuleIndex()
        if rule_index is not None and rule_index < len(self.rule_names):
            rule_name = self.rule_names[rule_index]
        else:
            rule_name = str(rule_index)

        nt_name = ctx.__class__.__name__
        if nt_name.endswith("Context"):
            nt_name = nt_name[:-len("Context")]
        name = "<%s:%s> " % (rule_name, nt_name)
        self.kid_number += 1
        self.builder += name
        if child_count:
            self.builder += f"[{child_count}]"
            self.kid_number = 0

    def exitEveryRule(self, ctx: ParserRuleContext) -> None:
        if ctx.getChildCount():
            self.indentation -= 1

class PrettyPrinterCompact(ParseTreeListener):
    def __init__(self, rule_names):
        self.rule_names = rule_names
        self.builder = ""

    def visitTerminal(self, node: TerminalNode) -> None:
        if self.builder:
            self.builder += " "
        s = str(node)
        if not s.isidentifier():
            s = repr(str(node))
        self.builder += s
        # builder.append(Utils.escapeWhitespace(Trees.getNodeText(node, ruleNames), false));

    def visitErrorNode(self, node) -> None:
        if self.builder:
            self.builder += " "

        if hasattr(self, "kid_number"):
            self.builder += f"{self.kid_number}. "
        else:
            self.kid_number = 0
        self.kid_number += 1
        self.builder += str(node)
        # builder.append(Utils.escapeWhitespace(Trees.getNodeText(node, ruleNames), false));

    def enterEveryRule(self, ctx: ParserRuleContext) -> None:
        if self.builder:
            self.builder += " "

        child_count = ctx.getChildCount()
        if child_count:
            self.builder += "("

        rule_index = ctx.getRuleIndex()
        if rule_index is not None and rule_index < len(self.rule_names):
            rule_name = self.rule_names[rule_index]
        else:
            rule_name = str(rule_index)

        nt_name = ctx.__class__.__name__
        if nt_name.endswith("Context"):
            nt_name = nt_name[:-len("Context")]
        name = "<%s:%s> " % (rule_name, nt_name)

        self.builder += name

    def exitEveryRule(self, ctx: ParserRuleContext) -> None:
        if ctx.getChildCount():
            self.builder += ")"

def pretty_print_string(tree, rule_names, compact=False) -> str:
    walker = ParseTreeWalker()
    pp_fn = PrettyPrinterCompact if compact else PrettyPrinter
    pretty_printer = pp_fn(rule_names)
    walker.walk(pretty_printer, tree)
    return pretty_printer.builder

def pretty_print_string_compact(*args) -> None:
    pretty_print_string(*args, compact=True)

def pretty_print(*args, **kwargs) -> None:
    out = kwargs.get("out", sys.stdout)
    out.write(pretty_print_string(*args, **kwargs) + "\n")

def pretty_print_compact(*args, **kwargs) -> None:
    kwargs["compact"] = True
    pretty_print(*args, **kwargs)
