.PHONY: all develop dist FullForm FoxySheep run clean rmsheep demo install uninstall rmChangeLog ChangeLog

GIT2CL ?= git2cl
GEN_DIR = FoxySheep/generated
FS_DIR = FoxySheep

all: FullForm FoxySheep

#: Generate the FoxySheep FullForm Parser and Lexer
FullForm: $(GEN_DIR)/FullFormParser.py $(GEN_DIR)/FullFormLexer.py

#: Generate the FoxySheep Parser and Lexer
FoxySheep: $(GEN_DIR)/FoxySheepParser.py $(GEN_DIR)/FoxySheepLexer.py

#: Set up to run from source code
develop: FullForm FoxySheep
	pip install -e .

#: install FoxySheep module and fox-sheep command (see also develop)
install: FullForm FoxySheep
	python ./setup.py install

#: remove FoxySheep module and fox-sheep command
uninstall: FullForm FoxySheep
	pip uninstall FoxySheep

#: Run an interactive Parser session
run: develop
	foxy-sheep

$(GEN_DIR)/FoxySheepParser.py $(GEN_DIR)/FoxySheepLexer.py: grammar/FoxySheep.g4 grammar/FoxySheepLexerRules.g4 $(GEN_DIR)/__init__.py
	(cd grammar && antlr4 -Dlanguage=Python3 -o ../$(GEN_DIR) -visitor FoxySheep.g4)
	# Patch the generated lexer so that it includes among other things, our LexerBase
	(cd $(GEN_DIR) && patch < FoxySheep.lexer.py.patch)

$(GEN_DIR)/FullFormParser.py $(GEN_DIR)/FullFormLexer.py: grammar/FullForm.g4 grammar/FullFormLexerRules.g4 $(GEN_DIR)/__init__.py
	(cd grammar && antlr4 -Dlanguage=Python3 -o ../$(GEN_DIR) -visitor FullForm.g4)
	# Patch the generated lexer so that it includes among other things, our LexerBase
	(cd $(GEN_DIR) && patch < FullForm.lexer.py.patch)

#: Remove generated files
clean: rmsheep

# This rule is useful if antlr4 chokes before we move the generated files to generated.
rmsheep:
	rm -f FoxySheep*.py FoxySheep*.tokens
	rm -f grammar/FoxySheep*.py grammar/FoxySheep*.tokens
	rm -f $(GEN_DIR)/FoxySheep*.py $(GEN_DIR)/FoxySheep*.tokens
	rm -f $(FS_DIR)/FoxySheep*.py $(FS_DIR)/FoxySheep*.tokens

$(GEN_DIR)/__init__.py:
	touch $(GEN_DIR)/__init__.py

#: Run demo program
demo:
	python demo.py

#: Make distribution
dist:
	python setup.py bdist_egg bdist_wheel

rmChangeLog:
	rm ChangeLog || true

#: Create a ChangeLog from git via git log and git2cl
ChangeLog: rmChangeLog
	git log --pretty --numstat --summary | $(GIT2CL) >$@
