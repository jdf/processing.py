package jycessing.mode.run;

import java.io.File;
import java.io.PrintStream;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.UnicastRemoteObject;
import java.util.regex.Pattern;

import jycessing.PreparedPythonSketch;
import jycessing.PythonSketchError;
import jycessing.Runner;
import jycessing.Runner.LibraryPolicy;
import jycessing.mode.RunMode;
import processing.app.Base;
import processing.app.SketchException;

public class SketchRunner implements SketchService {
  private static void log(final String msg) {
    if (Base.DEBUG) {
      System.err.println(SketchRunner.class.getSimpleName() + ": " + msg);
    }
  }

  private final ModeService modeService;
  private Thread runner = null;

  public SketchRunner(final ModeService modeService) {
    this.modeService = modeService;
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

  @Override
  public void startSketch(final RunMode runMode, final File libraries, final File sketch,
      final String code, final String[] codePaths, final int x, final int y) {
    runner = new Thread(new Runnable() {
      @Override
      public void run() {
        try {
          try {
            final PreparedPythonSketch preparedSketch =
                Runner.prepareSketch(libraries, LibraryPolicy.SELECTIVE,
                    runMode.args(sketch.getAbsolutePath(), x, y), sketch.getAbsolutePath(), code);
            final PrintStream syserr = System.err;
            System.setErr(new MoveCommandFilteringPrintStream(syserr));
            try {
              preparedSketch.runBlocking();
            } finally {
              System.setErr(syserr);
            }
          } catch (PythonSketchError e) {
            modeService.handleSketchException(convertPythonSketchError(e, codePaths));
          } catch (Exception e) {
            modeService.handleSketchException(e);
          } finally {
            modeService.handleSketchStopped();
          }
        } catch (RemoteException e) {
          log(e.toString());
        }
        // Exiting; no need to interrupt and join it later.
        runner = null;
      }
    }, "processing.py mode runner");
    runner.start();
  }

  @Override
  public void stopSketch() {
    log("stopSketch()");
    if (runner != null) {
      log("Interrupting runner thread.");
      runner.interrupt();
      try {
        log("Joining runner thread.");
        runner.join();
        log("Runner thread terminated normally.");
      } catch (InterruptedException e) {
        log("Interrupted while joined to runner thread.");
      }
      runner = null;
    }
  }

  public static void main(String[] args) {
    try {
      log("Locating RMI registry.");
      final Registry registry = LocateRegistry.getRegistry(SketchServiceManager.RMI_PORT);
      log("Looking up ModeService in registry.");
      final ModeService modeService =
          (ModeService)registry.lookup(ModeService.class.getSimpleName());
      final SketchRunner sketchRunner = new SketchRunner(modeService);
      final SketchService stub = (SketchService)UnicastRemoteObject.exportObject(sketchRunner, 0);
      log("Calling mode's handleReady().");
      modeService.handleReady(stub);
    } catch (Exception e) {
      throw new RuntimeException(e);
    }
  }

  private SketchException convertPythonSketchError(PythonSketchError e, final String[] codePaths) {
    if (e.file == null) {
      return new SketchException(e.getMessage());
    }
    int fileIndex = -1;
    for (int i = 0; i < codePaths.length; i++) {
      if (codePaths.equals(new File(e.file).getAbsoluteFile())) {
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

}
