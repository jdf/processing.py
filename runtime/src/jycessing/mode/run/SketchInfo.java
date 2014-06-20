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

  // This may be different from the directory containing mainSketchFile,
  // because the sketch may have been temporarily copied into a temp
  // folder to make unsaved changes to source available.
  public final File sketchHome;

  public final File mainSketchFile;

  public final String sketchName;
  public final String code;
  public final String[] codeFileNames;
  public final Point editorLoc;
  public final Point sketchLoc;
  public final LibraryPolicy libraryPolicy;

  private SketchInfo(final String sketchName, final RunMode runMode, final List<File> libDirs,
      final File sketchHome, final File mainSketchFile, final String code,
      final String[] codeFileNames, final Point editorLoc, final Point sketchLoc,
      final LibraryPolicy libraryPolicy) {
    this.sketchName = sketchName;
    this.runMode = runMode;
    this.libraryDirs = Collections.unmodifiableList(libDirs);
    this.sketchHome = sketchHome;
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
    private File sketchHome;
    private File mainSketchFile;
    private String code;
    private String[] codeFileNames;
    private Point editorLoc;
    private Point sketchLoc;
    private LibraryPolicy libraryPolicy;

    public SketchInfo build() {
      if (sketchHome == null) {
        sketchHome = mainSketchFile.getParentFile();
      }
      return new SketchInfo(sketchName, runMode, libDirs, sketchHome, mainSketchFile, code,
          codeFileNames, editorLoc, sketchLoc, libraryPolicy);
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

    public Builder sketchHome(final File sketchHome) {
      this.sketchHome = sketchHome;
      return this;
    }

    public Builder mainSketchFile(final File mainSketchFile) {
      this.mainSketchFile = mainSketchFile;
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
