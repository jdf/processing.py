package jycessing.mode.run;

import java.awt.Point;
import java.io.File;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

import jycessing.DisplayType;
import jycessing.RunnableSketch;
import jycessing.Runner.LibraryPolicy;
import processing.app.Base;
import processing.app.Platform;
import processing.app.Sketch;
import processing.core.PApplet;

/**
 * A sketch run from the PDE.
 *
 * This is created in the PDE process, serialized, and then used in the sketch process.
 */

@SuppressWarnings("serial")
public class PdeSketch implements RunnableSketch, Serializable {

  private final List<File> libraryDirs;
  private final File mainFile;
  private final String mainCode;
  private final File sketchHome;
  private final Point location;
  private final LocationType locationType;
  private final DisplayType displayType;

  public final String[] codeFileNames; // unique to PdeSketch - leave as public field?

  public PdeSketch(final Sketch sketch, final File sketchPath, final DisplayType displayType,
      final Point location, final LocationType locationType) {

    this.displayType = displayType;
    this.location = location;
    this.locationType = locationType;

    this.mainFile = sketchPath.getAbsoluteFile();
    this.mainCode = sketch.getMainProgram();
    this.sketchHome = sketch.getFolder().getAbsoluteFile();

    final List<File> libraryDirs = new ArrayList<>();
    libraryDirs.add(Platform.getContentFile("modes/java/libraries"));
    libraryDirs.add(Base.getSketchbookLibrariesFolder());
    libraryDirs.add(sketch.getCodeFolder());
    this.libraryDirs = libraryDirs;

    final String[] codeFileNames = new String[sketch.getCodeCount()];
    for (int i = 0; i < codeFileNames.length; i++) {
      codeFileNames[i] = sketch.getCode(i).getFile().getName();
    }
    this.codeFileNames = codeFileNames;
  }

  public static enum LocationType {
    EDITOR_LOCATION, SKETCH_LOCATION;
  }

  @Override
  public File getMainFile() {
    return mainFile;
  }

  @Override
  public String getMainCode() {
    return mainCode;
  }

  @Override
  public File getHomeDirectory() {
    return mainFile.getParentFile();
  }

  @Override
  public String[] getPAppletArguments() {
    final List<String> args = new ArrayList<>();

    args.add(PApplet.ARGS_EXTERNAL);
    args.add(PApplet.ARGS_SKETCH_FOLDER + "=" + sketchHome);

    switch (displayType) {
      case WINDOWED:
        if (locationType == LocationType.EDITOR_LOCATION) {
          args.add(String.format("%s=%d,%d", PApplet.ARGS_EDITOR_LOCATION, location.x, location.y));
        } else if (locationType == LocationType.SKETCH_LOCATION) {
          args.add(String.format("%s=%d,%d", PApplet.ARGS_LOCATION, location.x, location.y));
        }
        break;
      case PRESENTATION:
        args.add("fullScreen");
        break;
    }

    args.add(mainFile.getName()); // sketch name; has to be last argument

    return args.toArray(new String[0]);
  }

  @Override
  public List<File> getLibraryDirectories() {
    return libraryDirs;
  }

  /**
   * PDE sketches should be selective - no need to rush, we can just load as we go.
   */
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
    entries.add(sketchHome);
    entries.add(new File(sketchHome, "source"));
    final File code = new File(sketchHome, "code");
    if (code.exists()) {
      entries.add(code);
    }
    return entries;
  }
}
