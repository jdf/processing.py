package jycessing.mode.export;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.nio.file.attribute.PosixFilePermissions;
import java.io.FilenameFilter;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import jycessing.mode.PyEditor;
import jycessing.mode.PythonMode;
import processing.app.Base;
import processing.app.Library;
import processing.app.Preferences;
import processing.app.Sketch;
import processing.core.PApplet;
import processing.core.PConstants;


/**
 * 
 * A Mac export.
 * 
 * If we embed java, we embed Processing's java, since we know it's been properly appbundled
 * and all symlinks work and stuff.
 * 
 * N.B. We use bash for the executable, so that we can easily include a pile of command line arguments,
 * as well as being able to prompt the user to install Java.
 *
 * Inspired by: https://github.com/tofi86/universalJavaApplicationStub
 * 
 * Layout:
 * $appdir/
 *        /$sketch.app/Contents/
 *              /MacOS/
 *                    /$sketch (shell script that cd's to ../Processing and runs the sketch)
 *              /Info.plist
 *              /Resources/
 *                    /sketch.icns (pretty icon)
 *                    /dialogs.applescript (used by main script to show native prompts)
 *              /Processing/
 *                    /source/
 *                    /lib/
 *                    /code/
 *                    /data/
 *              /PlugIns/jdk$version.jdk/ (copied from core processing)
 *                     
 *
 */
public class MacExport extends PlatformExport {

  @Override
  protected void log(final String msg) {
    if (PythonMode.VERBOSE) {
      System.err.println(MacExport.class.getSimpleName() + ": " + msg);
    }
  }

  public MacExport(Sketch sketch, PyEditor editor, Set<Library> libraries) {
    this.id = PConstants.MACOSX;
    this.name = PConstants.platformNames[id];
    this.sketch = sketch;
    this.editor = editor;
    this.libraries = libraries;
    this.arch = Arch.AMD64;
  }

  @Override
  public void export() throws IOException {
    // Work out user preferences and other possibilities we care about
    final boolean embedJava =
        (id == PApplet.platform) && Preferences.getBoolean("export.application.embed_java");

    // Work out the folders we'll be (maybe) using
    final File destFolder = new File(sketch.getFolder(), "application." + name);
    final File appRootFolder = new File(destFolder, sketch.getName() + ".app");
    final File contentsFolder = new File(appRootFolder, "Contents");
    final File binFolder = new File(contentsFolder, "MacOS");
    final File resourcesFolder = new File(contentsFolder, "Resources");
    final File processingFolder = new File(contentsFolder, "Processing");

    copyBasicStructure(processingFolder);

    copyStaticResources(resourcesFolder);

    if (embedJava) {
      copyJDKPlugin(new File(contentsFolder, "PlugIns"));
    }

    setUpInfoPlist(new File(contentsFolder, "Info.plist"), sketch.getName());

    setUpExecutable(binFolder, processingFolder, sketch.getName(), embedJava);

    log("Done.");
  }

  /**
   * Copy Processing's builtin JDK to the export.
   * 
   * (This only makes sense when we're on a Mac, running Processing from a .app bundle.)
   */
  private void copyJDKPlugin(final File targetPluginsFolder) throws IOException {
    // This is how Java Mode finds it... basically
    final File sourceJDKFolder = Base.getContentFile("../PlugIns").listFiles(new FilenameFilter() {
      public boolean accept(File dir, String name) {
        return name.endsWith(".jdk") && !name.startsWith(".");
      }
    })[0].getAbsoluteFile();

    log("Copying JDK from " + sourceJDKFolder);

    targetPluginsFolder.mkdirs();
    final File targetJDKFolder = new File(targetPluginsFolder, sourceJDKFolder.getName());
    Base.copyDirNative(sourceJDKFolder, targetJDKFolder);
  }


  private final static Pattern sketchPattern = Pattern.compile("@@sketch@@");

  /**
   * Read in Info.plist.tmpl, modify fields, package away in .app
   */
  private void setUpInfoPlist(final File targetInfoPlist, final String sketchName)
      throws IOException {
    log("Setting up Info.plist.");
    targetInfoPlist.getAbsoluteFile().getParentFile().mkdirs();

    final Path infoPlistTemplate =
        editor.getModeContentFile("application/macosx/Info.plist.tmpl").toPath();
    final String infoPlistTemplateText = new String(Files.readAllBytes(infoPlistTemplate), "UTF-8");
    final Matcher sketchNameMatcher = sketchPattern.matcher(infoPlistTemplateText);
    Files.write(targetInfoPlist.toPath(), sketchNameMatcher.replaceAll(sketchName).getBytes(),
        StandardOpenOption.WRITE, StandardOpenOption.CREATE);
  }

