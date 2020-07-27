"""Robert Jacobson's ANTL4-based translator parser for Mathematica."""

from FoxySheep.generated.InputFormLexer import InputFormLexer
from FoxySheep.generated.InputFormParser import InputFormParser
from FoxySheep.generated.InputFormListener import InputFormListener
from FoxySheep.generated.InputFormVisitor import InputFormVisitor

from FoxySheep.generated.FullFormLexer import FullFormLexer
from FoxySheep.generated.FullFormParser import FullFormParser
from FoxySheep.generated.FullFormListener import FullFormListener
from FoxySheep.generated.FullFormVisitor import FullFormVisitor

from FoxySheep.emitter.full_form import FullFormEmitter, input_form_to_full_form
from FoxySheep.emitter.python import input_form_to_python

from FoxySheep.parser import (
    ff_parse_tree_from_string,
    if2ff,
    parse_tree_from_string,
)
from FoxySheep.post_parser import PostParser
from FoxySheep.tree.pretty_printer import (
    pretty_print,
    pretty_print_string,
    PrettyPrinter,
    PrettyPrinterCompact,
)
from FoxySheep.tree import SymbolNode
from FoxySheep.__main__ import REPL

from FoxySheep.version import VERSION

# This ensures VERSION will appear in pydoc
__version__ = VERSION
