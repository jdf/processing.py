package jycessing.mode;

import java.awt.event.InputEvent;

import processing.app.Editor;
import processing.app.EditorToolbar;

@SuppressWarnings("serial")
public class PyToolbar extends EditorToolbar {

  public PyToolbar(final Editor editor) {
    super(editor);
  }

  @Override
  public void handleRun(final int modifiers) {
    final PyEditor peditor = (PyEditor)editor;
    final boolean shift = (modifiers & InputEvent.SHIFT_MASK) != 0;
    if (shift) {
      peditor.handlePresent();
    } else {
      peditor.handleRun();
    }
  }

  @Override
  public void handleStop() {
    final PyEditor peditor = (PyEditor)editor;
    peditor.handleStop();
  }
}
