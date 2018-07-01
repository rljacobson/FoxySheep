"""
Classes for the type system. The difference between a Wolfram Language type and a type in the target language can be blurry. Some design choices have to be made about what types there should be.

The type of an AST node is dynamic in general and is computed during type inference.

"""

class TypeBase():
    pass


## Mathematical types.

class MathematicalType(TypeBase):
    """
    Mathematical types.
    """
    pass

class NumberType(MathematicalType):
    """
    This type includes floats and ints.
    """
    pass

class FloatType(NumberType):
    pass

class IntegerType(NumberType):
    pass

class SymbolType(MathematicalType):
    """
    An identifier without a value and any other explicit or inferred type has type SymbolType.
    """

    def __init__(self, name=None):
        super().__init__()
        self.name = name


class ListLikeType(TypeBase):
    """
    This class includes lists and associations.
    """
    pass