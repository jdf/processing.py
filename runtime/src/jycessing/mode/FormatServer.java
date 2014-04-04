package jycessing.mode;

import java.io.File;

import processing.app.Base;
import processing.app.exec.StreamPump;

public class FormatServer {

  private final File modeHome;
  private Process server;

  public FormatServer(final File modeHome) {
    this.modeHome = modeHome;
  }

  public void startup() {
    final String serverpy = new File(modeHome, "formatter/format_server.py").getAbsolutePath();
    final String jython = new File(modeHome, "jython/jython.jar").getAbsolutePath();
    final ProcessBuilder pb = new ProcessBuilder(Base.getJavaPath(), "-jar", jython, serverpy);
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
