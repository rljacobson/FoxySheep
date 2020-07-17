from FoxySheep.tree.nodes import treeNode, Symbol


class SymbolNode(treeNode):
    """
    A SymbolNode is a particular appearance in the source code of a
    name.

    A SymbolNode is not an entry in a symbol table. The Symbol that this
    SymbolNode points to is managed by the symbol table.

    In the case that the SymbolNode represents a usage of the symbol with no
    prior declaration, the SymbolNode gets its own (empty) symbol,
    and subsequent uses of the symbol will refer to this SymbolNode as their
    definition until the creation of a new definition.

    Properties:
        `identifier` String, the name of the symbol.
        `declaration` Where the symbol was declared.
    """

    def __init__(self, identifier: str, symbol: Symbol = None, **kwargs):
        """
        Create a SymbolNode representing an appearance of identifier in the
        source language. If a Symbol is provided, this SymbolNode's Symbol
        is the same type instance as declaration.

        :param identifier:
        :param UpValue:
        :param kwargs:
        """
        super().__init__(**kwargs)
        self.identifier = identifier
        self._symbol = symbol

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, symbol: Symbol):
        assert symbol.identifier == self.identifier
        self._symbol = symbol
