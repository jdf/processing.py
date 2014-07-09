package jycessing.mode.export;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;

import jycessing.mode.PyEditor;
import jycessing.mode.PythonMode;
import processing.app.Base;
import processing.app.Library;
import processing.app.Preferences;
import processing.app.Sketch;

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
    Set<Library> libraries = new ImportExtractor(sketch).getLibraries();
    
    // Now, do this for each platform:
    if (Preferences.getBoolean("export.application.platform.linux")) {
      try {
        new LinuxExport(Arch.X86, sketch, editor, libraries).export();
      } catch (IOException e) {
        e.printStackTrace();
        editor.statusError("Export to linux32 failed!");
      }
      try {
        new LinuxExport(Arch.AMD64, sketch, editor, libraries).export();
      } catch (IOException e) {
        e.printStackTrace();
        editor.statusError("Export to linux64 failed!");
      }
    }
    if (Preferences.getBoolean("export.application.platform.windows")) {
      try {
        new WindowsExport(Arch.X86, sketch, editor, libraries).export();
      } catch (IOException e) {
        e.printStackTrace();
        editor.statusError("Export to windows32 failed!");
      }
      try {
        new WindowsExport(Arch.AMD64, sketch, editor, libraries).export();
      } catch (IOException e) {
        e.printStackTrace();
        editor.statusError("Export to windows64 failed!");
      }
    }
    if (Preferences.getBoolean("export.application.platform.macosx")) {
      try {
        new MacExport(sketch, editor, libraries).export();
      } catch (IOException e) {
        e.printStackTrace();
        editor.statusError("Export to macosx failed!");
      }
    }
    log("Opening result folder.");
    Base.openFolder(sketch.getFolder());
  }
}
