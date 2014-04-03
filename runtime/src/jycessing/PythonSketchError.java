package jycessing;

public class PythonSketchError extends Exception {
  public final String file;
  public final int line;
  public final int column;

  public PythonSketchError(String message) {
    this(message, null);
  }

  public PythonSketchError(String message, String file) {
    this(message, file, -1, -1);
  }

  public PythonSketchError(String message, String file, int line) {
    this(message, file, line, 0);
  }

  public PythonSketchError(String message, String file, int line, int column) {
    super(message);

    this.file = file;
    this.line = line;
    this.column = column;
  }
}
