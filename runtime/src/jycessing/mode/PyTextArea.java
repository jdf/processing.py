package jycessing.mode;

import java.awt.Color;
import java.awt.Graphics;

import javax.swing.text.Segment;

import processing.app.syntax.JEditTextArea;
import processing.app.syntax.SyntaxStyle;
import processing.app.syntax.TextAreaDefaults;
import processing.app.syntax.TextAreaPainter;
import processing.app.syntax.Token;

public class PyTextArea extends JEditTextArea {

  public PyTextArea(final TextAreaDefaults defaults) {
    super(defaults);
  }

  private static final Color TAB_COLOR = new Color(0xEEEEEE);

  @Override
  protected TextAreaPainter createPainter(final TextAreaDefaults defaults) {
    return new TextAreaPainter(this, defaults) {
      /**
       * Paint indent indicators.
       */
      @Override
      protected int paintSyntaxLine(final Graphics gfx, final Segment line, final int x,
          final int y, final Token tokens, final SyntaxStyle[] styles) {
        final int origOffset = line.offset;
        final int origCount = line.count;
        final int newXPosition = super.paintSyntaxLine(gfx, line, x, y, tokens, styles);
        int xOffset = x + 2;// + fm.charWidth(' ') / 2;
        for (int i = 0; i <= origCount - 4; i += 4) {
          final String nextFour = String.copyValueOf(line.array, origOffset + i, 4);
          if (!nextFour.equals("    ")) {
            break;
          }
          if (i > 0) {
            gfx.setColor(TAB_COLOR);
            gfx.drawLine(xOffset, y - fm.getHeight() + 1, xOffset, y);
          }
          xOffset += fm.stringWidth("    ");
        }
        return newXPosition;
      }
    };
  }
}
