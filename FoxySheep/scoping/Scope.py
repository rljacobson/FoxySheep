"""
Classes for Scoping.
"""
from typing import List

import FoxySheep.tree

from enum import Enum, auto as _auto
from FoxySheep.scoping import Symbol


class ScopeType(Enum):
    Empty = _auto()
    Table = _auto()
    Solve = _auto()
    Integrate = _auto()
    Limit = _auto()
    Plot = _auto()
    Manipulate = _auto()
    Module = _auto()
    Function = _auto()
    AnonymousFunction = _auto()
    Rule = _auto()


class Scope(FoxySheep.tree.Scope):
    """
    Represents the local scope of a Scoping construct, e.g. SetDelayed, Table

    Properties:
        `parent`: The Scoping construct to which this scope belongs; a
        DownValue.

        `parent_scope`: A reference to the containing scope.

        `self.symbols = dict()`: Holds the local variables.

    The next four properties derive from the scope type as given by the
    Wolfram Language built-in `_SyntaxInformation[symbol]`:

        `self.scope_type = scope_type`:  A value from the ScopeType enum
        describing how the local variables are declared.

        `self.scope_start = scope_start`: The starting position of the local
        variable list.

        `self.scope_end = scope_end` The end position of the local variable
        list.

        `self.body_position = body_position` The position of the "body"
        expression existing within this scope.
    """

    def __init__(
        self,
        parent: FoxySheep.tree.treeNode = None,
        parent_scope: "Scope" = None,
        scope_type: int = None,
        scope_start: int = -1,
        scope_end: int = -1,
        body_location: int = -1,
    ):
        """
        Create a new local scope.

        :param parent: The Scoping construct to which this scope belongs; a
        DownValue.
        :param parent_scope: A reference to the containing scope, or None if
        this is the global scope.
        :param scope_type: A value from the ScopeType enum.
        :param scope_start: The starting position of the local variable list.
        :param scope_end: The end position of the local variable list.
        :param body_location: The position of the "body" expression existing
        within this scope.
        """

        self.parent = parent
        self.parent_scope = parent_scope
        self._symbols = dict()
        self.scope_type = scope_type
        self.scope_start = scope_start
        self.scope_end = scope_end
        self.body_position = body_location

    def find_symbol(self, identifier: str) -> Symbol:
        return self._symbols.get(identifier, default=None)

    def add_symbol(self, symbol: Symbol):
        """
        Adds a new symbol to the Scope.

        A symbol added to a local scope must be declared by virtue of a
        Scoping construct (`Module`, `Table`, `SetDelayed`, etc.), as all
        other symbols are added to the `GlobalScope`.

        :param symbol: The Symbol object to add to the scope.
        :return:
        """

        # TODO: Check that another symbol with the same identifier is not already in this scope.
        self._symbols[symbol.identifier] = symbol

    def add_symbols(self, symbols: List[Symbol]):
        for symbol in symbols:
            self.add_symbol(symbol)


class GlobalScope(Scope):
    """This class stores user-declared symbols in the global scope. Note that
    virtual symbols are not stored in this class but rather are managed by a
    VirtualSymbolProvider.

    Note that any new symbol that is not created by a Scoping construct (
    `Module`, `Table`, etc.) is created in the `GlobalScope`.
    """

    def __init__(self):
        super().__init__(parent=None)
        # rocky: VirtualSymbolProvider is missing in FoxySheep
        # self._virtual_symbol_provider = VirtualSymbolProvider()

    def find_symbol(self, identifier: str) -> Symbol:
        """
        First searches for `identifier` in the list of user-defined symbols
        in the global namespace. If no concrete declaration for the symbol is
        found, we look in the database of built-in symbols, returning a
        VirtualNode if it's found. Otherwise, we return None.

        :param identifier: String, the name of the symbol we are searching
        for.
        :return: A concrete symbol declaration, or a VirtualNode
        representing the "declaration" of a built-in symbol, or None if the
        symbol isn't found.
        """

        # Search the global namespace for user-declared symbols.
        found = self._symbols.get(identifier, default=None)
        if found:
            return found

        # Now ask our VirtualSymbolProvider to search the database of
        # built-in symbols.
        return self._virtual_symbol_provider.find_virtual_symbol(identifier)


class ScopeStack(object):
    """
    A stack data structure that keeps track of the (linear) nested scopes as
    we walk the AST.

    Properties:
        `stack` A Python list of scopes.
    """

    def __init__(self, global_scope: GlobalScope = None):
        self._stack: List[Scope] = []
        if global_scope:
            self._stack.append(global_scope)
        else:
            self._stack.append(GlobalScope())

    def push(self, scope: Scope):
        self._stack.append(scope)

    def pop(self) -> Scope:
        return self._stack.pop()

    def find_symbol(self, identifier: str) -> Symbol:

        for scope in reversed(self._stack):
            found = scope.find_symbol(identifier)
            if found:
                return found

        # The symbol isn't found in any local scope.
        return None
