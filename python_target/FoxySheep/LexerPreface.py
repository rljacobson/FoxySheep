# encoding: utf-8
from __future__ import print_function

# In order for the generated lexer to subclass our lexer base class, we
# have to _manually_ add the following lines to the generated lexer,
# generated/FoxySheepLexer.py. Of course, we don't actually do this
# manually. Instead we do some bash magic:
#     cat FoxySheep/LexerPreface.py generated/FoxySheepLexer.py > tmp.py && mv tmp.py generated/FoxySheepLexer.py

#from FoxySheepParser import FoxySheepParser
#from FoxySheep.Lexer import Lexer
from antlr4 import *
from FoxySheepParser import FoxySheepParser
from .. import Lexer

# Generated from ../FoxySheep.g4 by ANTLR 4.7