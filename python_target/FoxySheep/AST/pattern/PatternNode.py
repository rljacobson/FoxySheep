from AST import ASTNode, SymbolNode


class PatternNode(ASTNode):
    """
    `Pattern[identifier_, pattern_]`
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._add_named_children(['identifier', 'pattern'])
