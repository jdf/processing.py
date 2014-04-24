package jycessing.mode;

import java.awt.Image;
import java.awt.event.MouseEvent;

import javax.swing.JPopupMenu;

import processing.app.Base;
import processing.app.Editor;
import processing.app.EditorToolbar;

@SuppressWarnings("serial")
public class PyToolbar extends EditorToolbar {

  static protected final int RUN = 0;
  static protected final int STOP = 1;

  static protected final int NEW = 2;
  static protected final int OPEN = 3;
  static protected final int SAVE = 4;
  static protected final int EXPORT = 5;

  static public String getTitle(final int index, final boolean shift) {
    switch (index) {
      case RUN:
        return !shift ? "Run" : "Present";
      case STOP:
        return "Stop";
      case NEW:
        return "New";
      case OPEN:
        return "Open";
      case SAVE:
        return "Save";
      case EXPORT:
        return "Export Application";
    }
    return null;
  }

  public PyToolbar(final Editor editor, final Base base) {
    super(editor, base);
  }

  @Override
  public void handlePressed(final MouseEvent e, final int sel) {
    final boolean shift = e.isShiftDown();
    final PyEditor peditor = (PyEditor)editor;

    switch (sel) {
      case RUN:
        if (shift) {
          peditor.handlePresent();
        } else {
          peditor.handleRun();
        }
        break;

      case STOP:
        peditor.handleStop();
        break;

      case OPEN:
        final JPopupMenu popup = editor.getMode().getToolbarMenu().getPopupMenu();
        popup.show(this, e.getX(), e.getY());
        break;

      case NEW:
        base.handleNew();
        break;

      case SAVE:
        peditor.handleSave(false);
        break;

      case EXPORT:
        peditor.handleExportApplication();
        break;
    }
  }

  @Override
  public void init() { // open up the processing icons
    final Image[][] images = loadImages();
    for (int i = 0; i < 6; i++) {
      addButton(getTitle(i, false), getTitle(i, true), images[i], i == NEW);
    }
  }
}
