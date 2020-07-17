# encoding: utf-8
# In order for the generated lexer to subclass our lexer base class, we
# have to patch the generated lexer using FoxySheepLexer.py.patch
#
# This is applied in the top-level Makefile. However to apply by hand run:
#    patch < FoxySheepLexer.py.patch

from FoxySheep.lexer_base import LexerBase

# Generated from FullForm.g4 by ANTLR 4.7.2
from antlr4 import ATNDeserializer, DFA, LexerATNSimulator, PredictionContextCache
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\33")
        buf.write("\u0102\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30")
        buf.write("\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36")
        buf.write("\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$\t$\4%\t%")
        buf.write("\4&\t&\3\2\6\2O\n\2\r\2\16\2P\3\2\7\2T\n\2\f\2\16\2W\13")
        buf.write("\2\3\3\3\3\5\3[\n\3\3\4\3\4\5\4_\n\4\3\5\3\5\3\6\3\6\3")
        buf.write("\7\3\7\3\7\7\7h\n\7\f\7\16\7k\13\7\3\7\7\7n\n\7\f\7\16")
        buf.write("\7q\13\7\3\7\3\7\3\7\5\7v\n\7\3\b\3\b\6\bz\n\b\r\b\16")
        buf.write("\b{\3\b\5\b\177\n\b\3\b\7\b\u0082\n\b\f\b\16\b\u0085\13")
        buf.write("\b\3\b\7\b\u0088\n\b\f\b\16\b\u008b\13\b\3\b\5\b\u008e")
        buf.write("\n\b\3\b\6\b\u0091\n\b\r\b\16\b\u0092\5\b\u0095\n\b\3")
        buf.write("\t\6\t\u0098\n\t\r\t\16\t\u0099\3\n\3\n\3\13\3\13\5\13")
        buf.write("\u00a0\n\13\3\f\3\f\5\f\u00a4\n\f\3\f\3\f\3\r\6\r\u00a9")
        buf.write("\n\r\r\r\16\r\u00aa\3\16\3\16\5\16\u00af\n\16\3\17\3\17")
        buf.write("\3\17\3\17\5\17\u00b5\n\17\3\20\3\20\3\20\3\20\3\20\3")
        buf.write("\20\3\20\3\21\3\21\3\22\3\22\3\23\3\23\3\24\3\24\7\24")
        buf.write("\u00c6\n\24\f\24\16\24\u00c9\13\24\3\24\3\24\3\24\3\24")
        buf.write("\3\25\3\25\3\26\3\26\3\27\3\27\3\30\3\30\3\30\3\31\3\31")
        buf.write("\3\31\3\32\3\32\3\32\3\33\3\33\3\34\3\34\3\35\3\35\3\36")
        buf.write("\3\36\3\37\3\37\3 \3 \3 \3!\3!\3!\3\"\3\"\3#\3#\3#\3#")
        buf.write("\3$\3$\3$\3$\3%\3%\6%\u00fa\n%\r%\16%\u00fb\3%\3%\3&\5")
        buf.write("&\u0101\n&\3\u00c7\2\'\3\3\5\2\7\2\t\2\13\2\r\4\17\5\21")
        buf.write("\6\23\2\25\2\27\7\31\2\33\2\35\2\37\2!\2#\b%\t\'\n)\13")
        buf.write("+\f-\r/\16\61\17\63\20\65\21\67\229\23;\24=\25?\26A\27")
        buf.write("C\30E\31G\32I\33K\2\3\2\13\64\2C\\c|\u00c2\u00d8\u00da")
        buf.write("\u00f8\u00fa\u0105\u0108\u0109\u010e\u0111\u0114\u0117")
        buf.write("\u011c\u012f\u0133\u0133\u0143\u0144\u0149\u014a\u0152")
        buf.write("\u0155\u015a\u0163\u0166\u0167\u0170\u0173\u017f\u0180")
        buf.write("\u0393\u03a3\u03a5\u03ab\u03b3\u03cb\u03d3\u03d4\u03d7")
        buf.write("\u03d8\u03dc\u03e3\u03f2\u03f3\u03f7\u03f7\u210c\u210e")
        buf.write("\u2112\u2115\u211d\u211e\u212a\u212a\u212e\u212f\u2131")
        buf.write("\u2133\u2135\u213a\uf6b4\uf6b7\uf6b9\uf6b9\uf6bb\uf6be")
        buf.write("\uf6c0\uf6c1\uf6c3\uf702\uf732\uf733\uf772\uf772\uf774")
        buf.write("\uf775\uf778\uf778\uf77b\uf77c\uf77f\uf782\uf784\uf78d")
        buf.write("\uf78f\uf792\uf795\uf79c\uf79e\uf7a4\uf7a6\uf7bf\uf802")
        buf.write("\uf835\ufb03\ufb04C\2&&\u00a3\u00a5\u00a7\u00a7\u00a9")
        buf.write("\u00a9\u00ab\u00ab\u00ad\u00ad\u00b0\u00b0\u00b2\u00b2")
        buf.write("\u00b7\u00b8\u00ba\u00ba\u00bd\u00bd\u00c1\u00c1\u02c9")
        buf.write("\u02c9\u02da\u02da\u2015\u2016\u2022\u2024\u2028\u2028")
        buf.write("\u2034\u2035\u2037\u2038\u2062\u2062\u20ae\u20ae\u2111")
        buf.write("\u2111\u2124\u2124\u2129\u2129\u212d\u212d\u21b7\u21b7")
        buf.write("\u2207\u2207\u2220\u2224\u22f0\u22f3\u2302\u2302\u231a")
        buf.write("\u231a\u231c\u231c\u23b6\u23b7\u2502\u2502\u2504\u2504")
        buf.write("\u25a2\u25a3\u25ac\u25ac\u25b0\u25b1\u25b4\u25b5\u25be")
        buf.write("\u25bf\u25c2\u25c2\u25c8\u25c9\u25cd\u25cd\u25d1\u25d1")
        buf.write("\u25e8\u25e8\u25fd\u25fe\u2607\u2607\u263b\u263c\u2662")
        buf.write("\u2665\u266f\u2671\u2738\u2738\uf3a2\uf3a2\uf3ba\uf3bb")
        buf.write("\uf529\uf52a\uf722\uf725\uf727\uf727\uf74b\uf74c\uf74f")
        buf.write("\uf759\uf762\uf762\uf765\uf765\uf768\uf768\uf76a\uf76e")
        buf.write("\uf7d6\uf7d6\uf802\uf835\ufe37\ufe3a\3\2\62;\4\2C\\c|")
        buf.write("\4\2$$^^\n\2$$))^^ddhhppttvv\5\2\62;CHch\4\2\13\13\17")
        buf.write("\17\t\2\"\"\u2007\u2007\u200b\u200c\u2061\u2061\u2425")
        buf.write("\u2425\uf382\uf382\uf384\uf386\2\u010c\2\3\3\2\2\2\2\r")
        buf.write("\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\27\3\2\2\2\2#\3\2")
        buf.write("\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2\2+\3\2\2\2\2-\3")
        buf.write("\2\2\2\2/\3\2\2\2\2\61\3\2\2\2\2\63\3\2\2\2\2\65\3\2\2")
        buf.write("\2\2\67\3\2\2\2\29\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2\2?\3")
        buf.write("\2\2\2\2A\3\2\2\2\2C\3\2\2\2\2E\3\2\2\2\2G\3\2\2\2\2I")
        buf.write("\3\2\2\2\3N\3\2\2\2\5Z\3\2\2\2\7^\3\2\2\2\t`\3\2\2\2\13")
        buf.write("b\3\2\2\2\ru\3\2\2\2\17w\3\2\2\2\21\u0097\3\2\2\2\23\u009b")
        buf.write("\3\2\2\2\25\u009f\3\2\2\2\27\u00a1\3\2\2\2\31\u00a8\3")
        buf.write("\2\2\2\33\u00ae\3\2\2\2\35\u00b4\3\2\2\2\37\u00b6\3\2")
        buf.write("\2\2!\u00bd\3\2\2\2#\u00bf\3\2\2\2%\u00c1\3\2\2\2\'\u00c3")
        buf.write("\3\2\2\2)\u00ce\3\2\2\2+\u00d0\3\2\2\2-\u00d2\3\2\2\2")
        buf.write("/\u00d4\3\2\2\2\61\u00d7\3\2\2\2\63\u00da\3\2\2\2\65\u00dd")
        buf.write("\3\2\2\2\67\u00df\3\2\2\29\u00e1\3\2\2\2;\u00e3\3\2\2")
        buf.write("\2=\u00e5\3\2\2\2?\u00e7\3\2\2\2A\u00ea\3\2\2\2C\u00ed")
        buf.write("\3\2\2\2E\u00ef\3\2\2\2G\u00f3\3\2\2\2I\u00f9\3\2\2\2")
        buf.write("K\u0100\3\2\2\2MO\5\7\4\2NM\3\2\2\2OP\3\2\2\2PN\3\2\2")
        buf.write("\2PQ\3\2\2\2QU\3\2\2\2RT\5\5\3\2SR\3\2\2\2TW\3\2\2\2U")
        buf.write("S\3\2\2\2UV\3\2\2\2V\4\3\2\2\2WU\3\2\2\2X[\5\7\4\2Y[\5")
        buf.write("\23\n\2ZX\3\2\2\2ZY\3\2\2\2[\6\3\2\2\2\\_\5\t\5\2]_\5")
        buf.write("\13\6\2^\\\3\2\2\2^]\3\2\2\2_\b\3\2\2\2`a\t\2\2\2a\n\3")
        buf.write("\2\2\2bc\t\3\2\2c\f\3\2\2\2de\5\21\t\2ei\5C\"\2fh\5\23")
        buf.write("\n\2gf\3\2\2\2hk\3\2\2\2ig\3\2\2\2ij\3\2\2\2jv\3\2\2\2")
        buf.write("ki\3\2\2\2ln\5\23\n\2ml\3\2\2\2nq\3\2\2\2om\3\2\2\2op")
        buf.write("\3\2\2\2pr\3\2\2\2qo\3\2\2\2rs\5C\"\2st\5\21\t\2tv\3\2")
        buf.write("\2\2ud\3\2\2\2uo\3\2\2\2v\16\3\2\2\2w\u0094\5? \2xz\5")
        buf.write("\25\13\2yx\3\2\2\2z{\3\2\2\2{y\3\2\2\2{|\3\2\2\2|~\3\2")
        buf.write("\2\2}\177\5C\"\2~}\3\2\2\2~\177\3\2\2\2\177\u0083\3\2")
        buf.write("\2\2\u0080\u0082\5\25\13\2\u0081\u0080\3\2\2\2\u0082\u0085")
        buf.write("\3\2\2\2\u0083\u0081\3\2\2\2\u0083\u0084\3\2\2\2\u0084")
        buf.write("\u0095\3\2\2\2\u0085\u0083\3\2\2\2\u0086\u0088\5\25\13")
        buf.write("\2\u0087\u0086\3\2\2\2\u0088\u008b\3\2\2\2\u0089\u0087")
        buf.write("\3\2\2\2\u0089\u008a\3\2\2\2\u008a\u008d\3\2\2\2\u008b")
        buf.write("\u0089\3\2\2\2\u008c\u008e\5C\"\2\u008d\u008c\3\2\2\2")
        buf.write("\u008d\u008e\3\2\2\2\u008e\u0090\3\2\2\2\u008f\u0091\5")
        buf.write("\25\13\2\u0090\u008f\3\2\2\2\u0091\u0092\3\2\2\2\u0092")
        buf.write("\u0090\3\2\2\2\u0092\u0093\3\2\2\2\u0093\u0095\3\2\2\2")
        buf.write("\u0094y\3\2\2\2\u0094\u0089\3\2\2\2\u0095\20\3\2\2\2\u0096")
        buf.write("\u0098\5\23\n\2\u0097\u0096\3\2\2\2\u0098\u0099\3\2\2")
        buf.write("\2\u0099\u0097\3\2\2\2\u0099\u009a\3\2\2\2\u009a\22\3")
        buf.write("\2\2\2\u009b\u009c\t\4\2\2\u009c\24\3\2\2\2\u009d\u00a0")
        buf.write("\5\23\n\2\u009e\u00a0\t\5\2\2\u009f\u009d\3\2\2\2\u009f")
        buf.write("\u009e\3\2\2\2\u00a0\26\3\2\2\2\u00a1\u00a3\59\35\2\u00a2")
        buf.write("\u00a4\5\31\r\2\u00a3\u00a2\3\2\2\2\u00a3\u00a4\3\2\2")
        buf.write("\2\u00a4\u00a5\3\2\2\2\u00a5\u00a6\59\35\2\u00a6\30\3")
        buf.write("\2\2\2\u00a7\u00a9\5\33\16\2\u00a8\u00a7\3\2\2\2\u00a9")
        buf.write("\u00aa\3\2\2\2\u00aa\u00a8\3\2\2\2\u00aa\u00ab\3\2\2\2")
        buf.write("\u00ab\32\3\2\2\2\u00ac\u00af\n\6\2\2\u00ad\u00af\5\35")
        buf.write("\17\2\u00ae\u00ac\3\2\2\2\u00ae\u00ad\3\2\2\2\u00af\34")
        buf.write("\3\2\2\2\u00b0\u00b1\5=\37\2\u00b1\u00b2\t\7\2\2\u00b2")
        buf.write("\u00b5\3\2\2\2\u00b3\u00b5\5\37\20\2\u00b4\u00b0\3\2\2")
        buf.write("\2\u00b4\u00b3\3\2\2\2\u00b5\36\3\2\2\2\u00b6\u00b7\5")
        buf.write("=\37\2\u00b7\u00b8\5;\36\2\u00b8\u00b9\5!\21\2\u00b9\u00ba")
        buf.write("\5!\21\2\u00ba\u00bb\5!\21\2\u00bb\u00bc\5!\21\2\u00bc")
        buf.write(" \3\2\2\2\u00bd\u00be\t\b\2\2\u00be\"\3\2\2\2\u00bf\u00c0")
        buf.write("\7-\2\2\u00c0$\3\2\2\2\u00c1\u00c2\7/\2\2\u00c2&\3\2\2")
        buf.write("\2\u00c3\u00c7\5/\30\2\u00c4\u00c6\13\2\2\2\u00c5\u00c4")
        buf.write("\3\2\2\2\u00c6\u00c9\3\2\2\2\u00c7\u00c8\3\2\2\2\u00c7")
        buf.write("\u00c5\3\2\2\2\u00c8\u00ca\3\2\2\2\u00c9\u00c7\3\2\2\2")
        buf.write("\u00ca\u00cb\5\61\31\2\u00cb\u00cc\3\2\2\2\u00cc\u00cd")
        buf.write("\b\24\2\2\u00cd(\3\2\2\2\u00ce\u00cf\7]\2\2\u00cf*\3\2")
        buf.write("\2\2\u00d0\u00d1\7_\2\2\u00d1,\3\2\2\2\u00d2\u00d3\7.")
        buf.write("\2\2\u00d3.\3\2\2\2\u00d4\u00d5\7*\2\2\u00d5\u00d6\7,")
        buf.write("\2\2\u00d6\60\3\2\2\2\u00d7\u00d8\7,\2\2\u00d8\u00d9\7")
        buf.write("+\2\2\u00d9\62\3\2\2\2\u00da\u00db\7b\2\2\u00db\u00dc")
        buf.write("\7b\2\2\u00dc\64\3\2\2\2\u00dd\u00de\7b\2\2\u00de\66\3")
        buf.write("\2\2\2\u00df\u00e0\7)\2\2\u00e08\3\2\2\2\u00e1\u00e2\7")
        buf.write("$\2\2\u00e2:\3\2\2\2\u00e3\u00e4\7<\2\2\u00e4<\3\2\2\2")
        buf.write("\u00e5\u00e6\7^\2\2\u00e6>\3\2\2\2\u00e7\u00e8\7`\2\2")
        buf.write("\u00e8\u00e9\7`\2\2\u00e9@\3\2\2\2\u00ea\u00eb\7,\2\2")
        buf.write("\u00eb\u00ec\7`\2\2\u00ecB\3\2\2\2\u00ed\u00ee\7\60\2")
        buf.write("\2\u00eeD\3\2\2\2\u00ef\u00f0\7\f\2\2\u00f0\u00f1\3\2")
        buf.write("\2\2\u00f1\u00f2\b#\2\2\u00f2F\3\2\2\2\u00f3\u00f4\7\uf3b3")
        buf.write("\2\2\u00f4\u00f5\3\2\2\2\u00f5\u00f6\b$\2\2\u00f6H\3\2")
        buf.write("\2\2\u00f7\u00fa\t\t\2\2\u00f8\u00fa\5K&\2\u00f9\u00f7")
        buf.write("\3\2\2\2\u00f9\u00f8\3\2\2\2\u00fa\u00fb\3\2\2\2\u00fb")
        buf.write("\u00f9\3\2\2\2\u00fb\u00fc\3\2\2\2\u00fc\u00fd\3\2\2\2")
        buf.write("\u00fd\u00fe\b%\2\2\u00feJ\3\2\2\2\u00ff\u0101\t\n\2\2")
        buf.write("\u0100\u00ff\3\2\2\2\u0101L\3\2\2\2\33\2PUZ^iou{~\u0083")
        buf.write("\u0089\u008d\u0092\u0094\u0099\u009f\u00a3\u00aa\u00ae")
        buf.write("\u00b4\u00c7\u00f9\u00fb\u0100\3\b\2\2")
        return buf.getvalue()


