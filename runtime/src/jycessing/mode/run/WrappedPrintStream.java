package jycessing.mode.run;

import java.io.OutputStream;
import java.io.PrintStream;

public abstract class WrappedPrintStream extends PrintStream {

  public WrappedPrintStream(OutputStream out) {
    super(out);
  }

  public abstract void doPrint(String s);

  public abstract void doPrintln(String s);

  @Override
  public void print(String s) {
    doPrint(s);
  }

  @Override
  public void println(String s) {
    doPrintln(s);
  }

  @Override
  public void print(boolean b) {
    print(String.valueOf(b));
  }

  @Override
  public void print(char c) {
    print(String.valueOf(c));
  }

  @Override
  public void print(char[] s) {
    print(String.valueOf(s));
  }

  @Override
  public void print(double d) {
    print(String.valueOf(d));
  }

  @Override
  public void print(float f) {
    print(String.valueOf(f));
  }

  @Override
  public void print(int i) {
    print(String.valueOf(i));
  }

  @Override
  public void print(long l) {
    print(String.valueOf(l));
  }

  @Override
  public void print(Object obj) {
    print(String.valueOf(obj));
  }

  @Override
  public void println(boolean x) {
    println(String.valueOf(x));
  }

  @Override
  public void println() {
    println("");
  }

  @Override
  public void println(char x) {
    println(String.valueOf(x));
  }

  @Override
  public void println(char[] x) {
    println(String.valueOf(x));
  }

  @Override
  public void println(double x) {
    println(String.valueOf(x));
  }

  @Override
  public void println(float x) {
    println(String.valueOf(x));
  }

  @Override
  public void println(int x) {
    println(String.valueOf(x));
  }

  @Override
  public void println(long x) {
    println(String.valueOf(x));
  }

  @Override
  public void println(Object x) {
    println(String.valueOf(x));
  }

}