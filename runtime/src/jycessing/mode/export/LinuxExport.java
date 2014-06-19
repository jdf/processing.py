package jycessing.mode.export;

import java.util.ArrayList;
import java.util.List;
import java.io.File;
import java.io.IOException;

import jycessing.mode.PythonMode;
import jycessing.mode.run.SketchRunner;
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
  
  public LinuxExport(int bits, Sketch sketch, List<Library> libraries) {
    this.id = PConstants.LINUX;
    this.bits = bits;
    this.name = PConstants.platformNames[id] + bits;
    this.sketch = sketch;
    this.libraries = libraries;
  }
  
  public void export() throws IOException {
    // Work out user preferences and other possibilities we care about
    final boolean embedJava = (id == PApplet.platform) && Preferences.getBoolean("export.application.embed_java");
    final boolean hasData = sketch.hasDataFolder();
    final boolean hasCode = sketch.hasCodeFolder();
    final boolean deletePrevious = Preferences.getBoolean("export.delete_target_folder");
    
    // Work out the folders we'll be (maybe) using
    final File destFolder = new File(sketch.getFolder(), "application."+name);
    final File libFolder = new File(destFolder, "lib");
    final File codeFolder = new File(destFolder, "code");
    final File sourceFolder = new File(destFolder, "source");
    final File dataFolder = new File(destFolder, "data");
    final File javaFolder = new File(destFolder, "java");
        
    // Delete previous export (if the user wants to, and it exists) and make a new one
    if (deletePrevious) {
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
      Library core = new Library(Base.getContentFile("core"));
      libraries.add(core);
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
    
    // Make shell script
  }
}
