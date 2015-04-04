DIR=/Users/rljacobson/Documents/Development/FoxySheep/python\ target

all: FoxySheepParser.py

FoxySheepParser.py: ../FoxySheep.g4 ../FoxySheepLexerRules.g4 generated/__init__.py
	antlr4 -Dlanguage=Python2 -o $(DIR)/generated -visitor $(DIR)/../FoxySheep.g4

run: FoxySheepParser.py
	python FoxySheep.py

clean:
	rm $(DIR)/generated/*

generated/__init__.py:
	touch $(DIR)/generated/__init__.py