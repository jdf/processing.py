package jycessing.mode;

import java.io.File;

import processing.app.Base;
import processing.app.Editor;
import processing.app.EditorState;
import processing.app.Mode;

public class ProcessingDotPyMode extends Mode {

  public ProcessingDotPyMode(final Base base, final File folder) {
    super(base, folder);
  }

  @Override
  public String getTitle() {
    return "Processing.py";
  }

  @Override
  public Editor createEditor(final Base base, final String path, final EditorState state) {
    return new PyEditor(base, path, state, this);
  }

  @Override
  public String getDefaultExtension() {
    return "pde";
  }

  @Override
  public String[] getExtensions() {
    return new String[] { "pde", "py", "pyde" };
  }

  @Override
  public String[] getIgnorable() {
    return new String[] {};
  }

}
