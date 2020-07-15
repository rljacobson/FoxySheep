"""
Classes and utilities for handling built-in symbols which do not have an
associated `SymbolNode` representing its declaration. We call such a symbol
*virtual* because its declaration does not actually exist in the source,
because built-in functions and symbols are never explicitly declared.

Currently this is just a wrapper that provides access to the services of
WolframLanguageData.
"""

from FoxySheep.scoping import Symbol
import FoxySheep.utils.WolframLanguageData as wld


def find_virtual_symbol(cls, name: str) -> Symbol:
    """
    Returns a virtual symbol representing a built-in symbol or function.

    :param name: String, the name of the symbol.
    :return: A VirtualNode
    """

    return wld.find_symbol(name)


def get_operator_name(symbolic_rep: str) -> str:
    """
    Given the symbolic string representation for a built-in
    operator, returns its canonical name.

    For example:

        >>> get_operator_name('/@')
        'Map'

    :param symbolic_rep: The symbolic string representation of the operator.
    :return: The canonical name of the operator as a string.
    """

    return wld.get_operator_name()
