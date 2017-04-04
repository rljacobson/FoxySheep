DIR=.

all: FoxySheepLexer.py

FoxySheepLexer.py: FoxySheepParser.py
    (cat FoxySheep/LexerPreface.py && cat generated/FoxySheepLexer.py) > generated/FoxySheepLexer.py

FoxySheepParser.py: ../FoxySheep.g4 ../FoxySheepLexerRules.g4 generated/__init__.py
	antlr4 -Dlanguage=Python2 -o $(DIR)/generated -visitor $(DIR)/../FoxySheep.g4

run: FoxySheepLexer.py
	python example.py

clean:
	rm -f $(DIR)/generated/FoxySheep*

generated/__init__.py:
	touch $(DIR)/generated/__init__.py