package test.jycessing;

import java.io.File;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

import processing.core.PApplet;
import jycessing.RunnableSketch;
import jycessing.Runner.LibraryPolicy;

/**
 * 
 * Encapsulates a unit test so that it can be run by Runner.
 *
 */
public class TestSketch implements RunnableSketch {

  private final Path sourcePath;
  private final String sourceText;
  private final String name;

  public TestSketch(final Path sourcePath, final String sourceText, final String name) {
    this.sourcePath = sourcePath;
    this.sourceText = sourceText;
    this.name = name;
  }

  @Override
  public File getMainFile() {
    return sourcePath.toFile();
  }

  @Override
  public String getMainCode() {
    return sourceText;
  }

  @Override
  public File getHomeDirectory() {
    return Paths.get("testing/resources/").toFile().getAbsoluteFile();
  }

  @Override
  public String[] getPAppletArguments() {
    return new String[] {PApplet.ARGS_SKETCH_FOLDER + "=" + getHomeDirectory(), name};
  }

  @Override
  public List<File> getLibraryDirectories() {
    return null;
  }

  @Override
  public LibraryPolicy getLibraryPolicy() {
    return LibraryPolicy.SELECTIVE;
  }

  @Override
  public boolean shouldRun() {
    return true;
  }

  @Override
  public List<File> getPathEntries() {
    final List<File> entries = new ArrayList<>();
    entries.add(getHomeDirectory());
    return entries;
  }

}
