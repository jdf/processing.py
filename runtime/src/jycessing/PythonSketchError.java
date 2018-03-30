package jycessing;

public class PythonSketchError extends Exception {
  public final String fileName;
  public final int line;
  public final int column;

  public PythonSketchError(final String message) {
    this(message, null);
  }

  public PythonSketchError(final String message, final String fileName) {
    this(message, fileName, -1, -1);
  }

  public PythonSketchError(final String message, final String fileName, final int line) {
    this(message, fileName, line, 0);
  }

  public PythonSketchError(
      final String message, final String fileName, final int line, final int column) {
    super(message);

    this.fileName = fileName;
    this.line = line;
    this.column = column;
  }

  @Override
  public String toString() {
    if (fileName == null) {
      return getMessage();
    }
    if (line == -1) {
      return getMessage() + " in " + fileName;
    }
    if (column == -1) {
      return getMessage() + " at line " + line + " of " + fileName;
    }
    return getMessage() + " at " + line + ":" + column + " in " + fileName;
  }
}
