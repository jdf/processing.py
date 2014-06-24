package jycessing.mode.export;

import java.util.ArrayList;
import java.util.List;
import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.nio.file.Files;
import java.nio.file.attribute.PosixFilePermissions;

import jycessing.mode.PyEditor;
import jycessing.mode.PythonMode;
import processing.app.Base;
import processing.app.Library;
import processing.app.Preferences;
import processing.app.Sketch;
import processing.app.SketchCode;
import processing.core.PApplet;
import processing.core.PConstants;

public class LinuxExport extends PlatformExport {

  private static void log(final String msg) {
    if (PythonMode.VERBOSE) {
      System.err.println(LinuxExport.class.getSimpleName() + ": " + msg);
    }
  }
  
  private Sketch sketch;
  private List<Library> libraries;
  private PyEditor editor;
  
  public LinuxExport(int bits, Sketch sketch, PyEditor editor, List<Library> libraries) {
    this.id = PConstants.LINUX;
    this.bits = bits;
    this.name = PConstants.platformNames[id] + bits;
    this.sketch = sketch;
    this.editor = editor;
    this.libraries = libraries;
  }
  
  public void export() throws IOException {
    // Work out user preferences and other possibilities we care about
    final boolean embedJava = (id == PApplet.platform) && Preferences.getBoolean("export.application.embed_java");
    final boolean hasData = sketch.hasDataFolder();
    final boolean hasCode = sketch.hasCodeFolder();
    final boolean deletePrevious = Preferences.getBoolean("export.delete_target_folder");
    final boolean setMemory = Preferences.getBoolean("run.options.memory");
    
    // Work out the folders we'll be (maybe) using
    final File destFolder = new File(sketch.getFolder(), "application."+name);
    final File libFolder = new File(destFolder, "lib");
    final File codeFolder = new File(destFolder, "code");
    final File sourceFolder = new File(destFolder, "source");
    final File dataFolder = new File(destFolder, "data");
    final File javaFolder = new File(destFolder, "java");
    
    // Delete previous export (if the user wants to, and it exists) and make a new one
    if (deletePrevious) {
      log("Removing old export folder.");
      Base.removeDir(destFolder);
    }
    destFolder.mkdirs();
    
    // Handle embedding java
    if (embedJava) {
      log("Embedding java in export.");
      javaFolder.mkdirs();
      Base.copyDir(Base.getJavaHome(), javaFolder);
    }
    
    // Handle data folder
    if (hasData) {
      log("Copying data folder to export.");
      dataFolder.mkdirs();
      Base.copyDir(sketch.getDataFolder(), dataFolder);
    }
    
    // Handle code folder
    if (hasCode) {
      log("Copying code folder to export.");
      codeFolder.mkdirs();
      Base.copyDir(sketch.getCodeFolder(), codeFolder);
    }
    
    // Handle source folder
    {
      log("Copying source to export.");
      sourceFolder.mkdirs();
      for (SketchCode code : sketch.getCode()){
        code.copyTo(new File(sourceFolder, code.getFileName()));
      }
    }
    
    // Handle imported libraries
    // For now, all we have is the core library
    {
      log("Copying libraries to export.");
      libFolder.mkdirs();
      for (Library library : libraries) {
        for (File exportFile : library.getApplicationExports(id, bits)) {
          final String exportName = exportFile.getName();
          if (!exportFile.exists()) {
            System.err.println("The file "+exportName+" is mentioned in the export.txt from "
                          +library+" but does not actually exist. Moving on.");
            continue;
          }
          if (exportFile.isDirectory()) {
            Base.copyDir(exportFile, new File(libFolder, exportName));
          } else {
            Base.copyFile(exportFile, new File(libFolder, exportName));
          }
        }
      }
    }
    
    // Handle Python Mode stuff
    {
      log("Copying core processing.py .jars to export.");
      Base.copyDir(editor.getModeFolder(), libFolder);
    }
    
    // Make shell script
    {
      log("Creating shell script.");
      File scriptFile = new File(destFolder, sketch.getName());
      PrintWriter script = new PrintWriter(scriptFile);
      script.println("#!/bin/sh");
      script.println("APPDIR=$( cd $( dirname \"$0\" ) && pwd )");
      
      if (embedJava) {
        script.println("JAVA=$APPDIR/jre/bin/java");
      } else {
        script.println("JAVA=$(which java)");
      }
      
      // Make options for java
      List<String> options = new ArrayList<String>();
      
      // https://github.com/processing/processing/issues/2239
      options.add("-Djna.nosys=true");
      
      // Set library path
      options.add("-Djava.library.path=\"$APPDIR:$APPDIR/lib\"");
      
      // Enable assertions
      options.add("-ea");
      
      // Set memory
      if (setMemory) {
        options.add("-Xms" + Preferences.get("run.options.memory.initial") + "m");
        options.add("-Xmx" + Preferences.get("run.options.memory.maximum") + "m");
      }
      
      // Work out classpath
      StringWriter classpath = new StringWriter();
      for (File f : libFolder.listFiles()) {
        if (f.getName().toLowerCase().endsWith(".jar") || f.getName().toLowerCase().endsWith(".zip")) {
          classpath.append("$APPDIR/lib/"+f.getName()+":");
        }
      }
      options.add("-cp");
      options.add(classpath.toString().substring(0, classpath.toString().length()-1));
      
      // Class to run
      options.add("jycessing.Runner");
      
      // Runner arguments
      options.add("--noredirect");
      options.add("$APPDIR/source/"+sketch.getCode(0).getFileName());
      
      script.print("$JAVA");
      for (String o : options) {
        script.print(" "+o);
      }
      script.println();
      script.close();
      
      log("Setting script executable.");
      Files.setPosixFilePermissions(scriptFile.toPath(), PosixFilePermissions.fromString("rwxrwxrwx"));
    }
    log("Done.");
  }
}
