"""

"""

from FoxySheep.tree.nodes import treeNode, SymbolNode

class FunctionCallNode(treeNode):
    """
    The base class of all tree node classes representing a function call.

    The symbol_node
    """

    def __init__(self, symbol_node: SymbolNode, **kwargs):
        super().__init__(**kwargs)

        self.FunctionType = None


class FunctionDeclarationNode(treeNode):
    """
    The base class of all tree node classes representing something that
    creates a DownValue. This node will represent the DownValue in the symbol
    table. The symbol_node is the Head of the declaration, that is, the name
    of the function being created. The symbol_node will point to a Symbol in
    the symbol table. The symbol will have a DownValue that points back to
    this FunctionDeclarationNode.

    Properties:
        `symbol_node`: The name (head) of the function, a SymbolNode.
        `inner_scope`: The scope created by the function, if any.
    """

    def __init__(self, symbol_node: SymbolNode = None, **kwargs):
        """
        Create a new function declaration.

        :param symbol_node: The name (head) of the function.
        :param kwargs: The arguments to treeNodeBase.
        """

        super().__init__(**kwargs)

        # The Head of the declaration. The symbol_node will point to a Symbol
        # in the symbol table. The symbol will have a DownValue that points
        # back to this FunctionDeclarationNode.
        self.symbol_node = symbol_node

        # The function need not have a scope if it takes no variable arguments.
        # The inner_scope will need to be created based on the construction
        # of this node.
        self.inner_scope = None

    @property
    def lhs(self):
        if self.children:
            return self.children[0]
        return None

    @lhs.setter
    def lhs(self, symbol_node: SymbolNode, arguments_pattern: treeNode = None):
        self.children[0] = symbol_node

    @property
    def rhs(self):
        try:
            return self.children[1]
        except:
            return None

    @rhs.setter
    def rhs(self, rhs_node: treeNode):
        if not self.children:
            self.children.append(None)
        self.children[1] = treeNode
