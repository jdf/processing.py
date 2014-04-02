package jycessing.mode;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.PrintStream;
import java.util.regex.Pattern;

import javax.swing.JMenu;
import javax.swing.JMenuItem;

import org.python.core.PyException;

import jycessing.Runner;
import processing.app.Base;
import processing.app.Editor;
import processing.app.EditorState;
import processing.app.EditorToolbar;
import processing.app.Formatter;
import processing.app.Mode;
import processing.app.Toolkit;

@SuppressWarnings("serial")
public class PyEditor extends Editor {

  final PythonMode pyMode;
  final PyKeyListener listener;
  Thread runner;

  protected PyEditor(final Base base, final String path, final EditorState state, final Mode mode) {
    super(base, path, state, mode);

    listener = new PyKeyListener(this, textarea);
    pyMode = (PythonMode)mode;
  }

  @Override
  public String getCommentPrefix() {
    return "#";
  }

  @Override
  public void internalCloseRunner() {
    if (runner != null) {
      runner.interrupt();
      runner = null;
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
    return buildFileMenu(new JMenuItem[] { exportApplication });
  }

  @Override
  public JMenu buildHelpMenu() {
    final JMenu menu = new JMenu("Help");
    final JMenuItem item = new JMenuItem("Patches welcome");
    item.setEnabled(false);
    menu.add(item);
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

    return buildSketchMenu(new JMenuItem[] { runItem, presentItem, stopItem });
  }

  @Override
  public Formatter createFormatter() {
    unimplemented("createFormatter");
    return null;
  }

  @Override
  public EditorToolbar createToolbar() {
    return new PyToolbar(this, base);
  }

  /**
   * TODO(Adam Parrish): Create this!
   */
  public void handleExportApplication() {
    Base.showMessage("Sorry", "You can't do that yet.");
  }

  private enum RunMode {
    WINDOWED {
      @Override
      public String[] args(String sketchPath, final int x, final int y) {
        return new String[] { String.format("--editor-location=%d,%d", x, y), sketchPath };
      }
    },
    PRESENTATION {
      @Override
      public String[] args(String sketchPath, final int x, final int y) {
        return new String[] { "--present", "--external", sketchPath };
      }
    };
    abstract public String[] args(final String sketchPath, final int x, final int y);
  }

  // Ignore __MOVE__.
  // TODO(feinberg): Listen to __MOVE__.
  private static class MoveCommandFilteringPrintStream extends PrintStream {
    private static final Pattern IGNORE = Pattern.compile("^__MOVE__\\s+(.*)$");

    public MoveCommandFilteringPrintStream(final PrintStream wrapped) {
      super(wrapped);
    }

    @Override
    public void println(String s) {
      if (!IGNORE.matcher(s).matches()) {
        super.print(s);
      }
    }
  }

  private void runSketch(final RunMode mode) {
    final String sketchPath = getSketch().getCurrentCode().getFile().getAbsolutePath();
    if (runner != null) {
      internalCloseRunner();
    }
    prepareRun();
    runner = new Thread(new Runnable() {
      @Override
      public void run() {
        try {
          final PrintStream syserr = System.err;
          System.setErr(new MoveCommandFilteringPrintStream(syserr));
          try {
            Runner.runSketchBlocking(Base.getSketchbookLibrariesFolder(), mode.args(sketchPath,
                getX(), getY()), sketchPath, getSketch().getCurrentCode().getProgram());
          } finally {
            System.setErr(syserr);
          }
        } catch (PyException e) {
          System.err.println(e.getMessage());
          System.err.println(e.getCause());
        } catch (Exception e) {
          throw new RuntimeException(e);
        } finally {
          handleStop();
        }
      }
    }, "processing.py mode runner");
    runner.start();
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
    toolbar.deactivate(PyToolbar.STOP);
    toolbar.deactivate(PyToolbar.RUN);
    toFront();
  }

  public void handleSave() {
    toolbar.activate(PyToolbar.SAVE);
    super.handleSave(true);
    toolbar.deactivate(PyToolbar.SAVE);
  }

  @Override
  public boolean handleSaveAs() {
    toolbar.activate(PyToolbar.SAVE);
    final boolean result = super.handleSaveAs();
    toolbar.deactivate(PyToolbar.SAVE);
    return result;
  }

  @Override
  public void statusError(final String what) { // sketch died for some reason
    super.statusError(what);
    deactivateRun();
  }

  @Override
  public void deactivateRun() {
    toolbar.deactivate(PyToolbar.RUN);
  }

  @Override
  public void handleImportLibrary(final String jarPath) {
    unimplemented("handleImportLibrary");
  }

  private void unimplemented(final String what) {
    throw new RuntimeException("Here is something I don't know how to do: " + what);
  }

}