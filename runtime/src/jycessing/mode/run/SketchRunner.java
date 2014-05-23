package jycessing.mode.run;

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

  private final String id;
  private final ModeService modeService;
  private Thread runner = null;
  private volatile boolean shutdownWasRequested = false;

  public SketchRunner(final String id, final ModeService modeService) {
    this.id = id;
    this.modeService = modeService;
    try {
      OSXAdapter.setQuitHandler(this, this.getClass().getMethod("preventUserQuit"));
    } catch (final Exception e) {
      System.err.println(e.getMessage());
    }
  }

  /**
   * On Mac, even though this app has no menu, there's still a
   * built-in cmd-Q handler that, by default, quits the app.
   * Because starting up the {@link SketchRunner} is expensive,
   * we'd prefer to leave the app running.
   * <p>This function responds to a user cmd-Q by stopping the
   * currently running sketch, and rejecting the attempt to quit.
   * <p>But if we've received a shutdown request from the
   * {@link SketchServiceProcess} on the PDE VM, then we permit
   * the quit to proceed.
   * @return true iff the SketchRunner should quit.
   */
  public boolean preventUserQuit() {
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
            System.setErr(new ForwardingPrintStream(id, modeService, Stream.ERR));
            try {
              System.setOut(new ForwardingPrintStream(id, modeService, Stream.OUT));
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
            modeService.handleSketchException(id, convertPythonSketchError(e, info.codeFileNames));
          } catch (final Exception e) {
            if (e.getCause() != null && e.getCause() instanceof PythonSketchError) {
              modeService.handleSketchException(id,
                  convertPythonSketchError((PythonSketchError)e.getCause(), info.codeFileNames));
            } else {
              modeService.handleSketchException(id, e);
            }
          } finally {
            modeService.handleSketchStopped(id);
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
    final String id = args[0];
    // If env var SKETCH_RUNNER_FIRST=true then SketchRunner will wait for a ping from the Mode
    // before registering itself as the sketch runner.
    if (PythonMode.SKETCH_RUNNER_FIRST) {
      waitForMode(id);
    } else {
      startSketchRunner(id);
    }
  }

  private static class ModeWaiterImpl implements ModeWaiter {
    final String id;


    public ModeWaiterImpl(final String id) {
      this.id = id;
    }


    @Override
    public void modeReady(final ModeService modeService) {
      try {
        launch(id, modeService);
      } catch (final Exception e) {
        throw new RuntimeException(e);
      }
    }
  }

  private static void waitForMode(final String id) {
    try {
      RMIUtils.bind(new ModeWaiterImpl(id), ModeWaiter.class);
    } catch (final RMIProblem e) {
      throw new RuntimeException(e);
    }
  }

  private static void startSketchRunner(final String id) {
    try {
      final ModeService modeService = RMIUtils.lookup(ModeService.class);
      launch(id, modeService);
    } catch (final Exception e) {
      throw new RuntimeException(e);
    }
  }

  private static void launch(final String id, final ModeService modeService) throws RMIProblem,
      RemoteException {
    final SketchRunner sketchRunner = new SketchRunner(id, modeService);
    final SketchService stub = (SketchService)RMIUtils.export(sketchRunner);
    log("Calling mode's handleReady().");
    modeService.handleReady(id, stub);
    Runtime.getRuntime().addShutdownHook(new Thread(new Runnable() {
      @Override
      public void run() {
        log("Exiting; telling modeService.");
        try {
          modeService.handleSketchStopped(id);
        } catch (final RemoteException e) {
          // nothing we can do about it now.
        }
      }
    }));
  }

  private SketchException convertPythonSketchError(final PythonSketchError e,
      final String[] fileNames) {
    if (e.fileName == null) {
      return new SketchException(e.getMessage());
    }
    int fileIndex = -1;
    for (int i = 0; i < fileNames.length; i++) {
      if (fileNames[i].equals(e.fileName)) {
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
