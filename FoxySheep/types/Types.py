"""
Classes for the type system. The difference between a Wolfram Language
type and a type in the target language can be blurry. Some design choices
have to be made about what types there should be.

The type of an AST node is dynamic in general and is computed during type
inference.
"""

from typing import List


# Since TreeTypeTrait is the only subclass modifying type comparison
# behavior, I don't need to make `is_subtype()` a static method of `TypeBase` so
# that it can be overridden by different subtypes as I did with `match_tree()`
# and `_match_node` in the `ASTNode` class.
def is_subtype(type_lhs:'TypeBase', type_rhs:'TypeBase') -> bool:
    """
    Determines if type_lhs is a subtype of type_rhs.

    :param type_lhs:
    :param type_rhs:
    :return: True if type_lhs is a subtype of type_rhs; otherwise, False.
    """

    # TODO: Implement type matching.
    pass


class TypeBase:

    @property
    def type_name(self):
        name = type(self).__name__

        # The type name is the name of the class without the suffix
        if name.endswith('Type'):
            return name[:-4]
        return name


class MathematicalTypeTrait:
    """
    This type is a mix-in that specifies the type trait that this type is a
    type of a mathematical expression.
    """
    pass


class NumberType(TypeBase, MathematicalTypeTrait):
    """
    This type includes floats and ints.
    """
    pass


class RealType(NumberType):
    pass


class IntegerType(NumberType):
    pass


class RationalType(NumberType):
    # Will this type ever arise in practice considering n/m will always be
    # parsed as division?
    pass


class SymbolType(TypeBase, MathematicalTypeTrait):
    """
    An identifier without a value and any other explicit or inferred type has
    type SymbolType. Do not confuse this type with the type of a SymbolNode,
    which may have any type.

    SymbolType plays the role of the most generic type. However, we are using
    the implementation language's (Python's) subclassing mechanism to
    implement both type traits, like MathematicalType, and type specificity,
    e.g. IntegerType is a NumberType. So the most generic type wants to be a
    subclass of every type trait class while simultaneously being a
    superclass of every type. The solution is that SymbolType is the only
    type that can be replaced with a non-subclass.
    """

    def __init__(self):
        super().__init__()


class TreeType:
    """
    This type is a mix-in that specifies the type trait that this type can
    appear as a non leaf node in a composite type represented by a tree
    structure.
    """

    def __init__(self, children: List["TypeBase"] = None,
                 parent: 'TreeType' = None, **kwargs):
        self.parent = parent
        self.children = children


class ListLikeType(TypeBase):
    """
    This class includes lists and associations.
    """
    pass
