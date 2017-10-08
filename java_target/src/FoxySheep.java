//import java.io.FileInputStream;
//import java.io.InputStream;

//import org.antlr.v4.runtime.ANTLRInputStream;
import org.antlr.v4.runtime.CharStreams;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.ParseTreeWalker;



public class FoxySheep {

	public static void main(String[] args) throws Exception {
//		String inputFile = "/Users/rljacobson/Google Drive/Development/FoxySheep/unit_tests/ParseExpressions/SimpleAlgebraic.m";
//      CharStream input = CharStreams.fromFileName(inputFile);
		CharStream input = CharStreams.fromString("x^2-3x+4");

		//Don't use the lexer class generated from FoxySheepLexerRules.g4.
		//Use the lexer generated from FoxySheep.g4 instead.
		FoxySheepLexer lexer = new FoxySheepLexer(input);
		CommonTokenStream tokens = new CommonTokenStream(lexer);
		FoxySheepParser parser = new FoxySheepParser(tokens);
		
		//Parse the input.
		ParseTree tree = parser.prog();
		
		//Emit FullForm.
		FullFormEmitter emitter = new FullFormEmitter();
		System.out.println( emitter.visit(tree));
				
		
		//Post process the parse tree (flattens flat operators).
		ParseTreeWalker walker = new ParseTreeWalker();
		PostParser postParser = new PostParser();
		walker.walk(postParser, tree);
		//The PostParser can restructure the tree in a way that changes the root.
		if(tree.getParent() != null) tree = tree.getParent();
		
		//Emit FullForm again.
		System.out.println( emitter.visit(tree));
	}

}
