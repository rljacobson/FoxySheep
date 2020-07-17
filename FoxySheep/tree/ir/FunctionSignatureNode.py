from AST import ASTNode
from FoxySheep.scoping.Symbol import Symbol


class FunctionSignatureNode(ASTNode):
    """
    An abstraction representing a function signature, including the symbol
    for the function name, the parameters and their types, and default values.
    """

    def __init__(self, symbol: Symbol = None, **kwargs):
        """

        :param symbol: A `Symbol` for the head (name) of the function.
        :param kwargs:
        """
        super().__init__(**kwargs)
        self.symbol = symbol
