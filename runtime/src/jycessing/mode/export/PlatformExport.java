package jycessing.mode.export;

import java.io.IOException;

public abstract class PlatformExport {
  int id;
  int bits;
  String name;
  
  public abstract void export() throws IOException;
  
}
