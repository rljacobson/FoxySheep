"""
Contains utilities to match patterns in order to determine if a
declaration overwrites or specifies another, associate usages with
declarations, determine if a type is a subtype of another type, etc.

# `match(lhs_node, rhs_node)` and `match_pattern([lhs], [rhs])`

The `match(lhs_node, rhs_node)` function takes two ASTNodes and is a
convenience function that immediately calls `match_pattern([lhs], [rhs])`,
a function taking lists of ASTNodes with an optional argument specifying
which of lhs or rhs must generalize the other.

This module implements a simple recursive descent pattern recognizer for the
matcher. The match function is in the spirit of the Wolfram Language built-in
`MatchQ`, except this function returns an ordering of the trees if they
match, whereas `MatchQ` returns a boolean. Also, `MatchQ` is *asymmetric* at
least with respect to options: `OptionsPattern` needs to be on the rhs in
`MatchQ`. Since this function returns an ordering, it is *antisymmetric*.

AST trees are partially ordered with respect to pattern matching in Wolfram
Language. As a consequence of this partial ordering, we have, for example,
that `f[2, _]` and `f[_, 5]` are incomparable. We the partial ordering
induced on individual node can be described as follows:

    ("-->" = "is generalized by")

                    +--> __ --+
    nonpattern--> _ +         |--> __. --> ___ --> ___.
                    +--> _. --+
    Level: 0      1      2          3       4       5

Note that _. and __ in level 2 are NOT comparable.

This matcher DOES match Head criteria, as in f[x_Integer]. The head must
be a SymbolNode.

This matcher DOES NOT evaluate conditional criteria (uses of /;),
since evaluation of the conditional for a given input can only be
determined at runtime. However, the presence of a conditional
*specializes* the pattern relative to the same pattern but without the
conditional. If both lhs and rhs have a conditional, they must
themselves match.

DefaultValues, along with all other  \*Values, are not included in
the matching at all (in keeping with `MatchQ`'s behavior). Only the
default value's parent OptionalNode is involved in the match.


# find_bound_variables(signature: FunctionDeclarationNode)

Constructs a list of Symbols that are bound within the scope of a function.

"""

from enum import IntEnum, auto
from typing import List, Tuple

from FoxySheep.tree.symbol_node import SymbolNode
from FoxySheep.scoping import Scope, Symbol
from FoxySheep.tree import treeNode
from FoxySheep.tree.pattern import PatternNode, BlankAbstractNode
from FoxySheep.utils.misc import camel_to_snake


def get_bound_symbols(signature: treeNode, scope: Scope = None)->List[Symbol]:
    """
    Creates a list of symbols bound by the given function signature (a
    pattern). Signature should have the form `Head[arguments_pattern]`. The
    `Head` of signature is ignored. Note that a signature is the LHS of a
    function declaration in FoxySheep.

    If a `Scope` is given, each symbol is added to `scope` after it is
    created. The `scope` should be that of the FunctionDeclarationNode. It is
    the caller's responsibility to create `scope` correctly.

    This function recursively searches the tree rooted at signature,
    so variables buried in other structures will be found, e.g. the `x` in
    `f[{x_}]`.

    :param signature: The function signature to search.
    :param scope: The scope of the current function to which each symbol
    should be added.
    :return: A list of `Symbols`
    """

    symbol_list = []
    # Create a *copy* of `signature`'s list of children. Since arguments is a
    # stack, we reverse the list so that the leftmost child is on top.
    arguments = list(reversed(signature.children))

    # Recursively add symbols to symbol_list
    _find_bound_symbols(arguments, symbol_list)

    # Add each symbol to the scope.
    scope.add_symbols(symbol_list)

    return symbol_list


def _find_bound_symbols(arguments: List[treeNode], symbol_list: list):
    if not arguments:
        # Done.
        return

    # Get the next node.
    node = arguments.pop()

    # If we found a variable
    if type(node) == PatternNode and node.identifier:
        head = None # The default.
        # Check if there is a required Head.
        if node.pattern and isinstance(node.pattern, BlankAbstractNode):
            head = node.pattern.required_head
        symbol = Symbol(node.identifier, required_head = head)

    # If we found something with children:
    elif node.children:
        # Recurse to children before moving on.
        child_arguments = list(reversed(node.children))
        _find_bound_symbols(child_arguments, symbol_list)

    # Now continue with the rest of arguments.
    _find_bound_symbols(arguments, symbol_list)


class ComparisonValue(IntEnum):
    """
    Possible relations in a partially ordered set.
        Specifies/Less: <
        Equal: =
        Generalizes/Greater: >
        Incomparable/Unequal: cannot be compared.
    The matcher returns a ComparisonValue.
    """
    Less = Specializes = auto()
    LessOrEqual = SpecializesOrEqual = auto()
    Equal = auto()
    GreaterOrEqual = GeneralizesOrEqual = auto()
    Greater = Generalizes = auto()
    Unequal = Incomparable = auto()


