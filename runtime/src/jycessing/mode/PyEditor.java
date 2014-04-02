package jycessing.mode;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

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

/**
 * 
 */
@SuppressWarnings("serial")
public class PyEditor extends Editor {

  final ProcessingDotPyMode pyMode;
  final PyKeyListener listener;
  Thread runner;

  protected PyEditor(final Base base, final String path, final EditorState state, final Mode mode) {
    super(base, path, state, mode);

    listener = new PyKeyListener(this, textarea);
    pyMode = (ProcessingDotPyMode)mode;
  }

  @Override
  public String getCommentPrefix() {
    return "#";
  }

  @Override
  public void internalCloseRunner() {
    if (runner != null) {
      System.err.println("Interrupting runner.");
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
   * Handlers
   */
  public void handleExportApplication() {
    Base.showMessage("Sorry", "You can't do that yet.");
  }

  public void handleRun() {
    toolbar.activate(PyToolbar.RUN);
    final String sketchPath = getSketch().getCurrentCode().getFile().getAbsolutePath();
    runner = new Thread(new Runnable() {
      @Override
      public void run() {
        prepareRun();
        final String[] args = new String[] { "--external", sketchPath };
        try {
          Runner.runSketchBlocking(Base.getSketchbookLibrariesFolder(), args, sketchPath,
              getSketch().getCurrentCode().getProgram());
        } catch (PyException e) {
          System.err.println(e.getMessage());
          System.err.println(e.getCause());
        } catch (Exception e) {
          throw new RuntimeException(e);
        }
      }
    }, "processing.py mode runner");
    runner.start();
  }

  public void handlePresent() {
    unimplemented("handlePresent");
    toolbar.activate(PyToolbar.RUN);
    new Thread(new Runnable() {
      @Override
      public void run() {
        prepareRun();
      }
    }).start();
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