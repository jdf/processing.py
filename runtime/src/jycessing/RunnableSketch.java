package jycessing;

import java.io.File;
import java.util.List;

import jycessing.Runner.LibraryPolicy;

/** Everything Runner.runSketchBlocking needs to know to be able to run a sketch. */
public interface RunnableSketch {
  /** @return The main file of the sketch */
  public abstract File getMainFile();

  /** @return The primary code to run */
  public abstract String getMainCode();

  /** @return The main directory of the sketch */
  public abstract File getHomeDirectory();

  /** @return Files to append to sys.path */
  public abstract List<File> getPathEntries();

  /** @return Arguments to pass to PApplet */
  public abstract String[] getPAppletArguments();

  /** @return Directories to search for Processing libraries */
  public abstract List<File> getLibraryDirectories();

  /** @return How eagerly we should look for libraries */
  public abstract LibraryPolicy getLibraryPolicy();

  /**
   * Should probably be true, unless you're a warmup sketch
   *
   * @return Whether the sketch should run or not
   */
  public abstract boolean shouldRun();
}
