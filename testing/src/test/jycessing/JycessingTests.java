package test.jycessing;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.fail;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.io.UnsupportedEncodingException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;

import org.junit.Test;

import jycessing.MixedModeError;
import jycessing.MixedSmoothError;
import jycessing.PAppletJythonDriver;
import jycessing.Printer;
import jycessing.PythonSketchError;
import jycessing.Runner;
import jycessing.StreamPrinter;

public class JycessingTests {

  private static class CapturingPrinter implements Printer {
    private final ByteArrayOutputStream baos = new ByteArrayOutputStream();
    private final PrintStream out = new PrintStream(baos, true);

    @Override
    public void print(final Object o) {
      out.print(String.valueOf(o));
    }

    @Override
    public void flush() {
      out.flush();
    }

    public String getText() {
      try {
        return new String(baos.toByteArray(), "utf-8")
            .replaceAll("\r\n", "\n")
            .replaceAll("\r", "\n");
      } catch (final UnsupportedEncodingException e) {
        throw new RuntimeException(e);
      }
    }
  }

  private static String run(final String testResource) throws Exception {
    System.err.println("Running " + testResource + " test.");
    final Path source = Paths.get("testing/resources/test_" + testResource + ".py");
    final String sourceText = new String(Files.readAllBytes(source), "utf-8");
    final TestSketch sketch = new TestSketch(source, sourceText, "test " + testResource);
    final CapturingPrinter out = new CapturingPrinter();
    try {
      Runner.runSketchBlocking(sketch, out, new StreamPrinter(System.err));
    } finally {
      System.err.println(out.getText());
    }
    return out.getText();
  }

  private static void testImport(final String module) throws Exception {
    final Path tmp = Files.createTempDirectory("jycessing");
    final Path src = Paths.get(tmp.toString(), "test_import_" + module + ".pyde");
    try {
      final String testText = "import " + module + "\nprint 'OK'\nexit()";
      Files.copy(
          new ByteArrayInputStream(testText.getBytes("utf-8")),
          src,
          StandardCopyOption.REPLACE_EXISTING);
      final CapturingPrinter out = new CapturingPrinter();
      System.err.println("Running import " + module + " test.");
      final TestSketch sketch = new TestSketch(src, testText, "test import " + module);
      Runner.runSketchBlocking(sketch, out, new StreamPrinter(System.err));
      assertEquals("OK\n", out.getText());
    } finally {
      Files.delete(src);
      Files.delete(tmp);
    }
  }

  private static void expectOK(final String testName) throws Exception {
    assertEquals("OK\n", run(testName));
  }

  @Test
  public void inherit_str() throws Exception {
    assertEquals("cosmic\n12\n[12, 13]\n", run("inherit_str"));
  }

  @Test
  public void static_size() throws Exception {
    expectOK("static_size");
  }

  @Test
  public void filter_builtins() throws Exception {
    expectOK("filter");
  }

  @Test
  public void set_builtins() throws Exception {
    expectOK("set");
  }

  @Test
  public void map_builtins() throws Exception {
    assertEquals("50\n13\n", run("map"));
  }

  @Test
  public void md5() throws Exception {
    expectOK("md5");
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
    expectOK("load_in_initializer");
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
    expectOK("pvector");
  }

  @Test
  public void pixels() throws Exception {
    expectOK("pixels");
  }

  @Test
  public void unicode() throws Exception {
    expectOK("unicode");
  }

  @Test
  public void primitives() throws Exception {
    assertEquals("66.7\n", run("primitives"));
  }

  @Test
  public void millis() throws Exception {
    expectOK("millis");
  }

  @Test
  public void imports() throws Exception {
    expectOK("import");
  }

  @Test
  public void pvector_import() throws Exception {
    expectOK("pvector_in_imported_module");
  }

  @Test
  public void exit_builtin() throws Exception {
    expectOK("exit");
  }

  @Test
  public void exit_builtin_twice() throws Exception {
    expectOK("exit");
    expectOK("exit");
  }

  @Test
  public void csv() throws Exception {
    // We do it twice because this exposed a critical bug in the
    // re-initialization code (namely, that Py.None had different
    // values on successive runs, but something was holding on to
    // the old value.
    testImport("csv");
    testImport("csv");
  }

  @Test
  public void hex() throws Exception {
    expectOK("hex");
  }

  @Test
  public void color() throws Exception {
    expectOK("color");
  }

  @Test
  public void loadThings() throws Exception {
    expectOK("loadthings");
  }

  @Test
  public void writeThings() throws Exception {
    expectOK("writethings");
  }

  @Test
  public void constrain() throws Exception {
    expectOK("constrain");
  }

  @Test
  public void detectMixedMode() throws Exception {
    try {
      run("mixed_mode_error");
      fail("Expected mixed mode error.");
    } catch (final MixedModeError expected) {
      // noop
    }
  }

  @Test
  public void c_logical_and() throws Exception {
    try {
      run("c_logical_and");
      fail("Expected syntax error.");
    } catch (final PythonSketchError expected) {
      assertEquals(PAppletJythonDriver.C_LIKE_LOGICAL_AND_ERROR_MESSAGE, expected.getMessage());
    }
  }

  @Test
  public void c_logical_or() throws Exception {
    try {
      run("c_logical_or");
      fail("Expected syntax error.");
    } catch (final PythonSketchError expected) {
      assertEquals(PAppletJythonDriver.C_LIKE_LOGICAL_OR_ERROR_MESSAGE, expected.getMessage());
    }
  }

  @Test
  public void lerpColorStaticMode() throws Exception {
    expectOK("lerp_color_static_mode");
  }

  @Test
  public void lerpColorBeforeSetup() throws Exception {
    expectOK("lerp_color_before_setup");
  }

  @Test
  public void keyDefinedBeforeKeyEvent() throws Exception {
    expectOK("key_before_key_event");
  }

  @Test
  public void randintDomainRegression() throws Exception {
    expectOK("randint_domain_regression");
  }

  // https://github.com/jdf/processing.py/issues/167
  @Test
  public void syspathappend() throws Exception {
    expectOK("syspathappend");
  }

  // https://github.com/jdf/Processing.py-Bugs/issues/148
  @Test
  public void from_future_with_settings() throws Exception {
    expectOK("from_future_with_settings");
  }

  // https://github.com/jdf/processing.py/issues/199
  @Test
  public void matrix3d_print() throws Exception {
    final String actual = run("pmatrixprint");
    final String expected =
        " 1.0000  0.0000  0.0000  0.0000\n"
            + " 0.0000  1.0000  0.0000  0.0000\n"
            + " 0.0000  0.0000  1.0000  0.0000\n"
            + " 0.0000  0.0000  0.0000  1.0000\n\n";
    assertEquals(expected, actual);
  }

  // https://github.com/jdf/processing.py/issues/264
  @Test
  public void unittest() throws Exception {
    expectOK("unittest");
  }

  // https://github.com/jdf/processing.py/issues/251
  @Test
  public void detectMixedSmooth() throws Exception {
    try {
      run("mixed_smooth_error");
      fail("Expected mixed smooth error.");
    } catch (final MixedSmoothError expected) {
      // noop
    }
  }

  // https://github.com/jdf/processing.py/issues/280
  @Test
  public void g() throws Exception {
    expectOK("g");
  }

  @Test
  public void keyPressed_redefined() throws Exception {
    expectOK("keyPressed_redefined");
  }

  //https://github.com/jdf/processing.py/issues/281
  @Test
  public void thread() throws Exception {
    expectOK("thread");
  }
}
