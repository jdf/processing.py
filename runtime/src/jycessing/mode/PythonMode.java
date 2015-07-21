package jycessing.mode;

import java.io.File;
import java.io.IOException;

import jycessing.mode.run.SketchRunner;
import jycessing.mode.run.SketchService;
import jycessing.mode.run.SketchServiceManager;
import processing.app.Base;
import processing.app.ui.Editor;
import processing.app.ui.EditorState;
import processing.app.Formatter;
import processing.app.Mode;
import processing.app.syntax.TokenMarker;

public class PythonMode extends Mode {

  /**
   * If the environment variable VERBOSE_PYTHON_MODE is equal to the string "true", then
   * many Python Mode operations will be logged to standard error.
   */
  public static final boolean VERBOSE = Boolean.parseBoolean(System.getenv("VERBOSE_PYTHON_MODE"));

  /**
   * If the environment variable SKETCH_RUNNER_FIRST is equal to the string "true", then
   * {@link PythonMode} expects that the {@link SketchRunner} is already running and waiting
   * to be communicated with (as when you're debugging it in Eclipse, for example).
   */
  public static final boolean SKETCH_RUNNER_FIRST = Boolean.parseBoolean(System
      .getenv("SKETCH_RUNNER_FIRST"));

  /**
   * Python auto-formatting is handled by a server. {@link FormatServer} handles
   * the lifecycle of, and communication with, that server.
   */
  private final FormatServer formatServer;

  /**
   * Sketches are run in external JVM processes. The {@link SketchServiceManager} handles
   * the creation and destruction of those processes, and routes communication between
   * {@link PyEditor}s and their affiliated {@link SketchService}s.
   */
  private final SketchServiceManager sketchServiceManager;

  public PythonMode(final Base base, final File folder) {
    super(base, folder);
    formatServer = new FormatServer(folder);
    sketchServiceManager = new SketchServiceManager(this);
    /*
     * Since we're compatible with Java mode's libraries, we just hijack
     * their libraries folder.
     * WARNING: this depends on an implementation detail in {@link Mode},
     * and not on any API. May break in the future.
     */
    librariesFolder = Base.getContentFile("modes/java/libraries");
  }

  @Override
  public String getTitle() {
    return "Python";
  }

  @Override
  public Editor createEditor(final Base base, final String path, final EditorState state) {
    // Lazily start the format server only when an editor is required.
    if (!formatServer.isStarted()) {
      formatServer.start();
    }
    // Lazily start the sketch running service only when an editor is required.
    if (!sketchServiceManager.isStarted()) {
      sketchServiceManager.start();
    }
    return new PyEditor(base, path, state, this);
  }

  @Override
  public String getDefaultExtension() {
    return "pyde";
  }

  @Override
  public String getModuleExtension() {
    return "py";
  }

  @Override
  public String[] getExtensions() {
    return new String[] {getDefaultExtension(), getModuleExtension()};
  }

  @Override
  public String[] getIgnorable() {
    return new String[] {};
  }

  Formatter getFormatter() {
    return formatServer;
  }

  @Override
  protected void loadKeywords(final File keywordFile) throws IOException {
    loadKeywords(keywordFile, "//");
  }

  @Override
  public TokenMarker createTokenMarker() {
    return new PythonTokenMarker();
  }

  public SketchServiceManager getSketchServiceManager() {
    return sketchServiceManager;
  }

}
