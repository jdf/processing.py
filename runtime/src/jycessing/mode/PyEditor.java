package jycessing.mode;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.net.Socket;
import java.util.regex.Pattern;

import javax.swing.JMenu;
import javax.swing.JMenuItem;

import jycessing.PreparedPythonSketch;
import jycessing.PythonSketchError;
import jycessing.Runner;
import jycessing.Runner.LibraryPolicy;
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
  final PyKeyListener listener;
  Thread runner;

  protected PyEditor(final Base base, final String path, final EditorState state, final Mode mode) {
    super(base, path, state, mode);

    listener = new PyKeyListener(this, textarea);
    pyMode = (PythonMode)mode;
  }

  @Override
  public String getCommentPrefix() {
    return "# ";
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
    return new Formatter() {
      @Override
      public String format(String text) {
        try {
          final Socket sock = new Socket("localhost", 10011);
          try {
            final DataOutputStream out = new DataOutputStream(sock.getOutputStream());
            BufferedReader in =
                new BufferedReader(new InputStreamReader(sock.getInputStream(), "utf-8"));

            final byte[] encoded = text.getBytes("utf-8");
            out.writeInt(encoded.length);
            out.write(encoded);
            out.flush();

            final StringBuilder sb = new StringBuilder();
            String line;
            while ((line = in.readLine()) != null) {
              sb.append(line).append("\n");
            }
            return sb.toString();
          } finally {
            sock.close();
          }
        } catch (IOException e) {
          System.err.println(e);
          return text;
        }
      }
    };
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
        super.println(s);
      }
    }
  }

  private void runSketch(final RunMode mode) {
    final String sketchPath = getSketch().getCurrentCode().getFile().getAbsolutePath();
    prepareRun();
    runner = new Thread(new Runnable() {
      @Override
      public void run() {
        try {
          final PreparedPythonSketch sketch =
              Runner.prepareSketch(Base.getSketchbookLibrariesFolder(), LibraryPolicy.SELECTIVE,
                  mode.args(sketchPath, getX(), getY()), sketchPath, getSketch().getCurrentCode()
                      .getProgram());
          final PrintStream syserr = System.err;
          System.setErr(new MoveCommandFilteringPrintStream(syserr));
          try {
            sketch.runBlocking();
          } finally {
            System.setErr(syserr);
          }
        } catch (PythonSketchError e) {
          statusError(convertPythonSketchError(e));
        } catch (Exception e) {
          statusError(e);
        } finally {
          handleStop();
        }
      }
    }, "processing.py mode runner");
    runner.start();
  }

  private SketchException convertPythonSketchError(PythonSketchError e) {
    if (e.file == null) {
      return new SketchException(e.getMessage());
    }
    int fileIndex = -1;
    final SketchCode[] codes = getSketch().getCode();
    for (int i = 0; i < codes.length; i++) {
      if (codes[i].getFile().getAbsoluteFile().equals(new File(e.file).getAbsoluteFile())) {
        fileIndex = i;
        break;
      }
    }
    if (fileIndex < 0) {
      return new SketchException(e.getMessage());
    }
    if (e.line < 0) {
      return new SketchException(e.getMessage(), fileIndex, 0);
    }
    if (e.column < 0) {
      return new SketchException(e.getMessage(), fileIndex, e.line);
    }
    return new SketchException(e.getMessage(), fileIndex, e.line, e.column);
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
    sketch.ensureExistence();
    final String name = new File(jarPath).getParentFile().getParentFile().getName();
    if (Pattern.compile("^add_library\\(\\s*'" + name + "'\\s*\\)\\s*$", Pattern.MULTILINE)
        .matcher(getText()).find()) {
      return;
    }
    setSelection(0, 0); // scroll to start
    setSelectedText(String.format("add_library('%s')\n", name));
    sketch.setModified(true);
  }
}