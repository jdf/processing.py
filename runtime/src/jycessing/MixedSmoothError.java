package jycessing;

public class MixedSmoothError extends PythonSketchError {
  public MixedSmoothError() {
    super("smooth() and noSmooth() cannot be used in the same sketch.");
  }

  public MixedSmoothError(final String message, final String fileName, final int line) {
    super(message, fileName, line);
  }
}
