package jycessing.mode;

import java.io.File;
import java.io.IOException;

import jycessing.mode.run.SketchServiceManager;
import processing.app.Base;
import processing.app.Editor;
import processing.app.EditorState;
import processing.app.Formatter;
import processing.app.Mode;
import processing.app.syntax.TokenMarker;

public class PythonMode extends Mode {

  public static final boolean VERBOSE = Boolean.parseBoolean(System.getenv("VERBOSE_PYTHON_MODE"));
  public static final boolean SKETCH_RUNNER_FIRST =
      Boolean.parseBoolean(System.getenv("SKETCH_RUNNER_FIRST"));

  private final FormatServer formatServer;
  private final SketchServiceManager sketchServiceManager;

  public PythonMode(final Base base, final File folder) {
    super(base, folder);
    formatServer = new FormatServer(folder);
    formatServer.start();
    sketchServiceManager = new SketchServiceManager(this);
    sketchServiceManager.start();
  }

  @Override
  public String getTitle() {
    return "Python";
  }

  @Override
  public Editor createEditor(final Base base, final String path, final EditorState state) {
    return new PyEditor(base, path, state, this);
  }

  @Override
  public String getDefaultExtension() {
    return "pyde";
  }

  @Override
  public String[] getExtensions() {
    return new String[] { "pyde", "py" };
  }

  @Override
  public String[] getIgnorable() {
    return new String[] {};
  }

  Formatter getFormatter() {
    return formatServer;
  }

  @Override
  protected void loadKeywords(File keywordFile) throws IOException {
    loadKeywords(keywordFile, "//");
  }

  @Override
  public TokenMarker createTokenMarker() {
    return new PythonTokenMarker();
  }

  public SketchServiceManager getSketchServiceManager() {
    return sketchServiceManager;
  }

  public void handleSketchStopped() {
    base.getActiveEditor().deactivateRun();
  }

  public void handleSketchException(Exception e) {
    base.getActiveEditor().statusError(e);
  }
}
