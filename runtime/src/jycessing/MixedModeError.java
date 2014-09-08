package jycessing;

public class MixedModeError extends PythonSketchError {
  public MixedModeError() {
    super("It looks like you're mixing \"active\" and \"static\" modes.");
  }

  public MixedModeError(final String message, final String fileName, final int line) {
    super(message, fileName, line);
  }

}
