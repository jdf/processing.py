package jycessing.mode.export;

import java.io.File;
import java.io.FileNotFoundException;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import java.nio.file.Files;

import processing.core.PApplet;
import jycessing.RunnableSketch;
import jycessing.Runner.LibraryPolicy;
import jycessing.DisplayType;

/**
 * A sketch that's been exported from the PDE.
 * Runner.main() will create one of these if ARGS_EXPORTED is in argv.
 * 
 * This class tries to make sure that the exported sketch is in the right configuration - if it isn't,
 * it will warn the user and fail.
 */
public class ExportedSketch implements RunnableSketch {

  public static final String ARGS_EXPORTED = "--exported";
  
  private final File sketchPath;
  private final File sketchHome;
  private final String code;
  private final DisplayType displayType;
  private final String backgroundColor;
  private final String stopColor;
  private final List<File> libraryDirs;
  
  /**
   * @param args Command line arguments
   * @throws FileNotFoundException if the main sketch file can't be found
   */
  public ExportedSketch(final String[] args) throws Exception {
    // The last argument is the path to the sketch
    this.sketchPath = new File(args[args.length - 1]).getAbsoluteFile();
    this.sketchHome = sketchPath.getParentFile().getParentFile();

    if (!sketchPath.exists()) {
      throw new FileNotFoundException("Something is terribly wrong - I can't find your sketch!");
    }

    final List<String> codeLines =
        Files.readAllLines(sketchPath.toPath(), Charset.forName("UTF-8"));

    final StringBuilder code = new StringBuilder();
    for (final String line : codeLines) {
      code.append(line);
      code.append('\n');
    }
    this.code = code.toString();
    
    if (Arrays.asList(args).contains(PApplet.ARGS_FULL_SCREEN)) {
      this.displayType = DisplayType.PRESENTATION;
    } else {
      this.displayType = DisplayType.WINDOWED;
    }
    
    String backgroundColor = null;
    String stopColor = null;
    for (final String arg : args) {
      if (arg.contains(PApplet.ARGS_BGCOLOR)) {
        backgroundColor = arg.substring(arg.indexOf("=") + 1);
      } else if (arg.contains(PApplet.ARGS_STOP_COLOR)) {
        stopColor = arg.substring(arg.indexOf("=") + 1);
      }
    }
    this.backgroundColor = backgroundColor;
    this.stopColor = stopColor;
    
    final List<File> libraryDirs = new ArrayList<>();
    libraryDirs.add(sketchPath.getParentFile()); // "$APPDIR/source"
    final File libDir = new File(getHomeDirectory(), "lib");
    if (libDir.exists()) {
      libraryDirs.add(libDir); // "$APPDIR/lib"
    }
    final File codeDir = new File(getHomeDirectory(), "code");
    if (codeDir.exists()) {
      libraryDirs.add(codeDir); // "$APPDIR/lib"
    }
    this.libraryDirs = libraryDirs;
  }

  @Override
  public File getMainFile() {
    return sketchPath;
  }
  
  @Override
  public String getMainCode() {
    return code;
  }

  @Override
  public File getHomeDirectory() {
    return sketchHome;
  }

  @Override
  public String[] getPAppletArguments() {
    final List<String> args = new ArrayList<>();
    
    if (displayType == DisplayType.PRESENTATION) {
      args.add(PApplet.ARGS_FULL_SCREEN);
      args.add(PApplet.ARGS_BGCOLOR + "=" + backgroundColor);
      
      if (stopColor != null) {
        args.add(PApplet.ARGS_STOP_COLOR + "=" + stopColor);
      } else {
        args.add(PApplet.ARGS_HIDE_STOP);
      }
    }
    
    args.add(PApplet.ARGS_SKETCH_FOLDER + "=" + getHomeDirectory());
    
    args.add(sketchPath.getName()); // sketch name; must be last argument
    
    return args.toArray(new String[0]);
  }

  @Override
  public List<File> getLibraryDirectories() {
    return libraryDirs;
  }

  @Override
  public LibraryPolicy getLibraryPolicy() {
    return LibraryPolicy.PROMISCUOUS;
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
    entries.add(new File(sketchHome, "lib"));
    
    return entries;
  }

}
