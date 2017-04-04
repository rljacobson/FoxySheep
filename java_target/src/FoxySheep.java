import java.io.FileInputStream;
import java.io.InputStream;

import org.antlr.v4.runtime.ANTLRInputStream;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.ParseTreeWalker;



public class FoxySheep {

	public static void main(String[] args) throws Exception {
		String inputFile = "/Users/rljacobson/Google Drive/Development/FoxySheep/python target/Expression.txt";
		InputStream istream = new FileInputStream(inputFile);
		
		ANTLRInputStream input = new ANTLRInputStream(istream);
		//Don't use a class generated from FoxySheepLexerRules.g4.
		//Use the lexer generated from FoxySheep.g4 instead.
		FoxySheepLexer lexer = new FoxySheepLexer(input);
		CommonTokenStream tokens = new CommonTokenStream(lexer);
		FoxySheepParser parser = new FoxySheepParser(tokens);
		
		//Parse the input.
		ParseTree tree = parser.prog();
		
		//Emit FullForm.
		FullFormEmitter emitter = new FullFormEmitter();
		//System.out.println( emitter.visit(tree));
				
		
		//Post process the parse tree (flatten flat operators).
		ParseTreeWalker walker = new ParseTreeWalker();
		PostParser postParser = new PostParser();
		walker.walk(postParser, tree);
		//The PostParser can restructure the tree in a way that changes the root.
		if(tree.getParent() != null) tree = tree.getParent();
		
		//Emit FullForm again.
		System.out.println( emitter.visit(tree));
	}

}
