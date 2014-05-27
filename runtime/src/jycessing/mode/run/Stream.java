package jycessing.mode.run;

import java.io.PrintStream;

public enum Stream {
  ERR {
    @Override
    public PrintStream getSystemStream() {
      return System.err;
    }
  },
  OUT {
    @Override
    public PrintStream getSystemStream() {
      return System.out;
    }
  };
  abstract public PrintStream getSystemStream();
}
