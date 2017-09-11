package jycessing;

import java.io.PrintStream;

public class StreamPrinter implements Printer {

  private final PrintStream stream;

  public StreamPrinter(final PrintStream stream) {
    this.stream = stream;
  }

  @Override
  public void print(final Object o) {
    stream.print(String.valueOf(o));
    stream.flush();
  }

  @Override
  public void flush() {
    stream.flush();
  }
}
