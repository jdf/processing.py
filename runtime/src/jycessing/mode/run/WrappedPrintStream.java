package jycessing.mode.run;

import java.io.OutputStream;
import java.io.PrintStream;

public abstract class WrappedPrintStream extends PrintStream {

  public WrappedPrintStream(final OutputStream out) {
    super(out);
  }

  public abstract void doPrint(String s);

  public abstract void doPrintln(String s);

  @Override
  public void print(final String s) {
    doPrint(s);
  }

  @Override
  public void println(final String s) {
    doPrintln(s);
  }

  @Override
  public void print(final boolean b) {
    print(String.valueOf(b));
  }

  @Override
  public void print(final char c) {
    print(String.valueOf(c));
  }

  @Override
  public void print(final char[] s) {
    print(String.valueOf(s));
  }

  @Override
  public void print(final double d) {
    print(String.valueOf(d));
  }

  @Override
  public void print(final float f) {
    print(String.valueOf(f));
  }

  @Override
  public void print(final int i) {
    print(String.valueOf(i));
  }

  @Override
  public void print(final long l) {
    print(String.valueOf(l));
  }

  @Override
  public void print(final Object obj) {
    print(String.valueOf(obj));
  }

  @Override
  public void println(final boolean x) {
    println(String.valueOf(x));
  }

  @Override
  public void println() {
    println("");
  }

  @Override
  public void println(final char x) {
    println(String.valueOf(x));
  }

  @Override
  public void println(final char[] x) {
    println(String.valueOf(x));
  }

  @Override
  public void println(final double x) {
    println(String.valueOf(x));
  }

  @Override
  public void println(final float x) {
    println(String.valueOf(x));
  }

  @Override
  public void println(final int x) {
    println(String.valueOf(x));
  }

  @Override
  public void println(final long x) {
    println(String.valueOf(x));
  }

  @Override
  public void println(final Object x) {
    println(String.valueOf(x));
  }

}
