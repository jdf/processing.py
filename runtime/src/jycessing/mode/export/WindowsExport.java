package jycessing.mode.export;

import java.io.IOException;
import java.util.List;

import processing.app.Library;
import processing.app.Sketch;
import processing.core.PConstants;
import jycessing.mode.PyEditor;
import jycessing.mode.PythonMode;

public class WindowsExport extends PlatformExport {

  private static void log(final String msg) {
    if (PythonMode.VERBOSE) {
      System.err.println(WindowsExport.class.getSimpleName() + ": " + msg);
    }
  }
  
  
  private Sketch sketch;
  private List<Library> libraries;
  private PyEditor editor;
  private int bits;

  public WindowsExport(int bits, Sketch sketch, PyEditor editor, List<Library> libraries) {
    this.id = PConstants.WINDOWS;
    this.bits = bits;
    this.name = PConstants.platformNames[id] + bits;
    this.sketch = sketch;
    this.editor = editor;
    this.libraries = libraries;
  }
  
  @Override
  public void export() throws IOException {
    log("I would do a windows export here... if I knew how :(");
  }
  
}
