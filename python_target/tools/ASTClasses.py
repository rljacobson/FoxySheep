# 'Node' is appended to every AST class name. There should be a class for
# every Wolfram Language construct we wish to transform or otherwise interact
# with.

from enum import IntEnum, auto

from AST import ASTNode


class Props(IntEnum):
    NamedChildren = auto()
    SuperClass = auto()
    DoNotCreate = auto()


ast_classes = \
{
    'pattern/BlankAbstract': {Props.NamedChildren: ['required_head']},
    'pattern/Blank': {Props.SuperClasses: ['BlankAbstractNode']},
    'pattern/BlankSequence': {Props.SuperClasses: ['BlankAbstractNode']},
    'pattern/BlankNullSequence': {Props.SuperClasses: ['BlankAbstractNode']},
    'pattern/Pattern': {Props.NamedChildren: ['identifier', 'pattern']},
    'Symbol': {Props.DoNotCreate: None},

}
