package jycessing.mode;

import javax.swing.text.Segment;

import processing.app.syntax.Token;
import processing.app.syntax.TokenMarker;

public class PythonTokenMarker extends TokenMarker {
  private static final byte TRIPLEQUOTE1 = Token.INTERNAL_FIRST;
  private static final byte TRIPLEQUOTE2 = Token.INTERNAL_LAST;

  private static PyKeywordMap pyKeywords;

  private final PyKeywordMap keywords;
  private int lastOffset;
  private int lastKeyword;

  public PythonTokenMarker() {
    this.keywords = getKeywords();
  }

  @Override
  public void addColoring(final String keyword, final String coloring) {
    // KEYWORD1 -> 0, KEYWORD2 -> 1, etc
    final int num = coloring.charAt(coloring.length() - 1) - '1';
    int id = 0;
    boolean paren = false;
    switch (coloring.charAt(0)) {
      case 'K':
        id = Token.KEYWORD1 + num;
        break;
      case 'L':
        id = Token.LITERAL1 + num;
        break;
      case 'F':
        id = Token.FUNCTION1 + num;
        paren = true;
        break;
    }
    keywords.add(keyword, (byte)id);
  }

  @Override
  public byte markTokensImpl(byte token, final Segment line, final int lineIndex) {
    final char[] array = line.array;
    final int offset = line.offset;
    lastOffset = offset;
    lastKeyword = offset;
    final int length = line.count + offset;
    boolean backslash = false;

    loop: for (int i = offset; i < length; i++) {
      final int i1 = (i + 1);

      final char c = array[i];
      if (c == '\\') {
        backslash = !backslash;
        continue;
      }

      switch (token) {
        case Token.NULL:
          switch (c) {
            case '#':
              if (backslash) {
                backslash = false;
              } else {
                doKeyword(line, i, c);
                addToken(i - lastOffset, token);
                addToken(length - i, Token.COMMENT1);
                lastOffset = lastKeyword = length;
                break loop;
              }
              break;
            case '"':
              doKeyword(line, i, c);
              if (backslash) {
                backslash = false;
              } else {
                addToken(i - lastOffset, token);
                if (SyntaxUtilities.regionMatches(line, i1, "\"\"")) {
                  token = TRIPLEQUOTE1;
                } else {
                  token = Token.LITERAL1;
                }
                lastOffset = lastKeyword = i;
              }
              break;
            case '\'':
              doKeyword(line, i, c);
              if (backslash) {
                backslash = false;
              } else {
                addToken(i - lastOffset, token);
                if (SyntaxUtilities.regionMatches(line, i1, "''")) {
                  token = TRIPLEQUOTE2;
                } else {
                  token = Token.LITERAL2;
                }
                lastOffset = lastKeyword = i;
              }
              break;
            default:
              backslash = false;
              if (!Character.isLetterOrDigit(c) && c != '_') {
                doKeyword(line, i, c);
              }
              break;
          }
          break;
        case Token.LITERAL1:
          if (backslash) {
            backslash = false;
          } else if (c == '"') {
            addToken(i1 - lastOffset, token);
            token = Token.NULL;
            lastOffset = lastKeyword = i1;
          }
          break;
        case Token.LITERAL2:
          if (backslash) {
            backslash = false;
          } else if (c == '\'') {
            addToken(i1 - lastOffset, Token.LITERAL1);
            token = Token.NULL;
            lastOffset = lastKeyword = i1;
          }
          break;
        case TRIPLEQUOTE1:
          if (backslash) {
            backslash = false;
          } else if (SyntaxUtilities.regionMatches(line, i, "\"\"\"")) {
            addToken((i += 3) - lastOffset, Token.LITERAL1);
            token = Token.NULL;
            lastOffset = lastKeyword = i;
          }
          break;
        case TRIPLEQUOTE2:
          if (backslash) {
            backslash = false;
          } else if (SyntaxUtilities.regionMatches(line, i, "'''")) {
            addToken((i += 3) - lastOffset, Token.LITERAL1);
            token = Token.NULL;
            lastOffset = lastKeyword = i;
          }
          break;
        default:
          throw new InternalError("Invalid state: " + token);
      }
    }

    switch (token) {
      case TRIPLEQUOTE1:
      case TRIPLEQUOTE2:
        addToken(length - lastOffset, Token.LITERAL1);
        break;
      case Token.NULL:
        doKeyword(line, length, '\0');
        //$FALL-THROUGH$
      default:
        addToken(length - lastOffset, token);
        break;
    }

    return token;
  }

  public static PyKeywordMap getKeywords() {
    if (pyKeywords == null) {
      pyKeywords = new PyKeywordMap();
      pyKeywords.add("and", Token.KEYWORD3);
      pyKeywords.add("not", Token.KEYWORD3);
      pyKeywords.add("or", Token.KEYWORD3);
      pyKeywords.add("if", Token.KEYWORD1);
      pyKeywords.add("for", Token.KEYWORD1);
      pyKeywords.add("assert", Token.KEYWORD1);
      pyKeywords.add("break", Token.KEYWORD1);
      pyKeywords.add("continue", Token.KEYWORD1);
      pyKeywords.add("elif", Token.KEYWORD1);
      pyKeywords.add("else", Token.KEYWORD1);
      pyKeywords.add("except", Token.KEYWORD1);
      pyKeywords.add("exec", Token.KEYWORD1);
      pyKeywords.add("finally", Token.KEYWORD1);
      pyKeywords.add("raise", Token.KEYWORD1);
      pyKeywords.add("return", Token.KEYWORD1);
      pyKeywords.add("try", Token.KEYWORD1);
      pyKeywords.add("while", Token.KEYWORD1);
      pyKeywords.add("def", Token.KEYWORD2);
      pyKeywords.add("class", Token.KEYWORD2);
      pyKeywords.add("del", Token.KEYWORD2);
      pyKeywords.add("from", Token.KEYWORD2);
      pyKeywords.add("global", Token.KEYWORD2);
      pyKeywords.add("import", Token.KEYWORD2);
      pyKeywords.add("in", Token.KEYWORD2);
      pyKeywords.add("is", Token.KEYWORD2);
      pyKeywords.add("lambda", Token.KEYWORD2);
      pyKeywords.add("pass", Token.KEYWORD2);
      pyKeywords.add("print", Token.KEYWORD2);
    }
    return pyKeywords;
  }

  private boolean doKeyword(final Segment line, final int i, final char c) {
    final int i1 = i + 1;

    final int len = i - lastKeyword;
    final byte id = keywords.lookup(line, lastKeyword, len);
    if (id != Token.NULL) {
      if (lastKeyword != lastOffset) {
        addToken(lastKeyword - lastOffset, Token.NULL);
      }
      addToken(len, id);
      lastOffset = i;
    }
    lastKeyword = i1;
    return false;
  }
}
