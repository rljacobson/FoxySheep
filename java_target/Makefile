GEN_DIR = generated
FS_DIR = src
BIN_DIR = bin
ANTLR_CLASSPATH = "/usr/local/Cellar/antlr/4.7/antlr-4.7-complete.jar"

JAVAC_OPTS = -g -verbose -classpath .:$(ANTLR_CLASSPATH) -d $(BIN_DIR)
JAVA_OPTS = -classpath bin:$(ANTLR_CLASSPATH)

run: $(BIN_DIR)/FoxySheep.class
	java $(JAVA_OPTS) FoxySheep

all: $(BIN_DIR)/FoxySheep.class

$(GEN_DIR)/FoxySheepParser.java: ../FoxySheep.g4 ../FoxySheepLexerRules.g4 $(FS_DIR)/LexerBase.java
	antlr4 -o $(GEN_DIR) -visitor ../FoxySheep.g4
	# The -o option actually doesn't work.
	mv -f *java *.tokens generated

$(BIN_DIR)/FoxySheep.class: $(GEN_DIR)/*.java $(FS_DIR)/*.java
	javac $(JAVAC_OPTS) src/*.java generated/*.java

clean:
	rm -f $(BIN_DIR)/*.class

distclean:
	rm -f $(BIN_DIR)/*.class
	rm -f $(GEN_DIR)/*.class $(GEN_DIR)/*.tokens