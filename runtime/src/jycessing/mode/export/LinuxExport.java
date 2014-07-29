package jycessing.mode.export;

import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.nio.file.Files;
import java.nio.file.attribute.PosixFilePermissions;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;

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
 * Performs an export to Linux (32/64).
 * The linux export folder layout is as follows:
 * 
 * $appdir/                        (e.g. $sketchname/application.linux32)
 *        /$sketchname             (executable shell script to run the application)
 *        /source/                 (the source code of the sketch; used to run it)
 *        /lib/                    (where java imports are stored)
 *            /jycessing/          (where stuff necessary to jycessing is stored;
 *                                  everything in here is added to the classpath.)
 *            /$libname/library/   (where resources for $libname - imported with
 *                                  add_library - are stored. Not added to classpath.)
 *        /code/                   (any other code resources the user wanted to add;
 *                                  copied verbatim.)
 *        /data/                   (all non-code resources; copied verbatim.)
 *        
 *
 */
public class LinuxExport extends PlatformExport {

  @Override
  protected void log(final String msg) {
    if (PythonMode.VERBOSE) {
      System.err.println(LinuxExport.class.getSimpleName() + ": " + msg);
    } else {
      System.err.println("Not logging.");
    }
  }

  public LinuxExport(Arch arch, Sketch sketch, PyEditor editor, Set<Library> libraries) {
    this.id = PConstants.LINUX;
    this.arch = arch;
    this.name = PConstants.platformNames[id] + arch.bits;
    this.sketch = sketch;
    this.editor = editor;
    this.libraries = libraries;
  }

  public void export() throws IOException {
    // Work out user preferences and other possibilities we care about
    final boolean embedJava =
        (id == PApplet.platform) && Preferences.getBoolean("export.application.embed_java");

    // Work out the folders we'll be (maybe) using
    final File destFolder = new File(sketch.getFolder(), "application." + name);
    final File javaFolder = new File(destFolder, "java");

    copyBasicStructure(destFolder);

    // Handle embedding java
    if (embedJava) {
      log("Embedding java in export.");
      javaFolder.mkdirs();
      Base.copyDir(Base.getJavaHome(), javaFolder);
    }

    buildShellScript(destFolder, embedJava);

    log("Done.");
  }

  private void buildShellScript(final File destFolder, final boolean embedJava) throws IOException {
    log("Creating shell script.");
    

    final boolean setMemory = Preferences.getBoolean("run.options.memory");
    final boolean presentMode = Preferences.getBoolean("export.application.fullscreen");
    final boolean stopButton = Preferences.getBoolean("export.application.stop") && presentMode;

    final File jycessingFolder = new File(destFolder, "lib/jycessing");
    final File scriptFile = new File(destFolder, sketch.getName());
    final PrintWriter script = new PrintWriter(scriptFile);
    
    // We explicitly use "\n" because PrintWriter.println() uses the system line ending,
    // Which will confuse Linux if we're running from Windows.
    script.print("#!/bin/sh\n");
    script.print("APPDIR=\"$( cd $( dirname \"$0\" ) && pwd )\"\n");

    if (embedJava) {
      script.print("JAVA=\"$APPDIR/java/bin/java\"\n");
    } else {
      script.print("JAVA=java\n");
    }

    // Make options for java
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
    for (final File f : jycessingFolder.listFiles()) {
      if (f.getName().toLowerCase().endsWith(".jar") || f.getName().toLowerCase().endsWith(".zip")) {
        classpath.append("$APPDIR/lib/jycessing/" + f.getName() + ":");
      }
    }
    options.add("-cp");
    options.add("\"" + classpath.toString().substring(0, classpath.toString().length() - 1) + "\"");

    options.add("-splash:\"$APPDIR/lib/jycessing/splash.png\"");

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

    options.add("\"$APPDIR/source/" + sketch.getCode(0).getFileName() + "\"");

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
      log("Couldn't set script executable... we'll assume whoever gets it can handle it");
    }
  }
}
