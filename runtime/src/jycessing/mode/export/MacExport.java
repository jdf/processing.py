package jycessing.mode.export;

import java.io.IOException;
import java.util.List;

import processing.app.Library;
import processing.app.Sketch;
import processing.core.PConstants;
import jycessing.mode.PyEditor;
import jycessing.mode.PythonMode;

public class MacExport extends PlatformExport {

  private static void log(final String msg) {
    if (PythonMode.VERBOSE) {
      System.err.println(MacExport.class.getSimpleName() + ": " + msg);
    }
  }
  
  private final Sketch sketch;
  private final List<Library> libraries;
  private final PyEditor editor;
  
  public MacExport(Sketch sketch, PyEditor editor, List<Library> libraries) {
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
