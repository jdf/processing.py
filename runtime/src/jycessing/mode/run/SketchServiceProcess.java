package jycessing.mode.run;

import java.io.File;
import java.io.FilenameFilter;
import java.io.IOException;
import java.net.ConnectException;
import java.net.SocketTimeoutException;
import java.rmi.RemoteException;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;

import jycessing.mode.PyEditor;
import jycessing.mode.PythonMode;
import processing.app.Base;
import processing.app.Preferences;
import processing.app.SketchException;

public class SketchServiceProcess {
  private static void log(final String msg) {
    if (PythonMode.VERBOSE) {
      System.err.println(SketchServiceProcess.class.getSimpleName() + ": " + msg);
    }
  }

  private static final FilenameFilter JARS = new FilenameFilter() {
    @Override
    public boolean accept(final File dir, final String name) {
      return name.endsWith(".jar");
    }
  };

  private final PythonMode mode;
  private final PyEditor editor;
  private Process sketchServiceProcess;
  private SketchService sketchService;

  // If someone tries to run a sketch and, for some reason, there's no sketch runner,
  // remember the request and honor it when the sketch runner exists.
  private volatile Runnable pendingSketchRequest = null;

  public SketchServiceProcess(final PythonMode mode, final PyEditor editor) {
    this.mode = mode;
    this.editor = editor;
  }

  public void start() {
    log("Starting sketch runner process.");
    final ProcessBuilder pb = createServerCommand();
    log("Running:\n" + pb.command());
    try {
      sketchServiceProcess = pb.start();
    } catch (final IOException e) {
      Base.showError("PythonMode Error", "Cannot start python sketch runner.", e);
    }
  }

  private void handleRemoteException(final RemoteException e) throws SketchException {
    final Throwable cause = e.getCause();
    if (cause instanceof SocketTimeoutException || cause instanceof ConnectException) {
      log("SketchRunner either hung or not there. Restarting it.");
      restartServerProcess();
    } else {
      throw new SketchException(e.getMessage());
    }
  }

  public void handleReady(final SketchService service) {
    log("handleReady()");
    sketchService = service;
    log("Successfully bound SketchRunner stub.");
    final Runnable req = pendingSketchRequest;
    pendingSketchRequest = null;
    if (req != null) {
      req.run();
    }
  }

  public void handleSketchStopped() {
    log("Sketch stopped.");
    editor.deactivateRun();
  }

  private ProcessBuilder createServerCommand() {
    final ArrayList<String> command = new ArrayList<String>();

    command.add(Base.getJavaPath());

    if (Preferences.getBoolean("run.options.memory")) {
      command.add("-Xms" + Preferences.get("run.options.memory.initial") + "m");
      command.add("-Xmx" + Preferences.get("run.options.memory.maximum") + "m");
    }

    if (Base.isMacOS()) {
      // Suppress dock icon.
      command.add("-Dapple.awt.UIElement=true");
    }

    command.add("-Djava.library.path=" + System.getProperty("java.library.path"));

    final List<String> cp = new ArrayList<String>();
    cp.add(System.getProperty("java.class.path"));
    for (final File jar : new File(Base.getContentFile("core"), "library").listFiles(JARS)) {
      cp.add(jar.getAbsolutePath());
    }
    final File[] libJars = mode.getContentFile("mode").listFiles(JARS);
    if (libJars != null) {
      for (final File jar : libJars) {
        cp.add(jar.getAbsolutePath());
      }
    } else {
      log("No library jars found; I assume we're running in Eclipse.");
    }
    command.add("-cp");
    final StringBuilder sb = new StringBuilder();
    for (final String element : cp) {
      if (sb.length() > 0) {
        sb.append(File.pathSeparatorChar);
      }
      sb.append(element);
    }
    command.add(sb.toString());

    // enable assertions
    command.add("-ea");

    // Run the SketchRunner main.
    command.add(SketchRunner.class.getName());

    // Give the runner its ID as an argument.
    command.add(editor.getId());

    return new ProcessBuilder(command);
  }


  private void restartServerProcess() {
    shutdown();
    start();
  }

  public void runSketch(final SketchInfo info) throws SketchException {
    // Create a pending request in case of various failure modes.
    pendingSketchRequest = new Runnable() {
      @Override
      public void run() {
        try {
          runSketch(info);
        } catch (final SketchException e) {
          editor.statusError(e);
        }
      }
    };
    if (sketchService == null) {
      log("Sketch service not running. Leaving pending request to run sketch.");
      restartServerProcess();
      return;
    }
    try {
      sketchService.startSketch(info);
      // If and only if we've successully request a sketch start, nuke the pending request.
      pendingSketchRequest = null;
      return;
    } catch (final RemoteException e) {
      handleRemoteException(e);
      log("Leaving pending request to run sketch.");
    }
  }


  public void stopSketch() throws SketchException {
    if (sketchService == null) {
      log("Sketch runner apparetly not running; can't stop sketch.");
      handleSketchStopped();
      restartServerProcess();
      return;
    }
    try {
      sketchService.stopSketch();
    } catch (final RemoteException e) {
      handleRemoteException(e);
    }
  }


  public void shutdown() {
    if (sketchService != null) {
      log("Telling sketch runner to shutdown.");
      try {
        sketchService.shutdown();
      } catch (final RemoteException e) {
      }
    }
    if (sketchServiceProcess != null) {
      log("Killing sketch runner process.");
      sketchServiceProcess.destroy();
      log("Waiting for sketch runner process to exit.");
      try {
        sketchServiceProcess.waitFor();
        log("Sketcher runner process exited normally.");
      } catch (final InterruptedException e) {
        log("Interrupted while waiting for sketch runner to exit.");
      }
      sketchServiceProcess = null;
    }
  }

  private static final Pattern IGNORE = Pattern.compile("^__MOVE__\\s+(.*)$");

  public void print(final Stream stream, final String s) {
    if (stream == Stream.ERR) {
      editor.printErr(s);
    } else {
      editor.printOut(s);
    }
  }

  public void println(final Stream stream, final String s) {
    if (stream == Stream.ERR && IGNORE.matcher(s).matches()) {
      // TODO(feinberg): Handle MOVE commands.
      return;
    }
    if (stream == Stream.ERR) {
      editor.printErr(s + "\n");
    } else {
      editor.printOut(s + "\n");
    }
  }

  public void handleSketchException(final Exception e) {
    editor.statusError(e);
  }

}