class FullFormLexer(LexerBase):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    Name = 1
    DecimalNumber = 2
    NumberInBase = 3
    DIGITS = 4
    StringLiteral = 5
    PLUS = 6
    MINUS = 7
    COMMENT = 8
    LBRACKET = 9
    RBRACKET = 10
    COMMA = 11
    LCOMMENT = 12
    RCOMMENT = 13
    DOUBLEBACKQUOTE = 14
    BACKQUOTE = 15
    SINGLEQUOTE = 16
    QUOTE = 17
    RAWCOLON = 18
    RAWBACKSLASH = 19
    DOUBLECARET = 20
    ASTERISKCARET = 21
    DOT = 22
    NEWLINE = 23
    CONTINUATION = 24
    WHITESPACE = 25

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'+'", "'-'", "'['", "']'", "','", "'(*'", "'*)'", "'``'", "'`'",
            "'''", "'\"'", "':'", "'\\'", "'^^'", "'*^'", "'.'", "'\n'",
            "'\uF3B1'" ]

    symbolicNames = [ "<INVALID>",
            "Name", "DecimalNumber", "NumberInBase", "DIGITS", "StringLiteral",
            "PLUS", "MINUS", "COMMENT", "LBRACKET", "RBRACKET", "COMMA",
            "LCOMMENT", "RCOMMENT", "DOUBLEBACKQUOTE", "BACKQUOTE", "SINGLEQUOTE",
            "QUOTE", "RAWCOLON", "RAWBACKSLASH", "DOUBLECARET", "ASTERISKCARET",
            "DOT", "NEWLINE", "CONTINUATION", "WHITESPACE" ]

    ruleNames = [ "Name", "LetterFormOrDigit", "LetterForm", "Letter", "Letterlike",
                  "DecimalNumber", "NumberInBase", "DIGITS", "DIGIT", "DigitInAnyBase",
                  "StringLiteral", "StringCharacters", "StringCharacter",
                  "EscapeSequence", "UnicodeEscape", "HexDigit", "PLUS",
                  "MINUS", "COMMENT", "LBRACKET", "RBRACKET", "COMMA", "LCOMMENT",
                  "RCOMMENT", "DOUBLEBACKQUOTE", "BACKQUOTE", "SINGLEQUOTE",
                  "QUOTE", "RAWCOLON", "RAWBACKSLASH", "DOUBLECARET", "ASTERISKCARET",
                  "DOT", "NEWLINE", "CONTINUATION", "WHITESPACE", "SpaceCharacter" ]

    grammarFileName = "FullForm.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None
