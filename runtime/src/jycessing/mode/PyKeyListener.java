package jycessing.mode;

import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.KeyEvent;
import java.util.Stack;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import processing.app.Editor;
import processing.app.Sketch;
import processing.app.syntax.JEditTextArea;
import processing.mode.java.PdeKeyListener;

/**
 * This class provides Pythonic handling of TAB, BACKSPACE, and ENTER keys.
 */
public class PyKeyListener extends PdeKeyListener {
  final PyEditor pyEditor;
  final JEditTextArea textArea;

  // ctrl-alt on windows & linux, cmd-alt on os x
  private static int CTRL_ALT = ActionEvent.ALT_MASK
      | Toolkit.getDefaultToolkit().getMenuShortcutKeyMask();

  // 4 spaces per pep8
  private static final String TAB = "    ";
  private static final int TAB_SIZE = TAB.length();

  public PyKeyListener(final Editor editor, final JEditTextArea textarea) {
    super(editor, textarea);

    pyEditor = (PyEditor)editor;
    textArea = textarea;
  }

  @Override
  public boolean keyPressed(final KeyEvent event) {
    final char c = event.getKeyChar();
    final int code = event.getKeyCode();
    final int mods = event.getModifiers();

    final Sketch sketch = pyEditor.getSketch();

    // things that change the content of the text area
    if ((code == KeyEvent.VK_BACK_SPACE) || (code == KeyEvent.VK_TAB)
        || (code == KeyEvent.VK_ENTER) || (mods == 0 && c >= 32 && c < 128)) {
      sketch.setModified(true);
    }

    if (event.isMetaDown() && code == KeyEvent.VK_UP) {
      textArea.setCaretPosition(0);
      textArea.scrollToCaret();
      return true;
    }

    if (event.isMetaDown() && code == KeyEvent.VK_DOWN) {
      textArea.setCaretPosition(textArea.getDocumentLength());
      textArea.scrollToCaret();
      return true;
    }

    // ctrl-alt-[arrow] switches sketch tab
    if ((mods & CTRL_ALT) == CTRL_ALT) {
      if (code == KeyEvent.VK_LEFT) {
        sketch.handlePrevCode();
        return true;
      } else if (code == KeyEvent.VK_RIGHT) {
        sketch.handleNextCode();
        return true;
      }
    }

    final int thisLine = textArea.getCaretLine();
    final int thisPos = textArea.getCaretPosition();

    switch (code) {
      case KeyEvent.VK_BACK_SPACE:
        if (thisPos == textArea.getLineStartOffset(thisLine)) {
          // Let the user backspace onto the previous line.
          break;
        }
        final LineInfo currentLine = new LineInfo(thisLine);
        if (currentLine.caretInText) {
          // The caret is in the text; let the text editor handle this backspace.
          break;
        }
        // The caret is not in the text; treat it as a request to unindent.
        indent(-1);
        return true;

      case KeyEvent.VK_ESCAPE:
        textArea.selectNone();
        pyEditor.handleStop();
        return true;

      case KeyEvent.VK_TAB:
        indent(event.isShiftDown() ? -1 : 1);
        return true;

      case KeyEvent.VK_ENTER: // return
        final String text = textArea.getText(); // text
        textArea.setSelectedText(newline());
        break;
    }

    return false;
  }

  /**
   * A line is some whitespace followed by a bunch of whatever.
   */
  private static final Pattern LINE = Pattern.compile("^(\\s*)(.*)$");

  /**
   * Everything we need to know about a line in the text editor.
   */
  private class LineInfo {
    public final int lineNumber;

    // Expressed in units of "python indents", not in number of spaces.
    public final int indent;

    // The text content after whatever indent.
    public final String text;

    // Whether or not the caret happens to be positioned in the text portion of the line.
    public final boolean caretInText;

