package jycessing.mode.run;

import java.io.File;
import java.io.FilenameFilter;
import java.io.IOException;
import java.net.SocketTimeoutException;
import java.rmi.NotBoundException;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.UnicastRemoteObject;
import java.util.ArrayList;
import java.util.List;

import jycessing.mode.PythonMode;
import jycessing.mode.RunMode;

import org.python.google.common.base.Joiner;

import processing.app.Base;
import processing.app.Preferences;
import processing.app.SketchException;

public class SketchServiceManager implements ModeService {

  static final int RMI_PORT = 8220;

  static {
    System.setProperty("sun.rmi.transport.tcp.responseTimeout", "2000");
  }

  private static void log(final String msg) {
    System.err.println(SketchServiceManager.class.getSimpleName() + ": " + msg);
  }

  private static final FilenameFilter JARS = new FilenameFilter() {
    @Override
    public boolean accept(File dir, String name) {
      return name.endsWith(".jar");
    }
  };

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
      log("Creating RMI registry.");
      final Registry registry = LocateRegistry.createRegistry(RMI_PORT);
      log("Binding ModeService to registry.");
      registry.bind(ModeService.class.getSimpleName(), UnicastRemoteObject.exportObject(this, 0));
      Runtime.getRuntime().addShutdownHook(new Thread(new Runnable() {
        @Override
        public void run() {
          try {
            log("Unbinding SketchService from registry.");
            registry.unbind(ModeService.class.getSimpleName());
          } catch (Exception e) {
          }
        }
      }));
    } catch (Exception e) {
      Base.showError("PythonMode Error", "Cannot start python sketch service.", e);
      return;
    }
    startSketchServerProcess();
  }

  private void startSketchServerProcess() {
    log("Starting sketch runner process.");
    final ProcessBuilder pb = createServerCommand();
    pb.inheritIO();
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
      } catch (InterruptedException e) {
        log("Interrupted while waiting for sketch runner to exit.");
      }
      sketchServiceProcess = null;
    }
  }

  @Override
  public void handleReady() throws RemoteException {
    log("handleReady()");
    final Registry registry = LocateRegistry.getRegistry(RMI_PORT);
    try {
      sketchService = (SketchService)registry.lookup(SketchService.class.getSimpleName());
      log("Successfully bound SketchRunner stub.");
    } catch (NotBoundException e) {
      Base.showError("PythonMode Error", "Cannot find sketch runner in RMI registry.", e);
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
    for (final File jar : mode.getContentFile("mode").listFiles(JARS)) {
      cp.add(jar.getAbsolutePath());
    }
    command.add("-cp");
    command.add(Joiner.on(File.pathSeparator).join(cp));

    // enable assertions
    command.add("-ea");

    // Run the SketchRunner main.
    command.add(SketchRunner.class.getName());

    return new ProcessBuilder(command);
  }

  public void runSketch(RunMode runMode, File libraries, File sketch, String code,
      String[] codePaths, int x, int y) throws SketchException {
    if (sketchService == null) {
      throw new SketchException("Sketch runner not running!");
    }
    try {
      sketchService.startSketch(runMode, libraries, sketch, code, codePaths, x, y);
    } catch (RemoteException e) {
      throw new SketchException(e.getMessage());
    }
  }

  public void stopSketch() throws SketchException {
    if (sketchService == null) {
      throw new SketchException("Sketch runner not running!");
    }
    try {
      sketchService.stopSketch();
    } catch (RemoteException e) {
      if (e.getCause() instanceof SocketTimeoutException) {
        log("Timed out.");
        stop();
        startSketchServerProcess();
      } else {
        throw new SketchException(e.getMessage());
      }
    }
  }

  @Override
  public void handleSketchException(Exception e) {
    mode.handleSketchException(e);
  }
}
