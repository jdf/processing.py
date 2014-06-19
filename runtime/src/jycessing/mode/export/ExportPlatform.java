package jycessing.mode.export;

import processing.app.Sketch;

public abstract class ExportPlatform {
  int id;
  int bits;
  String name;
  
  public void embedJava(Sketch sketch) {}
  
  public void copyData(Sketch sketch) {}
  
  public void copyCode(Sketch sketch) {}
  
  public void copySource(Sketch sketch) {}
  
  public void createExecutable(Sketch sketch) {}
  
}
