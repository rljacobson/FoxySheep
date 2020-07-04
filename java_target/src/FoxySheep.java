//import java.io.FileInputStream;
//import java.io.InputStream;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

//import org.antlr.v4.runtime.ANTLRInputStream;
import org.antlr.v4.runtime.CharStreams;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.tree.ParseTree;
import org.antlr.v4.runtime.tree.ParseTreeWalker;


public class FoxySheep {

    // Cache the utility objects.
	private static FoxySheepParser parser;
	private static FoxySheepLexer lexer;
	private static FullFormParser ff_parser;
	private static FullFormLexer ff_lexer;
	private static FullFormEmitter emitter;
	private static ParseTreeWalker walker;
	private static PostParser postParser;

	public static ParseTree postParse(ParseTree tree){
        // Reuse existing objects.
	    if(walker == null) walker = new ParseTreeWalker();
        if(postParser == null) postParser = new PostParser();

		walker.walk(postParser, tree);
		if(tree.getParent() != null){
			tree = tree.getParent();
		}
		return tree;
	}

	public static ParseTree parseTreeFromString(String input){
	    //Reuse any existing parser or lexer.
	    if(lexer == null) {
	        lexer = new FoxySheepLexer(CharStreams.fromString((input)));
        } else{
	        lexer.setInputStream(CharStreams.fromString((input)));
        }
        if(parser == null) {
	        parser = new FoxySheepParser(new CommonTokenStream(lexer));
        } else{
	        parser.setTokenStream(new CommonTokenStream(lexer));
        }

        ParseTree tree = parser.prog();
        tree = postParse(tree);
		return tree;
	}

	public static ParseTree ffParseTreeFromString(String input){
        //Reuse any existing parser or lexer.
        if(ff_lexer == null) {
            ff_lexer = new FullFormLexer(CharStreams.fromString((input)));
        } else{
            ff_lexer.setInputStream(CharStreams.fromString((input)));
        }
        if(ff_parser == null) {
            ff_parser = new FullFormParser(new CommonTokenStream(ff_lexer));
        } else{
            ff_parser.setTokenStream(new CommonTokenStream(ff_lexer));
        }

        //Parse!
        return ff_parser.prog();
	}

	public static String fullFormFromString(String input){
	    // Reuse existing emitter.
        if(emitter == null){
            emitter = new FullFormEmitter();
        }

        // Parse the input.
        ParseTree tree = parseTreeFromString(input);

        // Emit FullForm
		return emitter.visit(tree);
	}

	public static void main(String[] args) throws Exception {
        BufferedReader cin = new BufferedReader(new InputStreamReader(System.in));
        String user_in;

        // Simple REPL
        while(true){
            System.out.print("in:= ");
            user_in = cin.readLine();
            if(user_in.isEmpty()){
                break;
            }
            System.out.println(fullFormFromString(user_in));
        }
	}

}
