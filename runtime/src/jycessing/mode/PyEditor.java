package jycessing.mode;

import java.awt.Point;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseWheelEvent;
import java.awt.event.MouseWheelListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.UUID;
import java.util.regex.Pattern;

import javax.swing.AbstractAction;
import javax.swing.JMenu;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;

import jycessing.DisplayType;
import jycessing.IOUtil;
import jycessing.mode.export.ExportDialog;
import jycessing.mode.run.PdeSketch;
import jycessing.mode.run.PdeSketch.LocationType;
import jycessing.mode.run.SketchService;
import jycessing.mode.run.SketchServiceManager;
import jycessing.mode.run.SketchServiceProcess;
import processing.app.Base;
import processing.app.Formatter;
import processing.app.Language;
import processing.app.Library;
import processing.app.Messages;
import processing.app.Mode;
import processing.app.Platform;
import processing.app.SketchCode;
import processing.app.SketchException;
import processing.app.ui.Editor;
import processing.app.ui.EditorException;
import processing.app.ui.EditorState;
import processing.app.ui.EditorToolbar;
import processing.app.ui.Toolkit;

@SuppressWarnings("serial")
public class PyEditor extends Editor {

  @SuppressWarnings("unused")
  private static void log(final String msg) {
    if (PythonMode.VERBOSE) {
      System.err.println(PyEditor.class.getSimpleName() + ": " + msg);
    }
  }

  /**
   * Every PyEditor has a UUID that the {@link SketchServiceManager} uses to
   * route events from the {@link SketchService} to its owning editor.
   */
  private final String id;

  private final PythonMode pyMode;
  private final PyInputHandler inputHandler;
  private final SketchServiceProcess sketchService;

  /**
   * If the user runs a dirty sketch, we create a temp dir containing the
   * modified state of the sketch and run it from there. We keep track
   * of it in this variable in order to delete it when done running.
   */
  private Path tempSketch;


  protected PyEditor(final Base base, final String path, final EditorState state, final Mode mode)
      throws EditorException {
    super(base, path, state, mode);

    id = UUID.randomUUID().toString();
    inputHandler = new PyInputHandler(this);
    pyMode = (PythonMode)mode;

    // Provide horizontal scrolling.
    textarea.addMouseWheelListener(createHorizontalScrollListener());

    // Create a sketch service affiliated with this editor.
    final SketchServiceManager sketchServiceManager = pyMode.getSketchServiceManager();
    sketchService = sketchServiceManager.createSketchService(this);

    // Ensure that the sketch service gets properly destroyed when either the
    // JVM terminates or this editor closes, whichever comes first.
    final Thread cleanup = new Thread(new Runnable() {
      @Override
      public void run() {
        sketchServiceManager.destroySketchService(PyEditor.this);
      }
    });
    Runtime.getRuntime().addShutdownHook(cleanup);
    addWindowListener(new WindowAdapter() {
      @Override
      public void windowClosing(final WindowEvent e) {
        cleanup.run();
        Runtime.getRuntime().removeShutdownHook(cleanup);
      }
    });
  }

  public String getId() {
    return id;
  }

  private MouseWheelListener createHorizontalScrollListener() {
    return new MouseWheelListener() {
      @Override
      public void mouseWheelMoved(final MouseWheelEvent e) {
        if (e.getScrollType() == MouseWheelEvent.WHEEL_UNIT_SCROLL && e.isShiftDown()) {
          final int current = textarea.getHorizontalScrollPosition();
          final int delta = e.getUnitsToScroll() * 6;
          textarea.setHorizontalScrollPosition(current + delta);
        }
      }
    };
  }

  @Override
  public String getCommentPrefix() {
    return "# ";
  }

  @Override
  public void internalCloseRunner() {
    try {
      sketchService.stopSketch();
    } catch (final SketchException e) {
      statusError(e);
    } finally {
      cleanupTempSketch();
    }
  }

