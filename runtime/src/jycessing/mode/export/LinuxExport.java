package jycessing.mode.export;

import java.util.ArrayList;
import java.util.List;
import java.io.File;
import java.io.IOException;

import processing.app.Base;
import processing.app.Library;
import processing.app.Preferences;
import processing.app.Sketch;
import processing.app.SketchCode;
import processing.core.PApplet;
import processing.core.PConstants;

public class LinuxExport extends PlatformExport {

  public LinuxExport(int bits) {
    this.id = PConstants.LINUX;
    this.bits = bits;
    this.name = PConstants.platformNames[id] + bits;
  }
  
  @Override
  public void embedJava(Sketch sketch) {
    // TODO Auto-generated method stub

  }

  @Override
  public void copyData(Sketch sketch) {
    // TODO Auto-generated method stub

  }

  @Override
  public void copyCode(Sketch sketch) {
    // TODO Auto-generated method stub

  }

  @Override
  public void copySource(Sketch sketch) {
    // TODO Auto-generated method stub

  }

  @Override
  public void copyLibraries(Sketch sketch, List<Library> libraries) {
    /*File libFolder = new File(sketch.getFolder(), this.name+"/lib");
    for (Library library : libraries) {
      for (File exportFile : library.getApplicationExports(id, bits)) {
        final String exportName = exportFile.getName();
        if (!exportFile.exists()) {
          System.err.println("The file "+exportName+" is mentioned in the export.txt from "
                        +library+" but does not actually exist.");
          continue;
        }
        try{
          if (exportFile.isDirectory()) {
            
            Base.copyDir(exportFile, new File(libFolder, exportName));
          } else {
            Base.copyFile(exportFile, new File(libFolder, exportName));
          }
        } catch(IOException e){
          e.printStackTrace();
        }
      }
    }*/
  }
  
  
  @Override
  public void createExecutable(Sketch sketch) {
    // TODO Auto-generated method stub

  }
  
  @Override
  public void prepareExportFolder(Sketch sketch) {
    // TODO Auto-generated method stub

  }
  
  public void export() {
 // Work out user preferences and other possibilities we care about
    /*
    // I'm putting these here to tell anyone reading what this method depends on - does that make sense?
    final boolean embedJava = (platform == PApplet.platform) && Preferences.getBoolean("export.application.embed_java");
    final boolean hasData = sketch.hasDataFolder();
    final boolean hasCode = sketch.hasCodeFolder();
    
    // Work out the folders we'll be (maybe) using
    final File destFolder = new File(sketch.getFolder(), "application."+PConstants.platformNames[platform]+bits);
    final File libFolder = new File(destFolder, "lib");
    final File codeFolder = new File(destFolder, "code");
    final File sourceFolder = new File(destFolder, "source");
    final File dataFolder = new File(destFolder, "data");
    final File javaFolder = new File(destFolder, "java");
    
    // Things we need to keep track of
    List<Library> libraries = new ArrayList<Library>(); // Obtained by scraping the python AST, eventually...
    List<String> jarFiles = new ArrayList<String>();    // Things we'll need to add to the export's classpath
    
    // Delete previous export (if the user wants to, and it exists) and make a new one
    pyMode.prepareExportFolder(destFolder);
    
    // Handle embedding java
    if (embedJava) {
      log("Embedding java in export.");
      javaFolder.mkdirs();
      if (platform == PConstants.MACOSX) {
        
      } else if (platform == PConstants.WINDOWS) {
        
      } else if (platform == PConstants.LINUX) {
        Base.copyDir(Base.getJavaHome(), javaFolder);
      } else if (platform == PConstants.OTHER) {
        
      }
    }
    
    // Handle data folder
    if (hasData) {
      log("Copying data folder to export.");
      dataFolder.mkdirs();
      if (platform == PConstants.MACOSX) {
        
      } else if (platform == PConstants.WINDOWS) {
        
      } else if (platform == PConstants.LINUX) {
        Base.copyDir(sketch.getDataFolder(), dataFolder);
      } else if (platform == PConstants.OTHER) {
        
      }
    }
    
    // Handle code folder
    // ...what is the code folder for, exactly?
    if (hasCode) {
      log("Copying code folder to export.");
      codeFolder.mkdirs();
      if (platform == PConstants.MACOSX) {
        
      } else if (platform == PConstants.WINDOWS) {
        
      } else if (platform == PConstants.LINUX) {
        
      } else if (platform == PConstants.OTHER) {
        
      }
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
    // For now, all we have is the core library and the processing.py library
    {
      Library core = new Library(Base.getContentFile("core"));
      libraries.add(core);
      for (Library library : libraries) {
        for (File exportFile : library.getApplicationExports(platform, bits)) {
          final String exportName = exportFile.getName();
          if (!exportFile.exists()) {
            statusError("The file "+exportName+" is mentioned in the export.txt from "
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
    }*/
  }
  
}
