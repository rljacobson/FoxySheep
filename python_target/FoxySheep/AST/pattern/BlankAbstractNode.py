from AST import ASTNode, SymbolNode


class BlankAbstractNode(ASTNode):
    """
    `BlankAbstractNode` is the superclass of Blank*Node, each of which has
    one optional child called `required_head`.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._add_named_children(['required_head'])
