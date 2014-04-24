package jycessing;

public class PythonSketchError extends Exception {
  public final String file;
  public final int line;
  public final int column;

  public PythonSketchError(final String message) {
    this(message, null);
  }

  public PythonSketchError(final String message, final String file) {
    this(message, file, -1, -1);
  }

  public PythonSketchError(final String message, final String file, final int line) {
    this(message, file, line, 0);
  }

  public PythonSketchError(final String message, final String file, final int line, final int column) {
    super(message);

    this.file = file;
    this.line = line;
    this.column = column;
  }

  @Override
  public String toString() {
    if (file == null) {
      return getMessage();
    }
    if (line == -1) {
      return getMessage() + " in " + file;
    }
    if (column == -1) {
      return getMessage() + " at line " + line + " of " + file;
    }
    return getMessage() + " at " + line + ":" + column + " in " + file;
  }
}
