from AST import ASTNode


class OptionalNode(ASTNode):
    """
    `Optional[pattern_, default_.]`
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._add_named_children(['pattern', 'default'])
