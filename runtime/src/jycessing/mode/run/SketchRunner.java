package jycessing.mode.run;

import java.io.File;
import java.io.PrintStream;
import java.rmi.RemoteException;
import java.util.regex.Pattern;

import jycessing.PreparedPythonSketch;
import jycessing.PythonSketchError;
import jycessing.Runner;
import jycessing.Runner.LibraryPolicy;
import jycessing.mode.PythonMode;
import jycessing.mode.run.RMIUtils.RMIProblem;
import processing.app.SketchException;

public class SketchRunner implements SketchService {

  private static void log(final String msg) {
    if (PythonMode.VERBOSE) {
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
  public void startSketch(final SketchInfo info) {
    runner = new Thread(new Runnable() {
      @Override
      public void run() {
        try {
          try {
            final PreparedPythonSketch preparedSketch =
                Runner.prepareSketch(info.libraries, LibraryPolicy.SELECTIVE,
                    info.runMode.args(info.sketch.getAbsolutePath(), info.x, info.y),
                    info.sketch.getAbsolutePath(), info.code);
            final PrintStream syserr = System.err;
            System.setErr(new MoveCommandFilteringPrintStream(syserr));
            try {
              preparedSketch.runBlocking();
            } finally {
              System.setErr(syserr);
            }
          } catch (PythonSketchError e) {
            modeService.handleSketchException(convertPythonSketchError(e, info.codePaths));
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
    // If env var SKETCH_RUNNER_FIRST=true then SketchRunner will wait for a ping from the Mode
    // before registering itself as the sketch runner.
    if (PythonMode.SKETCH_RUNNER_FIRST) {
      waitForMode();
    } else {
      startSketchRunner();
    }
  }

  private static class ModeWaiterImpl implements ModeWaiter {
    @Override
    public void modeReady(ModeService modeService) {
      try {
        launch(modeService);
      } catch (Exception e) {
        throw new RuntimeException(e);
      }
    }
  }

  private static void waitForMode() {
    try {
      RMIUtils.bind(new ModeWaiterImpl(), ModeWaiter.class);
    } catch (RMIProblem e) {
      throw new RuntimeException(e);
    }
  }

  private static void startSketchRunner() {
    try {
      final ModeService modeService = RMIUtils.lookup(ModeService.class);
      launch(modeService);
    } catch (Exception e) {
      throw new RuntimeException(e);
    }
  }

  private static void launch(final ModeService modeService) throws RMIProblem, RemoteException {
    final SketchRunner sketchRunner = new SketchRunner(modeService);
    final SketchService stub = (SketchService)RMIUtils.export(sketchRunner);
    log("Calling mode's handleReady().");
    modeService.handleReady(stub);
    Runtime.getRuntime().addShutdownHook(new Thread(new Runnable() {
      @Override
      public void run() {
        log("Exiting; telling modeService.");
        try {
          modeService.handleSketchStopped();
        } catch (RemoteException e) {
          // nothing we can do about it now.
        }
      }
    }));
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
