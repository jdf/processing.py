package jycessing.mode.export;

import java.util.List;

import processing.app.Library;
import processing.app.Sketch;

public abstract class PlatformExport {
  int id;
  int bits;
  String name;
  
  public abstract void embedJava(Sketch sketch);
  
  public abstract void copyData(Sketch sketch);
  
  public abstract void copyCode(Sketch sketch);
  
  public abstract void copySource(Sketch sketch);
  
  public abstract void createExecutable(Sketch sketch);
  
  public abstract void prepareExportFolder(Sketch sketch);
  
  public abstract void copyLibraries(Sketch sketch, List<Library> libraries);
  
}
