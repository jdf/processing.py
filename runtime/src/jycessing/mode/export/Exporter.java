package jycessing.mode.export;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import jycessing.mode.PyEditor;
import jycessing.mode.PythonMode;
import processing.app.Base;
import processing.app.Library;
import processing.app.Preferences;
import processing.app.Sketch;
import processing.app.SketchCode;
import processing.core.PApplet;
import processing.core.PConstants;

public class Exporter {
  
  @SuppressWarnings("unused")
  private static void log(final String msg) {
    if (PythonMode.VERBOSE) {
      System.err.println(Exporter.class.getSimpleName() + ": " + msg);
    }
  }
  
  private Sketch sketch;
  private PyEditor editor; // I don't really want to pass this around but there's some functionality I need
  
  public Exporter(PyEditor editor, Sketch sketch){
    this.sketch = sketch;
  }
  
  public void export() {
    
  }
  
  private void exportTo(ExportPlatform platform) throws IOException {
    
    log("Exporting to "+platform.name);
    
    // Work out user preferences and other possibilities we care about
    // I'm putting these here to tell anyone reading what this method depends on - does that make sense?
    final boolean embedJava = (platform.id == PApplet.platform) && Preferences.getBoolean("export.application.embed_java");
    final boolean hasData = sketch.hasDataFolder();
    final boolean hasCode = sketch.hasCodeFolder();
    
    // Work out the folders we'll be (maybe) using
    final File destFolder = new File(sketch.getFolder(), "application."+platform.name);
    final File libFolder = new File(destFolder, "lib");
    
    // Things we need to keep track of
    List<Library> libraries = new ArrayList<Library>(); // Obtained by scraping the python AST, eventually...
    List<String> jarFiles = new ArrayList<String>();    // Things we'll need to add to the export's classpath
    
    // Delete previous export (if the user wants to, and it exists) and make a new one
    // pyMode.prepareExportFolder(destFolder);
    
    // Handle embedding java
    if (embedJava) {
      log("Embedding java in export.");
      platform.embedJava(sketch);
    }
    
    // Handle data folder
    if (hasData) {
      log("Copying data folder to export.");
      platform.copyData(sketch);
    }
    
    // Handle code folder
    // ...what is the code folder for, exactly?
    if (hasCode) {
      log("Copying code folder to export.");
      platform.copyCode(sketch);
    }
    
    // Handle source folder
    {
      log("Copying source to export.");
      platform.copySource(sketch);
    }
    
    // Handle imported libraries
    // For now, all we have is the core library
    {
      Library core = new Library(Base.getContentFile("core"));
      libraries.add(core);
      
      for (Library library : libraries) {
        for (File exportFile : library.getApplicationExports(platform.id, platform.bits)) {
          final String exportName = exportFile.getName();
          if (!exportFile.exists()) {
            System.err.println("The file "+exportName+" is mentioned in the export.txt from "
                          +library+" but does not actually exist.");
            continue;
          }
          if (exportFile.isDirectory()) {
            Base.copyDir(exportFile, new File(libFolder, exportName));
          } else if (exportName.toLowerCase().endsWith(".jar") || exportName.toLowerCase().endsWith(".zip")) {
            jarFiles.add(exportName);
            Base.copyFile(exportFile, new File(libFolder, exportName));
          } else {
            Base.copyFile(exportFile, new File(libFolder, exportName));
          }
        }
      }
    }
    
    // Add Python Mode stuff (pymode jar, guava, jython jar, jython license)
    // [If we restructured the mode code as a P5 library this could be folded into the above]
    for (File exportFile : editor.getRequiredFiles()){
      if (exportFile.getName().toLowerCase().endsWith(".jar")) {
        jarFiles.add(exportFile.getName());
      }
      Base.copyFile(exportFile, new File(libFolder, exportFile.getName()));
    }
    
    platform.createExecutable(sketch);
  }
}
