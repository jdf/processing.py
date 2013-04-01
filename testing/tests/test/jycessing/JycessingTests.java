package test.jycessing;

import static junit.framework.Assert.assertEquals;

import org.junit.Test;
import org.junit.runner.JUnitCore;

import jycessing.Runner;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

public class JycessingTests {

  private static String run(final String testResource) throws Exception {
    final ByteArrayOutputStream baos = new ByteArrayOutputStream();
    final PrintStream saved = System.out;
    try {
      System.setOut(new PrintStream(baos, true));
      Runner.runFromCommandLineArguments(new String[] { "testing/test_resources/test_"
          + testResource + ".py" });
      return new String(baos.toByteArray()).replaceAll("\r\n", "\n").replaceAll("\r", "\n");
    } finally {
      System.setOut(saved);
    }
  }

  private static void testImport(final String module) throws Exception {
    final ByteArrayOutputStream baos = new ByteArrayOutputStream();
    final PrintStream saved = System.out;
    try {
      System.setOut(new PrintStream(baos, true));
      final String testClass = module + "_test";
      final String bogusFileName = "<test " + module + ">";
      final String testText = "import " + module + "\nprint 'OK'\nexit()";
      Runner.runSketch(new String[] { testClass }, bogusFileName, testText);
      assertEquals("OK\n",
          new String(baos.toByteArray()).replaceAll("\r\n", "\n").replaceAll("\r", "\n"));
    } finally {
      System.setOut(saved);
    }
  }

  @Test
  public void inherit_str() throws Exception {
    assertEquals("cosmic\n12\n[12, 13]\n", run("inherit_str"));
  }

  @Test
  public void static_size() throws Exception {
    assertEquals("OK\n", run("static_size"));
  }

  @Test
  public void set_builtins() throws Exception {
    assertEquals("128\nset(['banana'])\nissubclass: True\nMySet(['baz'])\n", run("set"));
  }

  @Test
  public void map_builtins() throws Exception {
    assertEquals("50\n13\n", run("map"));
  }

  @Test
  public void md5() throws Exception {
    assertEquals("bb649c83dd1ea5c9d9dec9a18df0ffe9\n", run("md5"));
  }

  @Test
  public void urllib2() throws Exception {
    testImport("urllib2");
  }

  @Test
  public void urllib() throws Exception {
    testImport("urllib");
  }

  @Test
  public void load_in_initializer() throws Exception {
    assertEquals("OK\n", run("load_in_initializer"));
  }

  @Test
  public void datetime() throws Exception {
    testImport("datetime");
  }

  @Test
  public void calendar() throws Exception {
    testImport("calendar");
  }

  @Test
  public void processing_core() throws Exception {
    assertEquals("[ 1.0, 2.0, 3.0 ]\n<type 'processing.core.PFont'>\n", run("pcore"));
  }

  @Test
  public void pvector() throws Exception {
    assertEquals("OK\n", run("pvector"));
  }

  @Test
  public void loadPixels() throws Exception {
    assertEquals("OK\n", run("loadPixels"));
  }

  @Test
  public void unicode() throws Exception {
    assertEquals("OK\n", run("unicode"));
  }

  public static void main(final String[] args) {
    JUnitCore.runClasses(JycessingTests.class);
  }
}
