all: generated/FoxySheepParser.py

run: generated/FoxySheepParser.py
	python example.py

generated/FoxySheepParser.py: ../FoxySheep.g4 ../FoxySheepLexerRules.g4 FoxySheep/LexerPreface.py generated/__init__.py
	antlr4 -Dlanguage=Python2 -o generated -visitor ../FoxySheep.g4
	# antlr4 does not respect the -o flag??
	mv -f FoxySheep.tokens FoxySheepLexer.py FoxySheepLexer.tokens FoxySheepListener.py FoxySheepParser.py FoxySheepVisitor.py generated
	# The next two lines modify the generated lexer.
	cat FoxySheep/LexerPreface.py generated/FoxySheepLexer.py > tmp.py
	mv -f tmp.py generated/FoxySheepLexer.py

movegenerated: generated/FoxySheepParser.py
	mv -f FoxySheep.tokens FoxySheepLexer.py FoxySheepLexer.tokens FoxySheepListener.py FoxySheepParser.py FoxySheepVisitor.py generated

clean:
	rm -f generated/FoxySheep*
	rm -f tmp.py

# This rule is useful if antlr4 chokes before we move the generated files to generated.
rmsheep:
	rm FoxySheep*.py FoxySheep*.tokens

generated/__init__.py:
	touch generated/__init__.py