package jycessing.mode.run;

import java.io.File;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import jycessing.Runner.LibraryPolicy;
import jycessing.mode.RunMode;

public class SketchInfo implements Serializable {

  public final RunMode runMode;
  public final List<File> libraryDirs;

  // One of the following two should be set,
  public final File sketch;

  public final String code;
  public final String[] codePaths;
  public final int x;
  public final int y;
  public final LibraryPolicy libraryPolicy;

  private SketchInfo(final RunMode runMode, final List<File> libDirs, final File sketch,
      final String code, final String[] codePaths, final int x, final int y,
      final LibraryPolicy libraryPolicy) {
    this.runMode = runMode;
    this.libraryDirs = Collections.unmodifiableList(libDirs);
    this.sketch = sketch;
    this.code = code;
    this.codePaths = codePaths;
    this.x = x;
    this.y = y;
    this.libraryPolicy = libraryPolicy;
  }

  public static class Builder {
    private RunMode runMode;
    private final List<File> libDirs = new ArrayList<File>();
    private File sketch;
    private String code;
    private String[] codePaths;
    private int x = -1;
    private int y = -1;
    private LibraryPolicy libraryPolicy;

    public SketchInfo build() {
      return new SketchInfo(runMode, libDirs, sketch, code, codePaths, x, y, libraryPolicy);
    }

    public Builder runMode(final RunMode runMode) {
      this.runMode = runMode;
      return this;
    }

    public Builder addLibraryDir(final File dir) {
      libDirs.add(dir);
      return this;
    }

    public Builder sketch(final File sketch) {
      this.sketch = sketch;
      return this;
    }

    public Builder code(final String code) {
      this.code = code;
      return this;
    }

    public Builder codePaths(final String[] codePaths) {
      this.codePaths = codePaths;
      return this;
    }

    public Builder x(final int x) {
      this.x = x;
      return this;
    }

    public Builder y(final int y) {
      this.y = y;
      return this;
    }

    public Builder libraryPolicy(final LibraryPolicy libraryPolicy) {
      this.libraryPolicy = libraryPolicy;
      return this;
    }
  }

}
