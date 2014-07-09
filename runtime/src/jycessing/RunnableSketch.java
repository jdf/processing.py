package jycessing;

import java.io.File;
import java.util.List;

import jycessing.Runner.LibraryPolicy;

/**
 *
 * Everything Runner.runSketchBlocking needs to know to be able to run a sketch.
 *
 */
public interface RunnableSketch {
  public abstract File getMainFile();
  public abstract String getMainCode();
  public abstract File getHomeDirectory();
  public abstract String[] getPAppletArguments();
  public abstract List<File> getLibraryDirectories();
  public abstract LibraryPolicy getLibraryPolicy();
  public abstract boolean shouldRun(); // should probably be true, unless you're a warmup sketch
}
