package jycessing.mode.run;

import java.awt.Point;
import java.io.File;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

import processing.app.Base;
import processing.app.Sketch;
import processing.core.PApplet;
import jycessing.DisplayType;
import jycessing.RunnableSketch;
import jycessing.Runner.LibraryPolicy;

/**
 * This class is a little bit wacky.
 * It's created in the PDE process, serialized, and then used in 
 * the sketch process.
 * I'm hoping lazy class loading will prevent the sketch process
 * from complaining that it doesn't know about Base.
 */

public class PdeSketch implements RunnableSketch, Serializable {
  
  private final List<File> libraryDirs;
  private final File mainFile;
  private final String mainCode;
  private final File sketchHome;
  private final Point location;
  private final boolean isEditorLocation;
  private final DisplayType displayType;
  
  public final String[] codeFileNames; // unique to PdeSketch - leave as public field?
  
  public PdeSketch(final Sketch sketch,
                    final File sketchPath,
                    final DisplayType displayType,
                    final Point location,
                    final boolean isEditorLocation) {
    
    this.displayType = displayType;
    this.location = location;
    this.isEditorLocation = isEditorLocation;
    
    this.mainFile = sketchPath.getAbsoluteFile();
    this.mainCode = sketch.getMainProgram();
    this.sketchHome = sketch.getFolder().getAbsoluteFile();
    
    final List<File> libraryDirs = new ArrayList<>();
    libraryDirs.add(Base.getContentFile("modes/java/libraries"));
    libraryDirs.add(Base.getSketchbookLibrariesFolder());
    libraryDirs.add(sketch.getCodeFolder());
    this.libraryDirs = libraryDirs;

    final String[] codeFileNames = new String[sketch.getCodeCount()];
    for (int i = 0; i < codeFileNames.length; i++) {
      codeFileNames[i] = sketch.getCode(i).getFile().getName();
    }
    this.codeFileNames = codeFileNames;
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
    List<String> args = new ArrayList<>();
    
    args.add(PApplet.ARGS_EXTERNAL);
    args.add(PApplet.ARGS_SKETCH_FOLDER + "=" + sketchHome);
    
    switch (displayType) {
    case WINDOWED:
      if (isEditorLocation) {
        args.add(String.format("%s=%d,%d", PApplet.ARGS_EDITOR_LOCATION, location.x, location.y));
      } else {
        args.add(String.format("%s=%d,%d", PApplet.ARGS_LOCATION, location.x, location.y));
      }
      break;
    case PRESENTATION:
      args.add(PApplet.ARGS_FULL_SCREEN);
      args.add(PApplet.ARGS_HIDE_STOP);
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
}