    LineInfo(final int lineNumber) {
      this.lineNumber = lineNumber;

      final Matcher m = LINE.matcher(textArea.getLineText(lineNumber));
      if (!m.matches()) {
        throw new AssertionError("How can a line have less than nothing in it?");
      }
      final String space = m.group(1);
      text = m.group(2);
      final int caretLinePos =
          textArea.getCaretPosition() - textArea.getLineStartOffset(lineNumber);
      caretInText = caretLinePos > space.length();
      // Calculate the current indent measured in tab stops of TAB_SIZE spaces.
      int currentIndent = 0;
      int spaceCounter = 0;
      for (int i = 0; i < space.length(); i++) {
        spaceCounter++;
        // A literal tab character advances to the next tab stop, as does the TAB_SIZEth space
        // character in a row.
        if (spaceCounter % TAB_SIZE == 0 || space.charAt(i) == '\t') {
          currentIndent++;
          spaceCounter = 0;
        }
      }
      indent = currentIndent;
    }

    @Override
    public String toString() {
      return String.format("<Line %d, indent %d, {%s}>", lineNumber, indent, text);
    }
  }

  /**
   * Maybe change the indent of the current selection. If sign is positive, then increase the
   * indent; otherwise, decrease it.
   * <p>If the last non-comment, non-blank line ends with ":", then the maximum indent for the
   * current line is one greater than the indent of that ":"-bearing line. Otherwise, the maximum
   * indent is equal to the indent of the last non-comment line.
   * <p>The minimum indent is 0.
   * @param sign The direction in which to modify the indent of the current line.
   */
  public void indent(final int sign) {
    final int startLine = textArea.getSelectionStartLine();
    final int stopLine = textArea.getSelectionStopLine();
    final int selectionStart = textArea.getSelectionStart();
    final int selectionStop = textArea.getSelectionStop();

    final LineInfo currentLine = new LineInfo(startLine);
    final int currentCaret = textArea.getCaretPosition();
    final int startLineEndRelativePos = textArea.getLineStopOffset(startLine) - selectionStart;
    final int stopLineEndRelativePos = textArea.getLineStopOffset(stopLine) - selectionStop;
    final int newIndent;

    if (sign > 0) {
      // Find previous non-blank non-comment line.
      LineInfo candidate = null;
      for (int i = startLine - 1; i >= 0; i--) {
        candidate = new LineInfo(i);
        if (candidate.text.length() > 0 && !candidate.text.startsWith("#")) {
          break;
        }
      }
      if (candidate == null) {
        newIndent = 0;
      } else {
        final String trimmed = candidate.text.trim();
        if (trimmed.endsWith(":") || trimmed.endsWith("(")) {
          newIndent = Math.min(candidate.indent + 1, currentLine.indent + 1);
        } else {
          newIndent = Math.min(candidate.indent, currentLine.indent + 1);
        }
      }
    } else {
      newIndent = Math.max(0, currentLine.indent - 1);
    }
    final int deltaIndent = newIndent - currentLine.indent;
    for (int i = startLine; i <= stopLine; i++) {
      indentLineBy(i, deltaIndent);
    }
    textArea.setSelectionStart(getAbsoluteCaretPositionRelativeToLineEnd(startLine,
        startLineEndRelativePos));
    textArea.setSelectionEnd(getAbsoluteCaretPositionRelativeToLineEnd(stopLine,
        stopLineEndRelativePos));
  }

  private int getAbsoluteCaretPositionRelativeToLineEnd(final int line,
      final int lineEndRelativePosition) {
    return Math.max(textArea.getLineStopOffset(line) - lineEndRelativePosition,
        textArea.getLineStartOffset(line));
  }

  private void indentLineBy(final int line, final int deltaIndent) {
    final LineInfo currentLine = new LineInfo(line);
    final int newIndent = Math.max(0, currentLine.indent + deltaIndent);

    final StringBuilder sb = new StringBuilder();
    for (int i = 0; i < newIndent; i++) {
      sb.append(TAB);
    }
    sb.append(currentLine.text);
    textArea.select(textArea.getLineStartOffset(line), textArea.getLineStopOffset(line) - 1);
    final String newLine = sb.toString();
    textArea.setSelectedText(newLine);
    textArea.selectNone();
  }

  private static final Pattern INITIAL_WHITESPACE = Pattern.compile("^(\\s*)");
  /*
   * This can be fooled by a line like
   * print "He said: #LOLHASHTAG!"
   */
  private static final Pattern TERMINAL_COLON = Pattern.compile(":\\s*(#.*)?$");
  private static final Pattern POP_CONTEXT = Pattern.compile("^\\s*(return|break|continue)\\b");

