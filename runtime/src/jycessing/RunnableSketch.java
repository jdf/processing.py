package jycessing;

import java.io.File;
import java.util.List;

import jycessing.Runner.LibraryPolicy;


public interface RunnableSketch {
  public abstract File getMainFile();
  public abstract String getMainCode();
  public abstract File getHomeDirectory();
  public abstract String[] getPAppletArguments();
  public abstract List<File> getLibraryDirectories();
  public abstract LibraryPolicy getLibraryPolicy();
  public abstract boolean shouldRun(); // only for warmup sketch
}
