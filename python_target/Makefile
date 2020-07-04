DIR = FoxySheep/generated
FS_DIR = FoxySheep

FullForm: $(DIR)/FullFormParser.py

FoxySheep: $(DIR)/FoxySheepParser.py

run: $(DIR)/FoxySheepParser.py $(DIR)/FullFormParser.py
	python3 FoxySheep.py

# The FoxySheep Parser
$(DIR)/FoxySheepParser.py: ../FoxySheep.g4 ../FoxySheepLexerRules.g4 FoxySheep/LexerPreface.py $(DIR)/__init__.py
	antlr4 -Dlanguage=Python3 -o $(DIR) -visitor ../FoxySheep.g4
	# antlr4 does not respect the -o flag??
	mv -f $(FS_DIR)/FoxySheep.tokens $(FS_DIR)/FoxySheepLexer.py $(FS_DIR)/FoxySheepLexer.tokens $(FS_DIR)/FoxySheepListener.py $(FS_DIR)/FoxySheepParser.py $(FS_DIR)/FoxySheepVisitor.py $(DIR)
	# The last few lines below modify the generated lexer.
	# We delete the future imports of the generated file as they need to appear at the beginning of the file.
	#sed -i -e '1,3d' $(DIR)/FoxySheepLexer.py
	# macOS sed insists on making a backup that we don't want.
	#rm -f $(DIR)/FoxySheepLexer.py-e
	# Now we overwrite the generated file with a prefixed version.
	cat $(FS_DIR)/LexerPreface.py $(DIR)/FoxySheepLexer.py > tmp.py
	mv -f tmp.py $(DIR)/FoxySheepLexer.py

# The FullForm Parser
$(DIR)/FullFormParser.py: ../FullForm.g4 ../FullFormLexerRules.g4 $(DIR)/__init__.py
	antlr4 -Dlanguage=Python3 -o $(DIR) -visitor ../FullForm.g4
	# antlr4 does not respect the -o flag??
	mv -f $(FS_DIR)/FullForm.tokens $(FS_DIR)/FullFormLexer.py $(FS_DIR)/FullFormLexer.tokens $(FS_DIR)/FullFormListener.py $(FS_DIR)/FullFormParser.py $(FS_DIR)/FullFormVisitor.py $(DIR)

clean:
	rm -f $(DIR)/FoxySheep*
	rm -f $(DIR)/FullForm*
	rm -f tmp.py

# This rule is useful if antlr4 chokes before we move the generated files to generated.
rmsheep:
	rm -f FoxySheep*.py FoxySheep*.tokens
	rm -f ../FoxySheep*.py ../FoxySheep*.tokens
	rm -f $(DIR)/FoxySheep*.py $(DIR)/FoxySheep*.tokens
	rm -f $(FS_DIR)/FoxySheep*.py $(FS_DIR)/FoxySheep*.tokens

$(DIR)/__init__.py:
	touch $(DIR)/__init__.py