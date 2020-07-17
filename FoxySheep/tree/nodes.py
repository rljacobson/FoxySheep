"""A collection of base classes and utility objects for building an abstract
syntax tree representing a Mathematica program. """

from typing import List

from FoxySheep.foxy_types import TypeBase

class Symbol(object):
    pass

class SymbolNode(object):
    pass

class treeNode(object):
    """
    The base class of all tree node classes.
    """

    def __init__(
        self,
        children: List["treeNode"] = None,
        parent: "treeNode" = None,
        type_: TypeBase = None,
        exprs: list = None,
    ):
        """
        Creates a node of the tree.

        :param children: A list of treeNode objects that are children of this node.
        :param parent: The parent_scope treeNode of this node.
        :param exprs: A list of the ANTLR SyntaxTree objects that represent this node.
        :param type_: The type of the value held by this node.
        """

        self.children = children
        self.parent = parent

        # A list of the ANTLR SyntaxTree objects that represent this node.
        self.exprs = exprs

        # The type returned or represented by the node.
        self._type = type_

        # Subclasses can register names for their child nodes which can be
        # accessed with __getattr__.
        self._named_children: dict = None

    def __getattr__(self, key: str):
        # Implements a mechanism to have child nodes with names as
        # attributes. See _add_named_child().

        # Check to see if key is one of the named children.
        if not self._named_children or key not in self._named_children:
            raise AttributeError(key)

        # If key is the name of a named child, find its index within
        # self.children.
        index = self._named_children[key]

        # Check that this node has children.
        if not self.children:
            return None

        # Try to retrieve the child.
        try:
            return self.children[index]
        except IndexError:
            pass

        return None

    def __setattr__(self, key, value):
        # Implements a mechanism to have child nodes with names as
        # attributes. See _add_named_child().

        # Check to see if key is one of the named children.
        if not self._named_children or key not in self._named_children:
            # Nope, not one of ours.
            super().__setattr__(key, value)

        # Since key is the name of a named child, find its index within
        # self.children.
        index = self._named_children[key]

        # Check that this node has children.
        if not self.children:
            self.children = []
        # Check that key's index exists.
        if len(self.children) < index + 1:
            # This index in self.children doesn't exist yet. We just extend
            # self.children with a list of None's.
            amount = index + 1 - len(self.children)
            self.children.extend(amount * [None])

        # Set the value.
        self.children[index] = value

    def _add_named_child(self, name: str, index: int):
        """
        Subclasses can register names for children at given indices in
        self.children so that a child with a name can be accessed by
        treeNode.name.

        :param name: String, the name of the child.
        :param index: Integer, the index in self.children at which the child
        lives.
        :return:
        """
        # Lazy instantiation.
        if not self._named_children:
            self._named_children = dict()
        self._named_children[name] = index

    def _add_named_children(self, names: List[str]):
        """
        Adds named children, automatically indexing starting at 0.

        :param names: List[str], the names of the children in order.
        :return:
        """
        for n, name in enumerate(names):
            self._add_named_child(name, n)

    def specify_type(self, type_: TypeBase):
        """
        The word *specify* is intentional, as type_ must be a subtype of this
        node's type unless this node's type is SymbolType.

        :param type_:
        :return:
        """
        # TODO: Implement treeNode.specify_type()
        pass

    @property
    def type_(self):
        return self._type