# The partial ordering excluding `Optional`s.
_order = {BlankNode: 1, BlankSequenceNode: 2, BlankNullSequenceNode: 3}


def match(lhs: List[treeNode], rhs: List[treeNode], gt: bool = None):
    """
    The driver of the pattern matcher. Does dynamic dispatch according to
    the subclass of each treeNode.

    :param gt: True if the lhs > rhs, False if rhs > lhs, and None if
    undetermined.
    :param lhs: A list of treeNode instances in reverse order from how
    they appear in the tree.
    :param rhs: A list of treeNode instances in reverse order from how
    they appear in the tree.
    :return: A ComparisonValue.
    """

    # The implementation of this function is complicated by the fact that we
    # are determining *which* of lhs/rhs dominates the other

    # TODO: Incorporate symbol attributes in matching.
    # The symbol attributes `Flat`, `Orderless`, and `OneIdentity` should
    # influence pattern matching, but this is not implemented.

    # TODO: Check for OptionsPattern first.

    # Base cases.
    if not lhs:
        if not rhs:
            return ComparisonValue.Equal
        else:
            success, gt = _swap(gt, False)
            if success:
                return _flip_result(match(rhs, lhs, gt))
            else:
                # We couldn't swap rhs and lhs, so either lhs!=rhs or lhs<=rhs
                # AND rhs<=lhs. Either way, match fails.
                return ComparisonValue.Incomparable

    # Peek at the top node.
    lhs_node = lhs[-1]

    # PatternNode is used to bind a symbol (variable name) to a pattern.
    # We ignore names of patterns, so we unwrap any PatternNode we find,
    # caring only about the patterns they contain. In the pathological
    # case that the PatternNode contains no pattern, we leave it alone.
    if isinstance(lhs_node, PatternNode):
        if PatternNode.pattern:
            lhs_node = lhs[-1] = PatternNode.pattern

    # Check if we should swap lhs and rhs, i.e., set the value of lhs_dominates.
    if rhs:
        rhs_node = rhs[-1]
        if type(rhs_node) == OptionalNode:
            if type(lhs_node) == OptionalNode:
                # Should we do a _match_node here first?
                # Do the optional rhs first.
                _match_optional(lhs, rhs, gt, optional_on_lhs = False)
            else:
                # Try to swap.
                success, gt = _swap(gt, False)
                if success:
                    return _flip_result(match(rhs, lhs, gt))
                else:
                    return ComparisonValue.Incomparable
        if type(lhs_node) in _order:
            if type(rhs_node) in _order:
                if _order[type(lhs_node)] < _order[type(rhs_node)]:
                    # Try to swap.
                    success, gt = _swap(gt, False)
                    if success:
                        return _flip_result(match(rhs, lhs, gt))
                    else:
                        return ComparisonValue.Incomparable
            # Enforce gt/prohibit any swap.
            _swap(gt, True)

    # This is the lazy programmers way of doing a switch on only a subset of
    # node classes. If the node's class is one for which we have an matching
    # _match function, call the appropriate function by ( string) name which
    # is extracted from the node's class's name. (The switch turns into a
    # hash.) This way, if we need to implement a new submatch function,
    # we just implement it and it will be used automatically.
    method = _dynamic_dispatch(lhs_node)
    if method:
        return method(lhs, rhs, gt)

    # At this point, lhs[-1] is not a pattern, and if rhs[-1] exists,
    # it is also not a pattern. If rhs is empty, match fails.
    if not rhs:
        return ComparisonValue.Incomparable

    # Check for equality of the trees rooted at lhs_node and rhs_node.
    result = _match_node(lhs, rhs, gt)

    return result


def match_pattern(lhs: treeNode, rhs: treeNode):
    """
    Determines if the argument pattern with root node_lhs matches the
    argument pattern with root node_rhs.


    :param lhs: The root node of the tree on the left to be matched against.
    :param rhs: The root node of the tree on the right to be matched against.
    :param match_types: Boolean. Whether or not to also match the inferred
    types. NOT IMPLEMENTED.
    :return: A ComparisonValue: Specifies ("<"), Equals ("="), Generalizes (
    ">"), or Incomparable.
    """

    # The work of doing the pattern matching is delegated to the match
    # function which takes lists of treeNodes, not treeNodes themselves.
    return match([lhs], [rhs])


