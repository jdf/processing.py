package jycessing.mode;

import javax.swing.text.Segment;

public class SyntaxUtilities {

  /**
   * Checks if a subregion of a <code>Segment</code> is equal to a
   * string.
   * @param text The segment
   * @param offset The offset into the segment
   * @param match The string to match
   */
  public static boolean regionMatches(final Segment text, final int offset, final String match) {
    final int length = offset + match.length();
    final char[] textArray = text.array;
    if (length > text.offset + text.count) {
      return false;
    }
    for (int i = offset, j = 0; i < length; i++, j++) {
      if (textArray[i] != match.charAt(j)) {
        return false;
      }
    }
    return true;
  }

  /**
   * Checks if a subregion of a <code>Segment</code> is equal to a
   * character array.
   * @param text The segment
   * @param offset The offset into the segment
   * @param match The character array to match
   */
  public static boolean regionMatches(final Segment text, final int offset, final char[] match) {
    final int length = offset + match.length;
    final char[] textArray = text.array;
    if (length > text.offset + text.count) {
      return false;
    }
    for (int i = offset, j = 0; i < length; i++, j++) {
      if (textArray[i] != match[j]) {
        return false;
      }
    }
    return true;
  }

}
