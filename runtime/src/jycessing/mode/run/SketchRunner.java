package jycessing.mode.run;

import java.io.File;
import java.io.PrintStream;
import java.rmi.RemoteException;

import jycessing.PythonSketchError;
import jycessing.Runner;
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
  private volatile boolean shutdownWasRequested = false;

  public SketchRunner(final ModeService modeService) {
    this.modeService = modeService;
    try {
      OSXAdapter.setQuitHandler(this, this.getClass().getMethod("cancelQuit"));
    } catch (final Exception e) {
      System.err.println(e.getMessage());
    }
  }

  public boolean cancelQuit() {
    if (shutdownWasRequested) {
      log("Permitting quit.");
      return true;
    }
    log("Cancelling quit, but stopping sketch.");
    new Thread(new Runnable() {
      @Override
      public void run() {
        stopSketch();
      }
    }).start();
    return false;
  }

  @Override
  public void shutdown() {
    shutdownWasRequested = true;
    log("Calling system.exit(0)");
    System.exit(0);
  }

  @Override
  public void startSketch(final SketchInfo info) {
    runner = new Thread(new Runnable() {
      @Override
      public void run() {
        try {
          try {
            final PrintStream syserr = System.err;
            final PrintStream sysout = System.out;
            System.setErr(new ForwardingPrintStream(modeService, Stream.ERR));
            try {
              System.setOut(new ForwardingPrintStream(modeService, Stream.OUT));
              try {
                Runner.runSketchBlocking(info);
              } finally {
                System.setOut(sysout);
              }
            } finally {
              System.setErr(syserr);
            }
          } catch (final PythonSketchError e) {
            log("Sketch runner caught " + e);
            modeService.handleSketchException(convertPythonSketchError(e, info.codePaths));
          } catch (final Exception e) {
            if (e.getCause() != null && e.getCause() instanceof PythonSketchError) {
              modeService.handleSketchException(convertPythonSketchError(
                  (PythonSketchError)e.getCause(), info.codePaths));
            } else {
              modeService.handleSketchException(e);
            }
          } finally {
            modeService.handleSketchStopped();
          }
        } catch (final RemoteException e) {
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
      } catch (final InterruptedException e) {
        log("Interrupted while joined to runner thread.");
      }
      runner = null;
    }
  }

  public static void main(final String[] args) {
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
    public void modeReady(final ModeService modeService) {
      try {
        launch(modeService);
      } catch (final Exception e) {
        throw new RuntimeException(e);
      }
    }
  }

  private static void waitForMode() {
    try {
      RMIUtils.bind(new ModeWaiterImpl(), ModeWaiter.class);
    } catch (final RMIProblem e) {
      throw new RuntimeException(e);
    }
  }

  private static void startSketchRunner() {
    try {
      final ModeService modeService = RMIUtils.lookup(ModeService.class);
      launch(modeService);
    } catch (final Exception e) {
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
        } catch (final RemoteException e) {
          // nothing we can do about it now.
        }
      }
    }));
  }

  private SketchException convertPythonSketchError(final PythonSketchError e,
      final String[] codePaths) {
    if (e.file == null) {
      return new SketchException(e.getMessage());
    }
    int fileIndex = -1;
    for (int i = 0; i < codePaths.length; i++) {
      final String codePath = new File(codePaths[i]).getAbsolutePath();
      final String exceptionFilePath = new File(e.file).getAbsolutePath();
      if (codePath.equals(exceptionFilePath)) {
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