def _synthesize(lhs: int, rhs: int) -> int:
    """
    Takes two ComparisonValues coming from comparing different parts of a
    tree  and synthesizes a compatible ComparisonValue. The compatible
    value is the most restrictive.

        >  and <  --> !=
        >  and >  --> >
        >  and >= --> >
        <  and >  --> !=
        <  and == --> <
        <  and <= --> <
        <= and >=--> ==
         etc.

    :param lhs:
    :param rhs:
    :return:
    """

    # Shortcut if they're the same.
    if lhs == rhs:
        return lhs

    # WLOG, assume lhs > rhs.
    if rhs > lhs:
        tmp = rhs
        rhs = lhs
        lhs = tmp

    if lhs == ComparisonValue.Incomparable:
        return lhs

    if lhs <= ComparisonValue.Equal:
        return rhs
    elif lhs == ComparisonValue.GreaterOrEqual and \
        rhs >= ComparisonValue.LessOrEqual:
        return ComparisonValue.Equal
    elif rhs == ComparisonValue.Equal:
        return lhs

    return ComparisonValue.Incomparable


def _swap(gt: bool, to: bool) -> Tuple[bool, bool]:
    """
    Attempts to set gt while enforcing the constraint that gt can be set to
    False only once and then only if gt is None, and gt cannot be set back to
    True once set to False. The swap fails only if one of the following:
        gt is False
        gt != None and to==False
    Here is every case:

        gt   | to    | success | result
        -----+-------+---------+-------
        None | True  | True    | True
        None | False | True    | False <-- Only case gt and to != success
        True | True  | True    | True
        True | False | False   | True
        False| True  | False   | False
        False| False | False   | False <-- Only case to==success != result

    Returns a tuple (success, lhs_dominates) where success is a boolean
    indicating whether the swap was successful, and the value of
    lhs_dominates after the attempt.

    :param gt: Boolean. What we are attempting to change.
    :param to: Boolean. What we are trying to change it to.
    :return: Tuple(success, new gt value).
    """
    if gt is None and not to:
        # gt has not been set and to==False
        return True, False

    gt = bool(gt)
    success = gt and to

    if not to and not success:
        return False, False

    # Covers all other cases.
    return (gt and to), (to == success)


def _flip_result(result: int):
    """
    Convenience function that exchanges < for > if lhs_dominates is False.

    Since this function is applied to return values of match(rhs, lhs) to
    flip-flop < and <= if gt is false. Since gt can only be flipped once,
    a call with argument order match(rhs, lhs) can only occur once, and so we
    don't ever have to flip-flop the other direction.

    :param result: A ComparisonValue.
    :return: Corrected ComparisonValue.
    """

    if result == ComparisonValue.Greater:
        return ComparisonValue.Less
    elif result == ComparisonValue.GreaterOrEqual:
        return ComparisonValue.LessOrEqual
    elif result == ComparisonValue.Less:
        # A sanity check. If we are constrained to lhs =< rhs and we find
        # that lhs > rhs, then lhs and rhs are incomparable.
        return ComparisonValue.Incomparable
    elif result == ComparisonValue.LessOrEqual:
        # Another sanity check. If we are constrained to lhs =< rhs and
        # we find that lhs > rhs, then lhs == rhs.
        return ComparisonValue.Equal

    return result


def _dynamic_dispatch(node: treeNode):
    """
    Returns the function _match_node_class_name if exists and None otherwise.

    :param node: An instance of some treeNode subclass.
    :return: The function _match_node_name, or None if it doesn't exist.
    """

    # Instance method names are in snake_case.
    method_name = '_match_' + camel_to_snake(
            # Remove the "Node" from the class name.
            node.__class__.__name__[:-4]
            )
    return globals().get(method_name, None)


def _match_node(lhs: List[treeNode], rhs: List[treeNode], gt: bool):
    """
    Determines whether the node at the top of lhs is the same treeNode
    subclass as the node at the top of rhs. In the case of two `SymbolNode`s,
    the `SymbolNodes`s match if and only if their names match. If the nodes
    match, match is called on their children. If successful, the match is
    continued with lhs and rhs.

    This function assumes lhs and rhs have been preprocessed by match,
    so do not call this function directly. Instead, call match_pattern.

    :param lhs: The first of two node lists to be compared.
    :param rhs: The second of two node lists to be compared.
    :param gt:  "Greater Than," holds state of whether lhs > rhs.

    :param match_types: Boolean. If True, one of the nodes' `type` property
    class type must be either the same class type or a subclass of the
    other node's `type` property's class type. NOT IMPLEMENTED.

    :return: A ComparisonValue: Specifies ("<"), Equals ("="), Generalizes (
    ">"), or Incomparable.
    """

    # TODO: Implement type matching.
    # if match_types:
    #     handle_error(NotImplementedError_("Matching types", treeNode=lhs_node))


    # Peak the current nodes.
    lhs_node = lhs[-1]
    rhs_node = rhs[-1]

    # The caller prohibits lhs_node < rhs_node, so we assume lhs_node >=
    # rhs_node.
    if type(lhs_node) != type(rhs_node):
        return ComparisonValue.Incomparable

    # SymbolNodes have an additional requirement that identifiers must match.
    if type(lhs_node) == SymbolNode and lhs_node.identifier != rhs_node.identifier:
        return ComparisonValue.Incomparable

    # Nodes themselves match. Descend into their children. Note that we make
    # *copies* of each list of children.
    children_lhs = list(reversed(lhs_node.children)) if lhs_node.children \
        else []
    children_rhs = list(reversed(rhs_node.children)) if rhs_node.children \
        else []
    result = match(children_lhs, rhs_node.children, gt)
    # Don't bother matching the rest if already !=.
    if result == ComparisonValue.Incomparable:
        return result

    # Match the rest of the stack.
    lhs_node = lhs.pop()
    rhs_node = rhs.pop()
    rest_result = match(lhs, rhs, gt)
    if rest_result == ComparisonValue.Incomparable:
        # Failure. Rewind the node stack.
        lhs.append(lhs_node)
        rhs.append(rhs_node)
        return rest_result

    return _synthesize(ComparisonValue.Equal, rest_result)


