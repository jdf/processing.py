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

import org.python.google.common.base.Joiner;

import processing.app.Base;
import processing.app.Preferences;
import processing.app.SketchException;

public class SketchServiceManager implements ModeService {

  private static void log(final String msg) {
    if (PythonMode.VERBOSE) {
      System.err.println(SketchServiceManager.class.getSimpleName() + ": " + msg);
    }
  }

  private static final FilenameFilter JARS = new FilenameFilter() {
    @Override
    public boolean accept(File dir, String name) {
      return name.endsWith(".jar");
    }
  };

  // If someone tries to run a sketch and, for some reason, there's no sketch runner,
  // remember the request and honor it when the sketch runner exists.
  private volatile Runnable pendingSketchRequest = null;

  private final PythonMode mode;
  private Process sketchServiceProcess;
  private SketchService sketchService;

  public SketchServiceManager(final PythonMode mode) {
    this.mode = mode;
    Runtime.getRuntime().addShutdownHook(new Thread(new Runnable() {
      @Override
      public void run() {
        stop();
      }
    }));
  }

  public void start() {
    try {
      if (PythonMode.SKETCH_RUNNER_FIRST) {
        final ModeService stub = (ModeService)RMIUtils.export(this);
        final ModeWaiter modeWaiter = RMIUtils.lookup(ModeWaiter.class);
        modeWaiter.modeReady(stub);
      } else {
        RMIUtils.bind(this, ModeService.class);
        startSketchServerProcess();
      }
    } catch (Exception e) {
      Base.showError("PythonMode Error", "Cannot start python sketch service.", e);
      return;
    }
  }

  private void startSketchServerProcess() {
    log("Starting sketch runner process.");
    final ProcessBuilder pb = createServerCommand();
    log("Running:\n" + Joiner.on(" ").join(pb.command()));
    try {
      sketchServiceProcess = pb.start();
    } catch (IOException e) {
      Base.showError("PythonMode Error", "Cannot start python sketch runner.", e);
    }
  }

  public void stop() {
    if (sketchServiceProcess != null) {
      log("Killing sketch runner process.");
      sketchServiceProcess.destroy();
      log("Waiting for sketch runner process to exit.");
      try {
        sketchServiceProcess.waitFor();
        log("Sketcher runner process exited normally.");
      } catch (InterruptedException e) {
        log("Interrupted while waiting for sketch runner to exit.");
      }
      sketchServiceProcess = null;
    }
  }

  @Override
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

  @Override
  public void handleSketchStopped() {
    log("Sketch stopped.");
    mode.handleSketchStopped();
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
    command.add(Joiner.on(File.pathSeparator).join(cp));

    // enable assertions
    command.add("-ea");

    // Run the SketchRunner main.
    command.add(SketchRunner.class.getName());

    return new ProcessBuilder(command);
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

  private void restartServerProcess() {
    stop();
    startSketchServerProcess();
  }

  public void runSketch(final PyEditor editor, final SketchInfo info) throws SketchException {
    // Create a pending request in case of various failure modes.
    pendingSketchRequest = new Runnable() {
      @Override
      public void run() {
        try {
          runSketch(editor, info);
        } catch (SketchException e) {
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
    } catch (RemoteException e) {
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
    } catch (RemoteException e) {
      handleRemoteException(e);
    }
  }

  private static final Pattern IGNORE = Pattern.compile("^__MOVE__\\s+(.*)$");

  @Override
  public void print(Stream stream, String s) {
    stream.getSystemStream().print(s);
    stream.getSystemStream().flush();
  }

  @Override
  public void println(Stream stream, String s) {
    if (stream == Stream.ERR && IGNORE.matcher(s).matches()) {
      // TODO(feinberg): Handle MOVE commands.
      return;
    }
    stream.getSystemStream().println(s);
    stream.getSystemStream().flush();
  }

  @Override
  public void handleSketchException(Exception e) {
    mode.handleSketchException(e);
  }
}
