# In order for the generated lexer to subclass our lexer base class, we
# have to _manually_ add the following lines to the generated lexer,
# generated/FoxySheepLexer.py. Of course, we don't actually do this
# manually. Instead we do some bash magic:
#     (cat FoxySheep/LexerPreface.py && cat generated/FoxySheepLexer.py) > generated/FoxySheepLexer.py

from generated.FoxySheepParser import FoxySheepParser
from FoxySheep.Lexer import Lexer
