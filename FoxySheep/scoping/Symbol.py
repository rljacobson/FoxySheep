from enum import IntEnum, auto as _auto
import FoxySheep.tree
from FoxySheep.tree import treeNode, FunctionDeclarationNode

class SymbolAttributes(IntEnum):
    Constant        = _auto()
    Flat            = _auto()
    HoldAll         = _auto()
    HoldAllComplete = _auto()
    HoldFirst       = _auto()
    HoldRest        = _auto()
    Listable        = _auto()
    Locked          = _auto()
    NHoldAll        = _auto()
    NHoldFirst      = _auto()
    NHoldRest       = _auto()
    NumericFunction = _auto()
    OneIdentity     = _auto()
    Orderless       = _auto()
    Protected       = _auto()
    ReadProtected   = _auto()
    SequenceHold    = _auto()
    Stub            = _auto()
    Temporary       = _auto()


class Symbol(FoxySheep.tree.Symbol):
    """
    Holds information about a particular symbol in a particular scope. In
    particular, it manages

        * OwnValues: Values without square brackets []. Only the first
        OwnValue is accessible via evaluating the symbol. Other OwnValues can
        only be set or accessed by manipulating OwnValues[name] itself.

        * DownValues: Function definitions, i.e., anything accessed with [].
        A DownValue can be considered a function declaration; it is the
        treeNode for the assignment that "creates" the DownValue.

        * DefaultValues: Default values for optional arguments.

        * Options: Option defaults for the symbol.

        * Attributes: A set of `SymbolAttributes`.

        * Messages: Messages of the form `symbol::tag`.
    """

    def __init__(self,
                 identifier: str,  # Required
                 own_values: list = None,
                 down_values: list = None,
                 default_values: dict = None,
                 # Values
                 options: set = None,
                 attributes: set = None,
                 messages: set = None,
                 # Conditions
                 required_head: 'Symbol' = None
                 # Not implemented:
                 # up_values: list = None,
                 # sub_values: list = None,
                 # n_values: list = None,
                 # format_values: list = None,
                 ):
        """


        :param identifier:
        :param own_values:
        :param down_values:
        :param default_values:
        :param options:
        :param attributes:
        :param messages:
        :param required_head:
        """

        self._identifier = identifier

        # We lazily create these container classes.
        self._own_values        = own_values
        self._down_values       = down_values
        self._default_values 	= default_values
        self._options 	        = options
        self._attributes 	    = attributes
        self._messages 	        = messages
        self._required_head     = required_head

        # Not implemented.
        # TODO: Implement UpValues.
        # self._up_values         = up_values
        # TODO: Implement SubValues.
        # self._sub_values        = sub_values
        # TODO: Implement NValues.
        # self._n_values          = n_values
        # TODO: Implement FormatValues.
        # self._format_values     = format_values

    @property
    def default(self):
        # Default values are associated to the position of a parameter. It is
        # possible to have a single default value without a position
        # designation. Internally, we associate the default value with
        # position -1.
        return self.get_default_at(-1)

    @default.setter
    def default(self, value):
        self.set_default_at(-1, value)

    def get_default_at(self, position: int):
        # Default values are associated to the position of a parameter. The
        # positions with defaults are sparse, so we use a dict rather than a
        # list to represent them.
        try:
            return self._default_values[position]
        except KeyError:
            pass
        return None

    def set_default_at(self, position: int, value: treeNode):
        if not self._default_values:
            self._default_values = dict()
        self._default_values[position] = value

    @property
    def identifier(self):
        return self._identifier

    @property
    def own_value(self):
        """
        Fetch the OwnValue of this symbol.

        TODO: Support multiple OwnValues.

        :return: An OwnValue, if one exists; otherwise None.
        """
        if self._own_values:
            return self._own_values[0]
        return None

    def find_matching_down_value(self, usage: treeNode):
        """
        Given a usage `f[3, 5]`, find the first DownValue of f matching the
        usage.

        :param usage: A function call.
        :return:
        """

        # TODO: Implement using Utils.PatternMatcher.match_pattern().

        return self._default_values[-1]

    def add_down_value(self, value: FunctionDeclarationNode):
        """
        Note: A DownValue is a function declaration.

        Adds a DownValue to the list of DownValues associated to this symbol.
        A DownValue must be a subclass of FunctionDeclarationNode. As with
        Mathematica, new DownValues overwrite existing DownValues having the
        same LHS, and DownValues are ordered according to the order they are
        added, except that DownValues with more specific LHS are ordered
        before DownValues with more general LHS.

        :param value: The DownValue to be added.
        """

        # TODO: Implement correct ordering of DownValues using Utils.PatternMatcher.match_pattern().

        self._default_values.append(value)
