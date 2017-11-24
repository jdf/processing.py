package jycessing.mode.run;

import java.rmi.RemoteException;

import jycessing.Printer;
import jycessing.PythonSketchError;
import jycessing.Runner;
import jycessing.SketchPositionListener;
import jycessing.mode.PythonMode;
import jycessing.mode.run.RMIUtils.RMIProblem;
import processing.app.SketchException;
import processing.core.PApplet;
import processing.core.PConstants;

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
    if (PApplet.platform == PConstants.MACOSX) {
      try {
        OSXAdapter.setQuitHandler(this, this.getClass().getMethod("preventUserQuit"));
      } catch (final Throwable e) {
        System.err.println(e.getMessage());
      }
    }
    new Thread(() -> Runner.warmup(), "SketchRunner Warmup Thread").start();
  }

  /**
   * On Mac, even though this app has no menu, there's still a built-in cmd-Q handler that, by
   * default, quits the app. Because starting up the {@link SketchRunner} is expensive, we'd prefer
   * to leave the app running.
   *
   * <p>This function responds to a user cmd-Q by stopping the currently running sketch, and
   * rejecting the attempt to quit.
   *
   * <p>But if we've received a shutdown request from the {@link SketchServiceProcess} on the PDE
   * VM, then we permit the quit to proceed.
   *
   * @return true iff the SketchRunner should quit.
   */
  public boolean preventUserQuit() {
    if (shutdownWasRequested) {
      log("Permitting quit.");
      return true;
    }
    log("Cancelling quit, but stopping sketch.");
    new Thread(() -> stopSketch()).start();
    return false;
  }

  @Override
  public void shutdown() {
    shutdownWasRequested = true;
    log("Calling system.exit(0)");
    System.exit(0);
  }

  @Override
  public void startSketch(final PdeSketch sketch) {
    runner =
        new Thread(
            () -> {
              try {
                try {
                  final Printer stdout =
                      new Printer() {
                        @Override
                        public void print(final Object o) {
                          try {
                            modeService.printStdOut(id, String.valueOf(o));
                          } catch (final RemoteException e) {
                            System.err.println(e);
                          }
                        }

                        @Override
                        public void flush() {
                          // no-op
                        }
                      };
                  final Printer stderr =
                      new Printer() {
                        @Override
                        public void print(final Object o) {
                          try {
                            modeService.printStdErr(id, String.valueOf(o));
                          } catch (final RemoteException e) {
                            System.err.println(e);
                          }
                        }

                        @Override
                        public void flush() {
                          // no-op
                        }
                      };
                  final SketchPositionListener sketchPositionListener =
                      leftTop -> {
                        try {
                          modeService.handleSketchMoved(id, leftTop);
                        } catch (final RemoteException e) {
                          System.err.println(e);
                        }
                      };
                  Runner.runSketchBlocking(sketch, stdout, stderr, sketchPositionListener);
                } catch (final PythonSketchError e1) {
                  log("Sketch runner caught " + e1);
                  if (e1.getMessage().startsWith("SystemExit")) {
                    // Someone called sys.exit(). No-op.
                  } else {
                    modeService.handleSketchException(
                        id, convertPythonSketchError(e1, sketch.codeFileNames));
                  }
                } catch (final Exception e2) {
                  if (e2.getCause() != null && e2.getCause() instanceof PythonSketchError) {
                    modeService.handleSketchException(
                        id,
                        convertPythonSketchError(
                            (PythonSketchError) e2.getCause(), sketch.codeFileNames));
                  } else {
                    modeService.handleSketchException(id, e2);
                  }
                } finally {
                  log("Handling sketch stoppage...");
                  modeService.handleSketchStopped(id);
                }
              } catch (final RemoteException e3) {
                log(e3.toString());
              }
              // Exiting; no need to interrupt and join it later.
              runner = null;
            },
            "processing.py mode runner");
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

  private static void launch(final String id, final ModeService modeService)
      throws RMIProblem, RemoteException {
    final SketchRunner sketchRunner = new SketchRunner(id, modeService);
    final SketchService stub = (SketchService) RMIUtils.export(sketchRunner);
    log("Calling mode's handleReady().");
    modeService.handleReady(id, stub);
    Runtime.getRuntime()
        .addShutdownHook(
            new Thread(
                () -> {
                  log("Exiting; telling modeService.");
                  try {
                    modeService.handleSketchStopped(id);
                  } catch (final RemoteException e) {
                    // nothing we can do about it now.
                  }
                }));
  }

  private SketchException convertPythonSketchError(
      final PythonSketchError e, final String[] fileNames) {
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
