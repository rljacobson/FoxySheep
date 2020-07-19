from antlr4 import ParseTreeWalker
from FoxySheep.post_parser import PostParser

def input_form_post(tree):
    """Post process the parse tree. In particular, flatten some flat
    operators. Some operators appear in the source text without any
    explicit associativity, such as `Plus`, and are parsed into arbitrary
    tree structures.
    """

    walker = ParseTreeWalker()
    post_parser = PostParser()
    walker.walk(post_parser, tree)

    # The PostParser can restructure the tree in a way that changes the root.
    if tree.parentCtx is not None:
        tree = tree.parentCtx
    return tree