  private boolean isOpen(final char c) {
    return c == '(' || c == '[' || c == '{';
  }

  private boolean isClose(final char c) {
    return c == ')' || c == ']' || c == '}';
  }

  /**
   * Search for an unterminated paren or bracket. If found, return
   * its index in the given text. Otherwise return -1.
   * <p>Ignores syntax errors, treating (foo] as a valid construct.
   * <p>Assumes that the text contains no surrogate characters.
   * @param cursor The current cursor position in the given text.
   * @param text The text to search for an unterminated paren or bracket.
   * @return The index of the unterminated paren, or -1.
   */
  private int indexOfUnclosedParen() {
    final int cursor = textArea.getCaretPosition();
    final String text = textArea.getText();
    final Stack<Integer> stack = new Stack<Integer>();
    int column = 0;
    for (int i = 0; i < cursor; i++) {
      final char c = text.charAt(i);
      if (isOpen(c)) {
        stack.push(column);
      } else if (isClose(c)) {
        if (stack.size() == 0) {
          // Syntax error; bail.
          return -1;
        }
        stack.pop();
      }

      if (c == '\n') {
        column = 0;
      } else {
        column++;
      }
    }
    return stack.size() > 0 ? stack.pop() : -1;
  }

  private String indentOf(final String line) {
    final Matcher m = INITIAL_WHITESPACE.matcher(line);
    if (!m.find()) {
      throw new AssertionError("How can there be nothing?");
    }
    return m.group();
  }

  private String getInitialWhitespace() {
    final String text = textArea.getText();
    final int cursor = textArea.getCaretPosition();
    final int lineNumber = textArea.getLineOfOffset(cursor);
    final int lineStart = textArea.getLineStartOffset(lineNumber);
    final int lineEnd = textArea.getLineStopOffset(lineNumber);
    final String line = textArea.getLineText(lineNumber);

    final String defaultIndent = indentOf(line);

    // Search for an unmatched closing paren on this line.
    int balance = 0;
    for (int i = cursor - 1; i >= lineStart; i--) {
      if (isClose(text.charAt(i))) {
        balance++;
      } else if (isOpen(text.charAt(i))) {
        balance--;
      }
    }
    if (balance == 0) {
      return defaultIndent;
    }
    if (balance > 0) {
      int index = lineStart - 1;
      while (balance > 0 && index >= 0) {
        if (isClose(text.charAt(index))) {
          balance++;
        } else if (isOpen(text.charAt(index))) {
          balance--;
        }
        index--;
      }
      if (balance != 0) {
        // Syntax error
        return defaultIndent;
      }
      return indentOf(textArea.getLineText(textArea.getLineOfOffset(index)));
    }
    final int parenColumn = indexOfUnclosedParen();
    if (parenColumn > -1) {
      return nSpaces(parenColumn + 1);
    }
    return defaultIndent;
  }

  private String newline() {
    final int cursor = textArea.getCaretPosition();

    if (cursor <= 1) {
      return "\n";
    }

    final int lineNumber = textArea.getLineOfOffset(cursor);
    final int lineStart = textArea.getLineStartOffset(lineNumber);
    final String line = textArea.getLineText(lineNumber);
    final String initialWhitespace = getInitialWhitespace();

    final String lineTextBeforeCursor = line.substring(0, cursor - lineStart);
    if (Pattern.matches("\\s*", lineTextBeforeCursor)) {
      return "\n" + initialWhitespace;
    }

    if (TERMINAL_COLON.matcher(line).find()) {
      return "\n" + initialWhitespace + TAB;
    }
    // TODO: popping context on return should return to the indent of the last def.
    if (POP_CONTEXT.matcher(line).find()) {
      final int currentIndentLength = initialWhitespace.length();
      final int spaceCount = Math.max(0, currentIndentLength - 4);
      return "\n" + nSpaces(spaceCount);
    }
    return "\n" + initialWhitespace;
  }

  private static final String nSpaces(final int n) {
    final StringBuilder sb = new StringBuilder(n);
    for (int i = 0; i < n; i++) {
      sb.append(' ');
    }
    return sb.toString();
  }
}
