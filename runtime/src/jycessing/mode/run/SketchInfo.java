package jycessing.mode.run;

import java.io.File;
import java.io.Serializable;

import jycessing.Runner.LibraryPolicy;
import jycessing.mode.RunMode;

public class SketchInfo implements Serializable {

  public final RunMode runMode;
  public final File libraries;

  // One of the following two should be set,
  public final File sketch;

  public final String code;
  public final String[] codePaths;
  public final int x;
  public final int y;
  public final LibraryPolicy libraryPolicy;

  private SketchInfo(final RunMode runMode, final File libraries, final File sketch,
      final String code, final String[] codePaths, final int x, final int y,
      final LibraryPolicy libraryPolicy) {
    this.runMode = runMode;
    this.libraries = libraries;
    this.sketch = sketch;
    this.code = code;
    this.codePaths = codePaths;
    this.x = x;
    this.y = y;
    this.libraryPolicy = libraryPolicy;
  }

  public static class Builder {
    private RunMode runMode;
    private File libraries;
    private File sketch;
    private String code;
    private String[] codePaths;
    private int x = -1;
    private int y = -1;
    private LibraryPolicy libraryPolicy;

    public SketchInfo build() {
      return new SketchInfo(runMode, libraries, sketch, code, codePaths, x, y, libraryPolicy);
    }

    public Builder runMode(final RunMode runMode) {
      this.runMode = runMode;
      return this;
    }

    public Builder libraries(final File libraries) {
      this.libraries = libraries;
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
