package jycessing;

public class DevNullPrinter implements Printer {

  public DevNullPrinter() {}

  @Override
  public void print(final Object o) {
    // no-op
  }

  @Override
  public void flush() {
    // no-op
  }
}