  private void cleanupTempSketch() {
    if (tempSketch != null) {
      if (tempSketch.toFile().exists()) {
        try {
          log("Deleting " + tempSketch);
          IOUtil.rm(tempSketch);
          log("Deleted " + tempSketch);
          assert (!tempSketch.toFile().exists());
        } catch (final IOException e) {
          System.err.println(e);
        }
      }
      tempSketch = null;
    }
  }

  /**
   * Build menus.
   */
  @Override
  public JMenu buildFileMenu() {
    final String appTitle = Language.text("Export Application");
    final JMenuItem exportApplication = Toolkit.newJMenuItem(appTitle, 'E');
    exportApplication.addActionListener(new ActionListener() {
      @Override
      public void actionPerformed(final ActionEvent e) {
        handleExportApplication();
      }
    });
    return buildFileMenu(new JMenuItem[] {exportApplication});
  }

  @Override
  public JMenu buildHelpMenu() {
    final JMenu menu = new JMenu("Help");
    menu.add(new JMenuItem(new AbstractAction("Report a bug in Python Mode") {
      @Override
      public void actionPerformed(final ActionEvent e) {
        Platform.openURL("http://github.com/jdf/processing.py-bugs/issues");
      }
    }));
    menu.add(new JMenuItem(new AbstractAction("Contribute to Python Mode") {
      @Override
      public void actionPerformed(final ActionEvent e) {
        Platform.openURL("http://github.com/jdf/processing.py");
      }
    }));
    return menu;
  }

  @Override
  public JMenu buildSketchMenu() {
    final JMenuItem runItem = Toolkit.newJMenuItem(Language.text("toolbar.run"), 'R');
    runItem.addActionListener(new ActionListener() {
      @Override
      public void actionPerformed(final ActionEvent e) {
        handleRun();
      }
    });

    final JMenuItem presentItem = Toolkit.newJMenuItemShift(Language.text("toolbar.present"), 'R');
    presentItem.addActionListener(new ActionListener() {
      @Override
      public void actionPerformed(final ActionEvent e) {
        handlePresent();
      }
    });

    final JMenuItem stopItem = new JMenuItem(Language.text("toolbar.stop"));
    stopItem.addActionListener(new ActionListener() {
      @Override
      public void actionPerformed(final ActionEvent e) {
        handleStop();
      }
    });

    return buildSketchMenu(new JMenuItem[] {runItem, presentItem, stopItem});
  }

  @Override
  public Formatter createFormatter() {
    return pyMode.getFormatter();
  }

  @Override
  public EditorToolbar createToolbar() {
    return new PyToolbar(this);
  }

  /**
   * TODO(James Gilles): Create this!
   * Create export GUI and hand off results to performExport()
   */
  public void handleExportApplication() {
    // Leaving this here because it seems like it's more the editor's responsibility
    if (sketch.isModified()) {
      final Object[] options = {"OK", "Cancel"};
      final int result =
          JOptionPane
              .showOptionDialog(this, "Save changes before export?", "Save",
                  JOptionPane.OK_CANCEL_OPTION, JOptionPane.QUESTION_MESSAGE, null, options,
                  options[0]);
      if (result == JOptionPane.OK_OPTION) {
        handleSave(true);
      } else {
        statusNotice("Export canceled, changes must first be saved.");
      }
    }

    new ExportDialog(this, sketch).go();
  }

  public File getModeContentFile(final String filename) {
    return pyMode.getContentFile(filename);
  }

  public File getSplashFile() {
    return pyMode.getContentFile("theme/splash.png");
  }

  /**
   * Save the current state of the sketch code into a temp dir, and return
   * the created directory.
   * @return a new directory containing a saved version of the current
   * (presumably modified) sketch code.
   * @throws IOException
   */
  private Path createTempSketch() throws IOException {
    final Path tmp = Files.createTempDirectory(sketch.getName());
    for (final SketchCode code : sketch.getCode()) {
      Files.write(tmp.resolve(code.getFileName()), code.getProgram().getBytes("utf-8"));
    }
    return tmp;
  }