  /**
   * Copy things that don't change between runs.
   */
  private void copyStaticResources(final File resourcesFolder) throws IOException {
    log("Moving static macosx resources.");
    final File osxFolder = editor.getModeContentFile("application/macosx");
    resourcesFolder.mkdirs();
    Base.copyFile(new File(osxFolder, "sketch.icns"), new File(resourcesFolder, "sketch.icns"));
    Base.copyFile(new File(osxFolder, "dialogs.applescript"), new File(resourcesFolder,
        "dialogs.applescript"));
  }

  /**
   * Create the shell script that will run the sketch.
   * 
   * Some duplicated code here from LinuxExport, but there's enough differences that I want to keep them separate
   */
  private void setUpExecutable(final File binFolder, final File processingFolder,
      final String sketchName, final boolean embedJava) throws IOException {

    log("Creating shell script.");

    final boolean setMemory = Preferences.getBoolean("run.options.memory");
    final boolean presentMode = Preferences.getBoolean("export.application.fullscreen");
    final boolean stopButton = Preferences.getBoolean("export.application.stop") && presentMode;

    binFolder.mkdirs();

    final File scriptFile = new File(binFolder, sketch.getName());
    final PrintWriter script = new PrintWriter(scriptFile);

    
    // We explicitly use "\n" because PrintWriter.println() uses the system line ending,
    // which will confuse Macs if we're running from Windows.
    script.print("#!/bin/bash\n");
    script.print("CONTENTS=\"$( cd \"$( dirname \"$0\" )/..\" && pwd )\"\n");

    if (!embedJava) {
      log("Adding java-locating prelude to script.");

      final Path findJavaScript = editor.getModeContentFile("application/macosx/findjava").toPath();
      final String findJava =
          new String(Files.readAllBytes(findJavaScript), "UTF-8").replaceAll("\\r\\n?", "\n");
      script.print(findJava + "\n");
    } else {
      script
          .print("JAVA=\"$(find $CONTENTS/PlugIns -maxdepth 1 -type d -name '*jdk')/Contents/Home/jre/bin/java\"" + "\n");
    }

    script.print("APPDIR=\"$CONTENTS/Processing\"\n");

    final List<String> options = new ArrayList<>();

    // https://github.com/processing/processing/issues/2239
    options.add("-Djna.nosys=true");

    // Set library path
    options.add("-Djava.library.path=\"$APPDIR:$APPDIR/lib:$APPDIR/lib/jycessing\"");

    // Enable assertions
    options.add("-ea");

    // Set memory
    if (setMemory) {
      options.add("-Xms" + Preferences.get("run.options.memory.initial") + "m");
      options.add("-Xmx" + Preferences.get("run.options.memory.maximum") + "m");
    }

    // Work out classpath - only add core stuff, the rest will be found by add_library
    final StringWriter classpath = new StringWriter();
    for (final File f : new File(processingFolder, "lib/jycessing").listFiles()) {
      if (f.getName().toLowerCase().endsWith(".jar") || f.getName().toLowerCase().endsWith(".zip")) {
        classpath.append("$APPDIR/lib/jycessing/" + f.getName() + ":");
      }
    }
    options.add("-cp");
    options.add("\"" + classpath.toString().substring(0, classpath.toString().length() - 1) + "\"");

    if (!presentMode) {
      // Wait, this seems totally arbitrary.
      // Why only have a splash screen if we're not in present mode?
      options.add("-splash:\"$APPDIR/lib/jycessing/splash.png\"");
      // Because removing the splash screen (see Runner.runSketchBlocking) _and_ being
      // in OS X full-screen mode causes the sketch to sorta-freeze. (It still runs,
      // it just doesn't update on screen / respond to keypresses.)
      // Why? I have no idea. But seriously, don't change this, I just spent 8 hours debugging it.
    }

    options.add("-Xdock:icon=\"$CONTENTS/Resources/sketch.icns\"");
    options.add("-Xdock:name=\"" + sketchName + "\"");

    if (PythonMode.VERBOSE) {
      // If we're in debug mode, assume we want our exports to be, too
      options.add("-Dverbose=true");
    }

    // Class to run
    options.add("jycessing.Runner");

    // Runner arguments
    options.add("--noredirect");
    options.add("--exported");

    if (presentMode) {
      options.add(PApplet.ARGS_FULL_SCREEN);

      options.add(PApplet.ARGS_BGCOLOR + "=" + Preferences.get("run.present.bgcolor"));
    }

    if (stopButton) {
      options.add(PApplet.ARGS_STOP_COLOR + "=" + Preferences.get("run.present.stop.color"));
    } else {
      options.add(PApplet.ARGS_HIDE_STOP);
    }

    options.add("\"$APPDIR/source/" + sketch.getCode(0).getFileName()+"\"");

    script.print("$JAVA");
    for (final String o : options) {
      script.print(" " + o);
    }
    script.print("\n");
    script.close();

    log("Setting script executable.");
    try {
      Files
        .setPosixFilePermissions(scriptFile.toPath(), PosixFilePermissions.fromString("rwxrwxrwx"));
    } catch (UnsupportedOperationException e) {
      // Windows, probably
      log("Couldn't set script executable... .app should work anyway, though");
    }
  }
}
