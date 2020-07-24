.PHONY: all check develop dist FullForm InputForm run clean rmsheep demo install uninstall rmChangeLog ChangeLog

GIT2CL ?= git2cl
GEN_DIR = FoxySheep/generated
FS_DIR = FoxySheep

all: FullForm InputForm

#: Generate the FoxySheep FullForm Parser and Lexer
FullForm: $(GEN_DIR)/FullFormParser.py $(GEN_DIR)/FullFormLexer.py

#: Generate the FoxySheep InputForm Parser and Lexer
InputForm: $(GEN_DIR)/InputFormParser.py $(GEN_DIR)/InputFormLexer.py

#: Set up to run from source code
check:
	py.test pytest

#: Set up to run from source code
develop: FullForm InputForm
	pip install -e .

#: install FoxySheep module and fox-sheep command (see also develop)
install: FullForm InputForm
	python ./setup.py install

#: remove FoxySheep module and fox-sheep command
uninstall: FullForm InputForm
	pip uninstall FoxySheep

#: Run an interactive Parser session
run: develop
	foxy-sheep

$(GEN_DIR)/InputFormParser.py $(GEN_DIR)/InputFormLexer.py: grammar/InputForm.g4 grammar/InputFormLexerRules.g4 $(GEN_DIR)/__init__.py
	(cd grammar && antlr4 -Dlanguage=Python3 -o ../$(GEN_DIR) -visitor InputForm.g4)
	# Patch the generated lexer so that it includes among other things, our LexerBase
	(cd $(GEN_DIR) && patch < InputForm.lexer.py.patch)

$(GEN_DIR)/FullFormParser.py $(GEN_DIR)/FullFormLexer.py: grammar/FullForm.g4 grammar/FullFormLexerRules.g4 $(GEN_DIR)/__init__.py
	(cd grammar && antlr4 -Dlanguage=Python3 -o ../$(GEN_DIR) -visitor FullForm.g4)
	# Patch the generated lexer so that it includes among other things, our LexerBase
	(cd $(GEN_DIR) && patch < FullForm.lexer.py.patch)

#: Remove generated files
clean: rmsheep

# This rule is useful if antlr4 chokes before we move the generated files to generated.
rmsheep:
	(cd grammar && rm -f InputForm*.py InputForm*.tokens)
	(cd $(GEN_DIR) && rm -f InputForm*.py InputForm*.tokens *.orig)

$(GEN_DIR)/__init__.py:
	touch $(GEN_DIR)/__init__.py

#: Run demo program
demo:
	python demo.py

#: Make distribution
dist:
	bash ./admin_tools/make-dist.sh

rmChangeLog:
	rm ChangeLog || true

#: Create a ChangeLog from git via git log and git2cl
ChangeLog: rmChangeLog
	git log --pretty --numstat --summary | $(GIT2CL) >$@
