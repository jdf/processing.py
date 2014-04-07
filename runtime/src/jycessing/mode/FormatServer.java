package jycessing.mode;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.IOException;
import java.net.Socket;

import processing.app.Base;
import processing.app.Formatter;
import processing.app.exec.StreamPump;

/**
 * This class manages running and communicating with a server that knows how to pretty-print
 * Python source code. The server is written in python. If a CPython interpreter is available,
 * we'll use it; otherwise we start up a Java processes using Jython to run the server.
 */
public class FormatServer implements Formatter {

  private final File modeHome;
  private Process server;

  public FormatServer(final File modeHome) {
    this.modeHome = modeHome;
  }

  private static boolean nativePythonAvailable() {
    try {
      return Runtime.getRuntime().exec("python --version").waitFor() == 0;
    } catch (Exception e) {
      return false;
    }
  }

  /**
   * If a python exectuable is available on this machine, use it to run the formatting server.
   * Otherwise, use the same Java that ran the PDE to interpret the formatting server with
   * Jython, which takes a very long time to start up.
   * @param formatServerPath Path to the format server script source.
   * @return a ProcessBuilder that, when started, will run the formatting server.
   */
  private ProcessBuilder getPythonProcess(final String formatServerPath) {
    if (nativePythonAvailable()) {
      System.err.println("Native python available for formatting.");
      return new ProcessBuilder("python", formatServerPath);
    }
    System.err.println("Native python not available for formatting.");
    final String jython = new File(modeHome, "mode/jython.jar").getAbsolutePath();
    return new ProcessBuilder(Base.getJavaPath(), "-jar", jython, formatServerPath);
  }

  /**
   * Starts the formatting server.
   */
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

  /**
   * Called as a ShutdownHook. Stops the formatting server.
   */
  public void shutdown() {
    sendShutdown();
    server.destroy();
    server = null;
  }

  @Override
  public String format(String text) {
    try {
      // Connect to format server.
      final Socket sock = new Socket("localhost", 10011);
      try {
        final DataOutputStream out = new DataOutputStream(sock.getOutputStream());
        final DataInputStream in = new DataInputStream(sock.getInputStream());

        final byte[] encoded = text.getBytes("utf-8");
        // Send big-endian encoded integer representing length of utf-8 encoded source code.
        out.writeInt(encoded.length);
        // Send bytes of utf-8 encoded source code.
        out.write(encoded);
        out.flush();

        // Read length of result.
        final int resultLength = in.readInt();
        // Read utf-8 encoded string.
        final byte[] buf = new byte[resultLength];
        in.readFully(buf);
        return new String(buf, "utf-8");
      } finally {
        sock.close();
      }
    } catch (IOException e) {
      System.err.println(e);
      return text;
    }
  }

  /**
   * Tells the formatting server to shut down gracefully.
   */
  private void sendShutdown() {
    System.err.println("Sending shutdown message to format server.");
    try {
      final Socket sock = new Socket("localhost", 10011);
      try {
        final DataOutputStream out = new DataOutputStream(sock.getOutputStream());
        // -1 is a sentinel value meaning "die".
        out.writeInt(-1);
        out.flush();
      } finally {
        sock.close();
      }
    } catch (IOException e) {
      System.err.println(e);
    }
  }
}
