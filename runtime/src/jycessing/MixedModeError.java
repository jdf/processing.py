package jycessing;

public class MixedModeError extends PythonSketchError {
  public MixedModeError() {
    super("It looks like you're mising \"active\" and \"static\" modes.");
  }
}
