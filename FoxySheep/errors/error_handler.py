"""
This module defines the mechanism by which errors are handled in FoxySheep.
"""

import sys

from antlr4.ParserRuleContext import ParserRuleContext
from tree import treeNode


def _print_err(*args, flush=False):
    sys.stderr.write(' '.join(map(str, args)) + '\n')
    if flush:
        sys.stderr.flush()


class ErrorBase:

    def __init__(self, parse_tree_node: ParserRuleContext=None,
                 ast_node: treeNode = None):
        self.parse_tree_node = parse_tree_node
        self.ast_node = ast_node

        class_name = type(self).__name__
        if class_name.endswith('Base'):
            class_name = class_name[:-4]
        elif class_name.endswith('_'):
            class_name = class_name[:-1]
        self.name = class_name

        self.message = 'Unknown error.'

    def get_line_number(self):
        """
        Returns the line number in the source text where the error occurs, or -1 if unknown.

        :return: line number, integer.
        """
        if self.parse_tree_node:
            start_token = self.parse_tree_node.start
            return start_token.getLine()
        # We don't have an associated parse_tree_node.
        return -1

    def get_char_position(self):
        """
        Returns the character position in the line in the source text where the error occurs, or -1 if unknown.

        :return: character position, integer.
        """
        if self.parse_tree_node:
            start_token = self.parse_tree_node.start
            return start_token.getCharPositionInLine()
        # We don't have an associated parse_tree_node.
        return -1

    def to_string(self):
        line = self.get_line_number()
        char = self.get_char_position()
        location = ''
        if line > -1 or char > -1:
            location = '{line}:{char}:'.format(line=line, char=char)

        return '{location}{error_name}: {message}'.format(
                location=location,
                error_name=self.name,
                message=self.message
                )


class UnknownFunctionError(ErrorBase):

    def __init__(self, identifier='', **kwargs):
        super().__init__(**kwargs)

        self.message = 'The function {identifier} is being called but is not ' \
                       'yet defined.'.format(identifier=identifier)


class NotImplementedError_(ErrorBase):

    def __init__(self, feature: str = '', **kwargs):
        super().__init__(**kwargs)

        self.message = '{feature} has not yet been implemented.'.format(
            feature=feature)


class ExternalExceptionError(ErrorBase):
    """
    An exception from an external library repackaged as an ErrorBase subclass.
    """

    def __init__(self, e: Exception, **kwargs):
        super().__init__(**kwargs)

        self._exception = e
        self.message = str(e)


def handle_error(error: ErrorBase):
    _print_err(error.to_string())