  private void runSketch(final DisplayType displayType) {
    prepareRun();
    toolbar.activateRun();
    final File sketchPath;
    if (sketch.isModified()) {
      log("Sketch is modified; must copy it to temp dir.");
      final String sketchMainFileName = sketch.getCode(0).getFile().getName();
      try {
        tempSketch = createTempSketch();
        sketchPath = tempSketch.resolve(sketchMainFileName).toFile();
      } catch (final IOException e) {
        Messages.showError("Sketchy Behavior", "I can't copy your unsaved work\n"
            + "to a temp directory.", e);
        return;
      }
    } else {
      sketchPath = sketch.getCode(0).getFile().getAbsoluteFile();
    }

    final LocationType locationType;
    final Point location;
    if (getSketchLocation() != null) {
      locationType = LocationType.SKETCH_LOCATION;
      location = new Point(getSketchLocation());
    } else { // assume editor has a position - is that safe?
      locationType = LocationType.EDITOR_LOCATION;
      location = new Point(getLocation());
    }

    try {
      sketchService
          .runSketch(new PdeSketch(sketch, sketchPath, displayType, location, locationType));
    } catch (final SketchException e) {
      statusError(e);
    }
  }

  @Override
  public void deactivateRun() {
    restoreToolbar();
    cleanupTempSketch();
  }

  public void handleRun() {
    runSketch(DisplayType.WINDOWED);
  }

  public void handlePresent() {
    runSketch(DisplayType.PRESENTATION);
  }

  public void handleStop() {
    toolbar.activateStop();
    internalCloseRunner();
    restoreToolbar();
    requestFocus();
  }

  private void restoreToolbar() {
    // toolbar.deactivate(PyToolbar.SAVE);
    toolbar.deactivateStop();
    toolbar.deactivateRun();
    toFront();
  }

  public void handleSave() {
    // toolbar.activate(PyToolbar.SAVE);
    super.handleSave(true);
    restoreToolbar();
    recolor();
  }

  @Override
  public boolean handleSaveAs() {
    // toolbar.activate(PyToolbar.SAVE);
    final boolean result = super.handleSaveAs();
    restoreToolbar();
    return result;
  }

  @Override
  public void statusError(final String what) { // sketch died for some reason
    super.statusError(what);
    restoreToolbar();
  }

  @Override
  public void handleImportLibrary(final String libraryName) {
    sketch.ensureExistence();

    final Library lib = mode.findLibraryByName(libraryName);
    if (lib == null) {
      statusError("Unable to locate library: " + libraryName);
      return;
    }

    final String name = new File(lib.getJarPath()).getParentFile().getParentFile().getName();
    if (Pattern.compile("^add_library\\(\\s*'" + name + "'\\s*\\)\\s*$", Pattern.MULTILINE)
        .matcher(getText()).find()) {
      return;
    }
    setSelection(0, 0); // scroll to start
    setSelectedText(String.format("add_library('%s')\n", name));
    sketch.setModified(true);
    recolor();
  }

  @Override
  public void handleIndentOutdent(final boolean increase) {
    inputHandler.indent(increase ? 1 : -1);
  }

  @Override
  public void handleAutoFormat() {
    super.handleAutoFormat();
    recolor();
  }

  @Override
  public void handlePaste() {
    super.handlePaste();
    recolor();
  }

  @Override
  public void handleCut() {
    super.handleCut();
    recolor();
  }

  @Override
  protected void handleCommentUncomment() {
    super.handleCommentUncomment();
    recolor();
  }

  private void recolor() {
    textarea.getDocument().tokenizeLines();
  }

  public void printOut(final String msg) {
    console.message(msg, false);
  }

  public void printErr(final String msg) {
    console.message(msg, true);
  }
}