def _match_optional(lhs: List[treeNode],
                    rhs: List[treeNode],
                    gt: bool,
                    optional_on_lhs: bool = True):
    """
    Tries to match the optional node on the top of the lhs stack. It does
    this by first trying a match with the node, and if it fails, trying again
    without the node.

    :param lhs:
    :param rhs:
    :param gt:
    :return:
    """
    # DefaultValues, along with all other  \*Values, are not included in
    # the matching at all (in keeping with `MatchQ`'s behavior). Only the
    # default value's parent OptionalNode is involved in the match.

    if optional_on_lhs:
        option_side = lhs
    else:
        option_side = rhs

    # Get the pattern out of the option_node.
    option_node = option_side.pop()
    pattern_node = option_node.pattern

    # Try first with the node.
    option_side.append(pattern_node)
    result = match(lhs, rhs, gt)
    if result != ComparisonValue.Incomparable:
        # It worked.
        return result

    # Now try without the node. Take it back off the lhs stack.
    option_side.pop()
    result = match(lhs, rhs, gt)
    if result == ComparisonValue.Incomparable:
        # Failure. Rewind the stack.
        option_side.append(option_node)

    return result


def _match_blank(lhs: List[treeNode], rhs: List[treeNode], gt: bool):
    if not rhs:
        return ComparisonValue.Incomparable

    lhs_node = lhs.pop()
    rhs_node = rhs.pop()

    result = match(lhs, rhs, gt)
    if result == ComparisonValue.Equal and type(rhs_node) != BlankNode:
        return ComparisonValue.Generalizes
    elif result == ComparisonValue.Incomparable:
        # Failure. Rewind the node stacks.
        lhs.append(lhs_node)
        rhs.append(rhs_node)

    return result


def _match_blank_sequence(lhs: List[treeNode], rhs: List[treeNode], gt: bool):
    # BlankSequence needs to match at least one node in rhs.
    if not rhs:
        return ComparisonValue.Incomparable

    # We automatically consume the rhs node.
    rhs_node = rhs.pop()
    # The rest is exactly like BlankNullSequence, so we replace the top of
    # lhs with a BlankNullSequence.
    lhs_node = lhs.pop()
    lhs.append(BlankNullSequenceNode())

    result = _match_blank_null_sequence(lhs, rhs, gt)
    if result in (ComparisonValue.Less, ComparisonValue.Incomparable):
        # Failure. Rewind the stack.
        lhs[-1] = lhs_node
        rhs.append(rhs_node)
        return ComparisonValue.Incomparable
    elif result == ComparisonValue.LessOrEqual:
        return ComparisonValue.Equal

    return result


def _match_blank_null_sequence(lhs: List[treeNode], rhs: List[treeNode], gt: bool):
    if not rhs:
        return ComparisonValue.Generalizes

    # `_match_blank_null_sequence` (and `_match_blank_sequence`) eats everything
    # it can while still successfully matching. This code is very similar to
    # `_match_Optional`, except `Optional` wraps a pattern object.

    # Try first to consume a node, leaving BlankNullSequence on the stack.
    rhs_node = rhs.pop()
    result = match(lhs, rhs, gt)
    if result != ComparisonValue.Incomparable:
        # It worked.
        return result

    # Now try without consuming a node and removing BlankNullSequence from
    # the stack.
    rhs.append(rhs_node)
    lhs_node = lhs.pop()
    result = match(lhs, rhs, gt)
    if result == ComparisonValue.Incomparable:
        # Failure. Rewind the stack.
        lhs.append(lhs_node)

    return result
