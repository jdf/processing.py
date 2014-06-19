package jycessing.mode;

import java.awt.Component;
import java.awt.Point;
import java.awt.Rectangle;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseWheelEvent;
import java.awt.event.MouseWheelListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.beans.PropertyChangeEvent;
import java.beans.PropertyChangeListener;
import java.io.File;
import java.io.IOException;
import java.nio.file.DirectoryIteratorException;
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import java.util.regex.Pattern;

import javax.swing.AbstractAction;
import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.JDialog;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.SwingConstants;

import jycessing.IOUtil;
import jycessing.Runner.LibraryPolicy;
import jycessing.mode.run.SketchInfo;
import jycessing.mode.run.SketchInfo.Builder;
import jycessing.mode.run.SketchService;
import jycessing.mode.run.SketchServiceManager;
import jycessing.mode.run.SketchServiceProcess;
import processing.app.Base;
import processing.app.Editor;
import processing.app.EditorState;
import processing.app.EditorToolbar;
import processing.app.Formatter;
import processing.app.Library;
import processing.app.Mode;
import processing.app.Preferences;
import processing.app.SketchCode;
import processing.app.SketchException;
import processing.app.Toolkit;
import processing.core.PApplet;
import processing.core.PConstants;

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
  private final PyKeyListener keyListener;
  private final SketchServiceProcess sketchService;

  /**
   * If the user runs a dirty sketch, we create a temp dir containing the
   * modified state of the sketch and run it from there. We keep track
   * of it in this variable in order to delete it when done running.
   */
  private Path tempSketch;


  protected PyEditor(final Base base, final String path, final EditorState state, final Mode mode) {
    super(base, path, state, mode);

    id = UUID.randomUUID().toString();
    keyListener = new PyKeyListener(this, textarea);
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
   * Create export GUI and hand off results to performExport()
   */
  public void handleExportApplication() {
    // This is kind of obnoxious. Should we just save automatically?
    if (sketch.isModified()) {
      Object[] options = { "OK", "Cancel" };
      int result = JOptionPane.showOptionDialog(this,
                                                "Save changes before export?",
                                                "Save",
                                                JOptionPane.OK_CANCEL_OPTION,
                                                JOptionPane.QUESTION_MESSAGE,
                                                null,
                                                options,
                                                options[0]);
      if (result == JOptionPane.OK_OPTION) {
        handleSave(true);
      } else {
        statusNotice("Export canceled, changes must first be saved.");
        return;
      }
    }
    JPanel panel = new JPanel();
    panel.setLayout(new BoxLayout(panel, BoxLayout.Y_AXIS));
    panel.add(Box.createVerticalStrut(6));
    JLabel filler = new JLabel("Options will go here", SwingConstants.CENTER);
    filler.setAlignmentX(Component.LEFT_ALIGNMENT);
    panel.add(filler);
    String[] options = { "Export", "Cancel" };
    final JOptionPane optionPane = new JOptionPane(panel,
                                                   JOptionPane.PLAIN_MESSAGE,
                                                   JOptionPane.YES_NO_OPTION,
                                                   null,
                                                   options,
                                                   options[0]);
    
    final JDialog dialog = new JDialog(this, "Export Application", true);
    dialog.setContentPane(optionPane);
    optionPane.addPropertyChangeListener(new PropertyChangeListener() {
      public void propertyChange(PropertyChangeEvent e) {
        String prop = e.getPropertyName();

        if (dialog.isVisible() &&
            (e.getSource() == optionPane) &&
            (prop.equals(JOptionPane.VALUE_PROPERTY))) {
          dialog.setVisible(false);
        }
      }
    });
    dialog.pack();
    dialog.setResizable(false);
    Rectangle bounds = getBounds();
    dialog.setLocation(bounds.x + (bounds.width - dialog.getSize().width) / 2,
                       bounds.y + (bounds.height - dialog.getSize().height) / 2);
    dialog.setVisible(true);
    
    // wait until they click "Export". This stops the main editor from working -
    // do we want that?
    Object value = optionPane.getValue();
    
    if (value.equals(options[0])) {
      performExport();
    } else {
      statusNotice("Export to Application Cancelled");
    }
  }

  /**
   * Perform preprocessing and export to each selected platform
   * Currently I'm only doing linux
   */
  public void performExport() {
    int platform = Base.getPlatformIndex("linux");
    try {
      exportToPlatform(platform, 64);
    } catch (Exception e) {
      e.printStackTrace();
      statusError("Export to "+PConstants.platformNames[platform]+64+" failed. Sorry!");
    }
  }
  
  /**
   * This is how Java Mode handles exporting - lots and lots of if statements.
   * I could also make individual "exportTo$Platform" methods, but I'm not sure.
   * 
   * @param platform
   * @param bits
   */
  public void exportToPlatform(int platform, int bits) throws IOException {
    
    log("Exporting to "+PConstants.platformNames[platform]+bits);
    
    // Work out user preferences and other possibilities we care about
    // I'm putting these here to tell anyone reading what this method depends on - does that make sense?
    final boolean embedJava = (platform == PApplet.platform) && Preferences.getBoolean("export.application.embed_java");
    final boolean hasData = sketch.hasDataFolder();
    final boolean hasCode = sketch.hasCodeFolder();
    
    // Work out the folders we'll be (maybe) using
    final File destFolder = new File(sketch.getFolder(), "application."+PConstants.platformNames[platform]+bits);
    final File libFolder = new File(destFolder, "lib");
    final File codeFolder = new File(destFolder, "code");
    final File sourceFolder = new File(destFolder, "source");
    final File dataFolder = new File(destFolder, "data");
    final File javaFolder = new File(destFolder, "java");
    
    // Things we need to keep track of
    List<Library> libraries = new ArrayList<Library>(); // Obtained by scraping the python AST, eventually...
    List<String> jarFiles = new ArrayList<String>();    // Things we'll need to add to the export's classpath
    
    // Delete previous export (if the user wants to, and it exists) and make a new one
    pyMode.prepareExportFolder(destFolder);
    
    // Handle embedding java
    if (embedJava) {
      log("Embedding java in export.");
      javaFolder.mkdirs();
      if (platform == PConstants.MACOSX) {
        
      } else if (platform == PConstants.WINDOWS) {
        
      } else if (platform == PConstants.LINUX) {
        Base.copyDir(Base.getJavaHome(), javaFolder);
      } else if (platform == PConstants.OTHER) {
        
      }
    }
    
    // Handle data folder
    if (hasData) {
      log("Copying data folder to export.");
      dataFolder.mkdirs();
      if (platform == PConstants.MACOSX) {
        
      } else if (platform == PConstants.WINDOWS) {
        
      } else if (platform == PConstants.LINUX) {
        Base.copyDir(sketch.getDataFolder(), dataFolder);
      } else if (platform == PConstants.OTHER) {
        
      }
    }
    
    // Handle code folder
    // ...what is the code folder for, exactly?
    if (hasCode) {
      log("Copying code folder to export.");
      codeFolder.mkdirs();
      if (platform == PConstants.MACOSX) {
        
      } else if (platform == PConstants.WINDOWS) {
        
      } else if (platform == PConstants.LINUX) {
        
      } else if (platform == PConstants.OTHER) {
        
      }
    }
    
    // Handle source folder
    {
      log("Copying source to export.");
      sourceFolder.mkdirs();
      for (SketchCode code : sketch.getCode()){
        code.copyTo(new File(sourceFolder, code.getFileName()));
      }
    }
    
    // Handle imported libraries
    // For now, all we have is the core library
    {
      Library core = new Library(Base.getContentFile("core"));
      libraries.add(core);
      
      for (Library library : libraries) {
        for (File exportFile : library.getApplicationExports(platform, bits)) {
          final String exportName = exportFile.getName();
          if (!exportFile.exists()) {
            statusError("The file "+exportName+" is mentioned in the export.txt from "
                          +library+" but does not actually exist.");
            continue;
          }
          if (exportFile.isDirectory()) {
            Base.copyDir(exportFile, new File(libFolder, exportName));
          } else if (exportName.toLowerCase().endsWith(".jar") || exportName.toLowerCase().endsWith(".zip")) {
            jarFiles.add(exportName);
            Base.copyFile(exportFile, new File(libFolder, exportName));
          } else {
            Base.copyFile(exportFile, new File(libFolder, exportName));
          }
        }
      }
    }
    
    // Add Python Mode stuff (pymode jar, guava, jython jar, jython license)
    // [If we restructured the mode code as a P5 library this could be folded into the above]
    for (File exportFile : pyMode.getContentFile("mode").listFiles()){
      if (exportFile.getName().toLowerCase().endsWith(".jar")) {
        jarFiles.add(exportFile.getName());
      }
      Base.copyFile(exportFile, new File(libFolder, exportFile.getName()));
    }
    
    // Create .sh file...
  }
  
  /**
   * Save the current state of the sketch into a temp dir, and return
   * the created directory.
   * @return a new directory containing a saved version of the current
   * (presumably modified) sketch.
   * @throws IOException 
   */
  private Path createTempSketch() throws IOException {
    final Path tmp = Files.createTempDirectory(sketch.getName());
    for (final SketchCode code : sketch.getCode()) {
      Files.write(tmp.resolve(code.getFileName()), code.getProgram().getBytes("utf-8"));
    }
    final Path sketchFolder = sketch.getFolder().toPath();
    try (final DirectoryStream<Path> stream = Files.newDirectoryStream(sketchFolder)) {
      for (final Path entry : stream) {
        if (!mode.canEdit(entry.toFile())) {
          IOUtil.copy(entry, tmp);
        }
      }
    } catch (final DirectoryIteratorException ex) {
      throw ex.getCause();
    }
    return tmp;
  }

  private void runSketch(final RunMode mode) {
    prepareRun();
    toolbar.activate(PyToolbar.RUN);
    final String sketchPath;
    if (sketch.isModified()) {
      log("Sketch is modified; must copy it to temp dir.");
      final String sketchMainFileName = sketch.getCode(0).getFile().getName();
      try {
        tempSketch = createTempSketch();
        sketchPath = tempSketch.resolve(sketchMainFileName).toString();
      } catch (final IOException e) {
        Base.showError("Sketchy Behavior", "I can't copy your unsaved work\n"
            + "to a temp directory.", e);
        return;
      }
    } else {
      sketchPath = sketch.getCode(0).getFile().getAbsolutePath();
    }

    try {
      final String[] codeFileNames = new String[sketch.getCodeCount()];
      for (int i = 0; i < codeFileNames.length; i++) {
        codeFileNames[i] = sketch.getCode(i).getFile().getName();
      }
      final Builder infoBuilder =
          new SketchInfo.Builder().sketchName(sketch.getName()).runMode(mode)
              .addLibraryDir(Base.getContentFile("modes/java/libraries"))
              .addLibraryDir(Base.getSketchbookLibrariesFolder())
              .mainSketchFile(new File(sketchPath).getAbsoluteFile())
              .code(sketch.getCode(0).getProgram()).codeFileNames(codeFileNames)
              .libraryPolicy(LibraryPolicy.SELECTIVE);

      if (getSketchLocation() != null) {
        infoBuilder.sketchLoc(getSketchLocation());
      } else if (getLocation() != null) {
        infoBuilder.editorLoc(new Point(getLocation()));
      }
      sketchService.runSketch(infoBuilder.build());
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
    runSketch(RunMode.WINDOWED);
  }

  public void handlePresent() {
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

  public void printOut(final String msg) {
    console.message(msg, false);
  }

  public void printErr(final String msg) {
    console.message(msg, true);
  }
}
