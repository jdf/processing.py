package jycessing;

import org.python.core.Py;
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

  public void runBlocking() {
    try {
      applet.runAndBlock(args);
    } catch (final Throwable t) {
      Py.printException(t);
    } finally {
      interp.cleanup();
    }
  }
}
