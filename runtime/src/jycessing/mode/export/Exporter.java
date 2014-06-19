package jycessing.mode.export;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import jycessing.mode.PyEditor;
import jycessing.mode.PythonMode;
import processing.app.Base;
import processing.app.Library;
import processing.app.Preferences;
import processing.app.Sketch;
import processing.app.SketchCode;
import processing.core.PApplet;
import processing.core.PConstants;

public class Exporter {
  
  @SuppressWarnings("unused")
  private static void log(final String msg) {
    if (PythonMode.VERBOSE) {
      System.err.println(Exporter.class.getSimpleName() + ": " + msg);
    }
  }
  
  private Sketch sketch;
  private PyEditor editor; // I don't really want to pass this around but there's some functionality I need
  
  public Exporter(PyEditor editor, Sketch sketch){
    this.sketch = sketch;
    this.editor = editor;
  }
  
  public void export() {
    // Do export-common things - work out libraries, etc.
    List<Library> libraries = new ArrayList<Library>();
    
    // Now, do this for each platform:
    try {
      new LinuxExport(64, sketch, libraries).export();
    } catch (IOException e) {
      e.printStackTrace();
      editor.statusError("Export failed!");
    }
  }
}
