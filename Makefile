.PHONY: all develop FullForm FoxySheep run clean rmsheep demo install uninstall

GEN_DIR = FoxySheep/generated
FS_DIR = FoxySheep

all: FullForm FoxySheep

#: Generate the FoxySheep FullForm Parser
FullForm: $(GEN_DIR)/FullFormParser.py

#: Generate the FoxySheep Parser
FoxySheep: $(GEN_DIR)/FoxySheepParser.py

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

$(GEN_DIR)/FoxySheepParser.py: grammar/FoxySheep.g4 grammar/FoxySheepLexerRules.g4 FoxySheep/LexerPreface.py $(GEN_DIR)/__init__.py
	(cd grammar && antlr4 -Dlanguage=Python3 -o ../$(GEN_DIR) -visitor FoxySheep.g4)
	# Now we overwrite the generated file with a prefixed version.
	(cd $(GEN_DIR) && patch < FoxySheep.lexer.py.patch)

$(GEN_DIR)/FullFormParser.py: grammar/FullForm.g4 grammar/FullFormLexerRules.g4 $(GEN_DIR)/__init__.py
	(cd grammar && antlr4 -Dlanguage=Python3 -o ../$(GEN_DIR) -visitor FullForm.g4)

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
