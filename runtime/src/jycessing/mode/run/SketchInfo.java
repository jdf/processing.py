package jycessing.mode.run;

import java.awt.Point;
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

  public final File mainSketchFile;

  public final String sketchName;
  public final String code;
  public final String[] codeFileNames;
  public final Point editorLoc;
  public final Point sketchLoc;
  public final LibraryPolicy libraryPolicy;

  private SketchInfo(final String sketchName, final RunMode runMode, final List<File> libDirs,
      final File mainSketchFile, final String code, final String[] codeFileNames,
      final Point editorLoc, final Point sketchLoc, final LibraryPolicy libraryPolicy) {
    this.sketchName = sketchName;
    this.runMode = runMode;
    this.libraryDirs = Collections.unmodifiableList(libDirs);
    this.mainSketchFile = mainSketchFile;
    this.code = code;
    this.codeFileNames = codeFileNames;
    this.editorLoc = editorLoc;
    this.sketchLoc = sketchLoc;
    this.libraryPolicy = libraryPolicy;
  }

  public static class Builder {
    private String sketchName;
    private RunMode runMode;
    private final List<File> libDirs = new ArrayList<>();
    private File sketch;
    private String code;
    private String[] codeFileNames;
    private Point editorLoc;
    private Point sketchLoc;
    private LibraryPolicy libraryPolicy;

    public SketchInfo build() {
      return new SketchInfo(sketchName, runMode, libDirs, sketch, code, codeFileNames, editorLoc,
          sketchLoc, libraryPolicy);
    }

    public Builder sketchName(final String sketchName) {
      this.sketchName = sketchName;
      return this;
    }

    public Builder runMode(final RunMode runMode) {
      this.runMode = runMode;
      return this;
    }

    public Builder addLibraryDir(final File dir) {
      libDirs.add(dir);
      return this;
    }

    public Builder mainSketchFile(final File sketch) {
      this.sketch = sketch;
      return this;
    }

    public Builder code(final String code) {
      this.code = code;
      return this;
    }

    public Builder codeFileNames(final String[] codeFileNames) {
      this.codeFileNames = codeFileNames;
      return this;
    }

    public Builder sketchLoc(final Point sketchLoc) {
      this.sketchLoc = sketchLoc;
      return this;
    }

    public Builder editorLoc(final Point editorLoc) {
      this.editorLoc = editorLoc;
      return this;
    }

    public Builder libraryPolicy(final LibraryPolicy libraryPolicy) {
      this.libraryPolicy = libraryPolicy;
      return this;
    }
  }

}
