all: FoxySheepParser.py

FoxySheepParser.py: FoxySheep.g4 FoxySheepLexerRules.g4
	antlr4 -Dlanguage=Python2 -o generated -visitor FoxySheep.g4
	touch generated/__init__.py

run: FoxySheepParser.py
	python FoxySheep.py

clean:
	rm generated/*.py?
	rm generated/*.tokens
	