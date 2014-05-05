package jycessing.mode;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ComponentAdapter;
import java.awt.event.ComponentEvent;
import java.awt.event.MouseWheelEvent;
import java.awt.event.MouseWheelListener;
import java.io.File;
import java.util.regex.Pattern;

import javax.swing.AbstractAction;
import javax.swing.JMenu;
import javax.swing.JMenuItem;

import jycessing.Runner.LibraryPolicy;
import jycessing.mode.run.SketchInfo;
import processing.app.Base;
import processing.app.Editor;
import processing.app.EditorState;
import processing.app.EditorToolbar;
import processing.app.Formatter;
import processing.app.Mode;
import processing.app.SketchCode;
import processing.app.SketchException;
import processing.app.Toolkit;

@SuppressWarnings("serial")
public class PyEditor extends Editor {

  final PythonMode pyMode;
  final PyKeyListener keyListener;
  Thread runner;
  boolean didAddHorizontalScrollListener = false;

  protected PyEditor(final Base base, final String path, final EditorState state, final Mode mode) {
    super(base, path, state, mode);

    keyListener = new PyKeyListener(this, textarea);
    pyMode = (PythonMode)mode;
    // Provide horizontal scrolling.
    addComponentListener(new ComponentAdapter() {
      @Override
      public void componentResized(final ComponentEvent e) {
        if (!didAddHorizontalScrollListener) {
          textarea.addMouseWheelListener(createHorizontalScrollListener());
          didAddHorizontalScrollListener = true;
        }
      }

    });
  }

  private MouseWheelListener createHorizontalScrollListener() {
    return new MouseWheelListener() {
      @Override
      public void mouseWheelMoved(final MouseWheelEvent e) {
        if (e.getScrollType() == MouseWheelEvent.WHEEL_UNIT_SCROLL && e.isShiftDown()) {
          final int current = textarea.getHorizontalScrollPosition();
          final int delta = e.getUnitsToScroll() * 6;
          textarea.setHorizontalScrollPosition(Math.max(0, current + delta));
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
      pyMode.getSketchServiceManager().stopSketch();
    } catch (final SketchException e) {
      statusError(e);
    }
  }

  /**
   * Build menus.
   */
  @Override
  public JMenu buildFileMenu() {
    final String appTitle = PyToolbar.getTitle(PyToolbar.EXPORT, false);
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
        Base.openURL("http://github.com/jdf/processing.py-bugs/issues");
      }
    }));
    menu.add(new JMenuItem(new AbstractAction("Contribute to Python Mode") {
      @Override
      public void actionPerformed(final ActionEvent e) {
        Base.openURL("http://github.com/jdf/processing.py");
      }
    }));
    return menu;
  }

  @Override
  public JMenu buildSketchMenu() {
    final JMenuItem runItem = Toolkit.newJMenuItem(PyToolbar.getTitle(PyToolbar.RUN, false), 'R');
    runItem.addActionListener(new ActionListener() {
      @Override
      public void actionPerformed(final ActionEvent e) {
        handleRun();
      }
    });

    final JMenuItem presentItem =
        Toolkit.newJMenuItemShift(PyToolbar.getTitle(PyToolbar.RUN, true), 'R');
    presentItem.addActionListener(new ActionListener() {
      @Override
      public void actionPerformed(final ActionEvent e) {
        handlePresent();
      }
    });

    final JMenuItem stopItem = new JMenuItem(PyToolbar.getTitle(PyToolbar.STOP, false));
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
    return new PyToolbar(this, base);
  }

  /**
   * TODO(James Gilles): Create this!
   */
  public void handleExportApplication() {
    Base.showMessage("Sorry", "You can't do that yet.");
  }

  private void runSketch(final RunMode mode) {
    prepareRun();
    final SketchCode code = getSketch().getCode(0);
    final String sketchPath = code.getFile().getAbsolutePath();
    try {
      final String[] codePaths = new String[sketch.getCodeCount()];
      for (int i = 0; i < codePaths.length; i++) {
        codePaths[i] = sketch.getCode(i).getFile().getAbsolutePath();
      }
      final SketchInfo info =
          new SketchInfo.Builder().runMode(mode)
              .addLibraryDir(Base.getContentFile("modes/java/libraries"))
              .addLibraryDir(Base.getSketchbookLibrariesFolder())
              .sketch(new File(sketchPath).getAbsoluteFile()).code(code.getProgram())
              .codePaths(codePaths).x(getX()).y(getY()).libraryPolicy(LibraryPolicy.SELECTIVE)
              .build();
      pyMode.getSketchServiceManager().runSketch(this, info);
    } catch (final SketchException e) {
      statusError(e);
    }
  }

  @Override
  public void deactivateRun() {
    restoreToolbar();
  }

  public void handleRun() {
    toolbar.activate(PyToolbar.RUN);
    runSketch(RunMode.WINDOWED);
  }

  public void handlePresent() {
    toolbar.activate(PyToolbar.RUN);
    runSketch(RunMode.PRESENTATION);
  }

  public void handleStop() {
    toolbar.activate(PyToolbar.STOP);
    internalCloseRunner();
    restoreToolbar();
    requestFocus();
  }

  private void restoreToolbar() {
    toolbar.deactivate(PyToolbar.SAVE);
    toolbar.deactivate(PyToolbar.STOP);
    toolbar.deactivate(PyToolbar.RUN);
    toFront();
  }

  public void handleSave() {
    toolbar.activate(PyToolbar.SAVE);
    super.handleSave(true);
    restoreToolbar();
    recolor();
  }

  @Override
  public boolean handleSaveAs() {
    toolbar.activate(PyToolbar.SAVE);
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
  public void handleImportLibrary(final String jarPath) {
    sketch.ensureExistence();
    final String name = new File(jarPath).getParentFile().getParentFile().getName();
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
    keyListener.indent(increase ? 1 : -1);
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
}
