package jycessing.mode.export;

import java.io.IOException;
import java.util.Set;

import jycessing.mode.PyEditor;
import jycessing.mode.PythonMode;
import processing.app.Library;
import processing.app.Platform;
import processing.app.Preferences;
import processing.app.Sketch;
import processing.app.ui.ExportPrompt;

/**
 * Class that handles doing the actual exporting. All this currently does is figure out libraries
 * and then hand off to each platform export.
 */
public class Exporter {

  @SuppressWarnings("unused")
  private static void log(final String msg) {
    if (PythonMode.VERBOSE) {
      System.err.println(Exporter.class.getSimpleName() + ": " + msg);
    }
  }

  private final Sketch sketch;
  private final PyEditor editor;

  public Exporter(final PyEditor editor) {
    this.editor = editor;
    this.sketch = editor.getSketch();
  }

  public void export() {
    // Work out the libraries the sketch exports - we only need to do this once.
    final Set<Library> libraries = new ImportExtractor(sketch).getLibraries();

    final String hostVariant = Platform.getVariant();
    for (String variant : Preferences.get(ExportPrompt.EXPORT_VARIANTS).split(",")) {
      // Can only embed Java on the native platform
      boolean embed = variant.equals(hostVariant) &&
        Preferences.getBoolean("export.application.embed_java");

      try {
        if (variant.startsWith("windows-")) {
          new WindowsExport(variant, sketch, editor, libraries, embed).export();
        } else if (variant.startsWith("macos-")) {
          new MacExport(variant, sketch, editor, libraries, embed).export();
        } else if (variant.startsWith("linux-")) {
          new LinuxExport(variant, sketch, editor, libraries, embed).export();
        }
      } catch (final IOException e) {
        e.printStackTrace();
        editor.statusError("Export to " + variant + " failed");
      }
    }

    log("Opening result folder.");
    Platform.openFolder(sketch.getFolder());
  }
}
