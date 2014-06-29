package jycessing.mode.export;

import java.io.IOException;

public abstract class PlatformExport {
  int id;
  String name;
  
  public abstract void export() throws IOException;
  
}
