package jycessing.mode.export;

import java.io.IOException;
import java.util.Set;

import jycessing.mode.PyEditor;
import jycessing.mode.PythonMode;
import processing.app.Library;
import processing.app.Sketch;
import processing.core.PConstants;


/**
 * 
 * A Mac export.
 * TODO implement.
 *
 */
public class MacExport extends PlatformExport {
  public static final Arch arch = Arch.AMD64; // macs only run x86_64 nowadays

  private static void log(final String msg) {
    if (PythonMode.VERBOSE) {
      System.err.println(MacExport.class.getSimpleName() + ": " + msg);
    }
  }
  
  private final Sketch sketch;
  private final Set<Library> libraries;
  private final PyEditor editor;
  
  public MacExport(Sketch sketch, PyEditor editor, Set<Library> libraries) {
    this.id = PConstants.MACOSX;
    this.name = PConstants.platformNames[id];
    this.sketch = sketch;
    this.editor = editor;
    this.libraries = libraries;
  }
  
  @Override
  public void export() throws IOException {
    log("I would do a mac export here... if I knew how :(");

  }

}
