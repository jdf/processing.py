package jycessing.mode.export;

import java.io.IOException;

/**
 * 
 * Subclass this to add more platforms, if we ever want to add freebsd or haiku or something
 *
 */
public abstract class PlatformExport {
  int id;
  String name;
  
  public abstract void export() throws IOException;
  
}
