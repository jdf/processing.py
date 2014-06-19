package jycessing.mode.export;

import java.util.List;
import java.io.File;
import java.io.IOException;

import processing.app.Base;
import processing.app.Library;
import processing.app.Sketch;
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

}
