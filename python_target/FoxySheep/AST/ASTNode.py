"""
A collection of base classes and utility objects for building an abstract syntax tree representing a Mathematica program.
"""

import enum

class ASTNodeBase:
    """
    The base class of all AST node classes.
    """

    def __init__(self, children=None, parent=None, exprs=None, type=None):
        """
        Creates a node of the AST.

        :param children: A list of ASTNode objects that are children of this node.
        :param parent: The parent ASTNode of this node.
        :param exprs: A list of the ANTLR SyntaxTree objects that represent this node.
        :param is_math_expression: A flag representing whether this node is a mathematical expression (unset=-1, no=0, yes=1).
        """

        if children:
            self.children = children
        else:
            self.children = []

        self.parent = parent

        if exprs:
            self.exprs = exprs
        else:
            self.exprs = []

        self.type = type


class FunctionAttribute(enum.IntEnum):
    """An enum representing function attributes."""
    Listable = enum.auto()
    Flat = enum.auto()
    Orderless = enum.auto()
    OneIdentity = enum.auto()


class FunctionNodeBase(ASTNodeBase):
    """
    The base class of all AST node classes representing a callable function.
    """

    def __init__(self, identifier=None, symbol=None, **kwargs):
        """


        :param identifier: The name (head) of the function.
        :param symbol: The symbol associated to the function, or none if there is no symbol.
        :param kwargs: The arguments to ASTNodeBase.
        """

        super().__init__(**kwargs)

        self.identifier = identifier
        self.symbol = symbol

        self.scope = None
        self.function_attributes = set() # A set of `FunctionAttribute`s.
        self.options_pattern = None
        self.arguments_pattern = None

