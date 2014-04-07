package jycessing.mode;

import java.io.File;
import processing.app.Base;
import processing.app.exec.StreamPump;

public class FormatServer {

  private final File modeHome;
  private Process server;

  private static boolean nativePythonAvailable() {
    try {
      return Runtime.getRuntime().exec("python --version").waitFor() == 0;
    } catch (Exception e) {
      return false;
    }
  }

  private ProcessBuilder getPythonProcess(final String formatServerPath) {
    if (nativePythonAvailable()) {
      System.err.println("Native python available for formatting.");
      return new ProcessBuilder("python", formatServerPath);
    }
    System.err.println("Native python not available for formatting.");
    final String jython = new File(modeHome, "jython/jython.jar").getAbsolutePath();
    return new ProcessBuilder(Base.getJavaPath(), "-jar", jython, formatServerPath);
  }

  public FormatServer(final File modeHome) {
    this.modeHome = modeHome;
  }

  public void startup() {
    final String serverpy = new File(modeHome, "formatter/format_server.py").getAbsolutePath();
    final ProcessBuilder pb = getPythonProcess(serverpy);
    pb.redirectErrorStream(true);
    new Thread(new Runnable() {
      @Override
      public void run() {
        try {
          System.err.println("Starting up the format server.");
          server = pb.start();
          Runtime.getRuntime().addShutdownHook(new Thread(new Runnable() {
            @Override
            public void run() {
              shutdown();
            }
          }));
          new StreamPump(server.getInputStream(), "Format Server Output").addTarget(System.err)
              .start();
        } catch (Exception e) {
          throw new RuntimeException(pb.toString(), e);
        }
      }
    }, "FormatServerStarter").start();
  }

  public void shutdown() {
    System.err.println("Shutting down format server.");
    server.destroy();
    server = null;
  }
}
