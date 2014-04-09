package jycessing;

import org.python.util.InteractiveConsole;

public class PreparedPythonSketch {

  private final InteractiveConsole interp;
  private final PAppletJythonDriver applet;
  private final String[] args;

  public PreparedPythonSketch(InteractiveConsole interp, PAppletJythonDriver applet,
                              final String[] args) {
    this.interp = interp;
    this.applet = applet;
    this.args = args;
  }

  public void runBlocking() throws PythonSketchError {
    interp.setOut(System.out);
    interp.setErr(System.err);
    try {
      applet.runAndBlock(args);
    } finally {
      interp.cleanup();
    }
  }
}
