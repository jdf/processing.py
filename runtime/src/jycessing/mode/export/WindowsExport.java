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
 * Perform an export to Windows.
 * TODO implement.
 *
 */
public class WindowsExport extends PlatformExport {

  private static void log(final String msg) {
    if (PythonMode.VERBOSE) {
      System.err.println(WindowsExport.class.getSimpleName() + ": " + msg);
    }
  }
  
  private final Sketch sketch;
  private final Set<Library> libraries;
  private final PyEditor editor;
  private final Arch arch;

  public WindowsExport(Arch arch, Sketch sketch, PyEditor editor, Set<Library> libraries) {
    this.id = PConstants.WINDOWS;
    this.arch = arch;
    this.name = PConstants.platformNames[id] + arch.bits;
    this.sketch = sketch;
    this.editor = editor;
    this.libraries = libraries;
  }
  
  @Override
  public void export() throws IOException {
    log("I would do a windows export here... if I knew how :(");
  }
  
}
