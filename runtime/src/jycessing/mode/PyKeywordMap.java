package jycessing.mode;

import javax.swing.text.Segment;

import processing.app.syntax.Token;

public class PyKeywordMap {
  private final Keyword[] map;

  /**
   * Creates a new <code>KeywordMap</code>.
   * @param ignoreCase True if keys are case insensitive
   */
  public PyKeywordMap() {
    this(52);
  }

  /**
   * Creates a new <code>KeywordMap</code>.
   * @param ignoreCase True if the keys are case insensitive
   * @param mapLength The number of `buckets' to create.
   * A value of 52 will give good performance for most maps.
   */
  public PyKeywordMap(int mapLength) {
    this.mapLength = mapLength;
    map = new Keyword[mapLength];
  }

  /**
   * Looks up a key.
   * @param text The text segment
   * @param offset The offset of the substring within the text segment
   * @param length The length of the substring
   */
  public byte lookup(Segment text, int offset, int length) {
    if (length == 0) {
      return Token.NULL;
    }
    Keyword k = map[getSegmentMapKey(text, offset, length)];
    while (k != null) {
      if (length != k.keyword.length) {
        k = k.next;
        continue;
      }
      if (SyntaxUtilities.regionMatches(text, offset, k.keyword)) {
        return k.id;
      }
      k = k.next;
    }
    return Token.NULL;
  }

  /**
   * Adds a key-value mapping.
   * @param keyword The key
   * @Param id The value
   */
  public void add(String keyword, byte id) {
    int key = getStringMapKey(keyword);
    map[key] = new Keyword(keyword.toCharArray(), id, map[key]);
  }

  // protected members
  protected int mapLength;

  protected int getStringMapKey(String s) {
    return (Character.toUpperCase(s.charAt(0)) + Character.toUpperCase(s.charAt(s.length() - 1)))
        % mapLength;
  }

  protected int getSegmentMapKey(Segment s, int off, int len) {
    return (Character.toUpperCase(s.array[off]) + Character.toUpperCase(s.array[off + len - 1]))
        % mapLength;
  }

  // private members
  class Keyword {
    public Keyword(char[] keyword, byte id, Keyword next) {
      this.keyword = keyword;
      this.id = id;
      this.next = next;
    }

    public char[] keyword;
    public byte id;
    public Keyword next;
  }

}
