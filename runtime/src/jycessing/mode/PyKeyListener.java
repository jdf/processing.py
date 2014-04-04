package jycessing.mode;

import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.KeyEvent;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import processing.app.Editor;
import processing.app.Sketch;
import processing.app.syntax.JEditTextArea;
import processing.mode.java.PdeKeyListener;

/**
 * 
 */
public class PyKeyListener extends PdeKeyListener {
  final PyEditor peditor;
  final JEditTextArea ptextarea;

  // ctrl-alt on windows & linux, cmd-alt on os x
  private static int CTRL_ALT = ActionEvent.ALT_MASK
      | Toolkit.getDefaultToolkit().getMenuShortcutKeyMask();

  // 4 spaces per pep8
  private static final String TAB = "    ";

  public PyKeyListener(final Editor editor, final JEditTextArea textarea) {
    super(editor, textarea);

    peditor = (PyEditor)editor;
    ptextarea = textarea;
  }

  @Override
  public boolean keyPressed(final KeyEvent event) {
    final char c = event.getKeyChar();
    final int code = event.getKeyCode();

    final Sketch sketch = peditor.getSketch();

    // things that change the content of the text area
    if ((code == KeyEvent.VK_BACK_SPACE) || (code == KeyEvent.VK_TAB)
        || (code == KeyEvent.VK_ENTER) || ((c >= 32) && (c < 128))) {
      sketch.setModified(true);
    }

    // ctrl-alt-[arrow] switches sketch tab
    if ((event.getModifiers() & CTRL_ALT) == CTRL_ALT) {
      if (code == KeyEvent.VK_LEFT) {
        sketch.handlePrevCode();
        return true;
      } else if (code == KeyEvent.VK_RIGHT) {
        sketch.handleNextCode();
        return true;
      }
    }

    // TODO handle ctrl-[up|down]; should move cursor to next empty line in
    // that direction

    // handle specific keypresses
    switch (c) {

      case 9: // tab; overriding with spaces
        ptextarea.setSelectedText(TAB);
        break;

      case 10: // return
      case 13: // also return
        final String text = ptextarea.getText(); // text
        final int cursor = ptextarea.getCaretPosition();
        ptextarea.setSelectedText(getIndent(cursor, text));
        break;
    }

    return false;
  }

  private static Pattern findIndent = Pattern.compile("^((?: |\\t)*)");
  private static Pattern incIndent = Pattern.compile(":( |\\t)*(#.*)?$"); // TODO

  String getIndent(final int cursor, final String text) {
    if (cursor <= 1) {
      return "\n";
    }

    int lineStart, lineEnd;
    int i;
    for (i = cursor - 1; i >= 0 && text.charAt(i) != '\n'; i--) {
      // noop
    }
    lineStart = i + 1;
    for (i = cursor - 1; i < text.length() && text.charAt(i) != '\n'; i++) {
      // noop
    }
    lineEnd = i;

    if (lineEnd <= lineStart) {
      return "\n";
    }

    final String line = text.substring(lineStart, lineEnd);

    String indent;
    final Matcher f = findIndent.matcher(line);

    if (f.find()) {
      indent = '\n' + f.group();

      if (incIndent.matcher(line).find()) {
        indent += TAB;
      }
    } else {
      indent = "\n";
    }

    return indent;
  }
}