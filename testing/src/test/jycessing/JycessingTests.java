package test.jycessing;

import static org.junit.Assert.assertEquals;

import org.junit.Test;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;

import jycessing.Runner;
import jycessing.Runner.LibraryPolicy;
import jycessing.mode.RunMode;
import jycessing.mode.run.SketchInfo;

public class JycessingTests {
  private static String run(final String testResource) throws Exception {
    final ByteArrayOutputStream baos = new ByteArrayOutputStream();
    final PrintStream saved = System.out;
    try {
      System.err.println("Running " + testResource + " test.");
      final Path source = Paths.get("testing/resources/test_" + testResource + ".py");
      final String sourceText = new String(Files.readAllBytes(source), "utf-8");
      final SketchInfo info =
          new SketchInfo.Builder().sketchName("test " + testResource)
              .libraryPolicy(LibraryPolicy.SELECTIVE).code(sourceText).sketch(source.toFile())
              .runMode(RunMode.UNIT_TEST).build();
      System.setOut(new PrintStream(baos, true));
      Runner.runSketchBlocking(info);
      return new String(baos.toByteArray()).replaceAll("\r\n", "\n").replaceAll("\r", "\n");
    } finally {
      System.setOut(saved);
    }
  }

  private static void testImport(final String module) throws Exception {
    final Path tmp = Files.createTempDirectory("jycessing");
    final Path src = Paths.get(tmp.toString(), "test_import_" + module + ".pyde");
    try {
      final String testText = "import " + module + "\nprint 'OK'\nexit()";
      Files.copy(new ByteArrayInputStream(testText.getBytes("utf-8")), src,
          StandardCopyOption.REPLACE_EXISTING);
      final ByteArrayOutputStream baos = new ByteArrayOutputStream();
      final PrintStream saved = System.out;
      try {
        System.setOut(new PrintStream(baos, true));
        System.err.println("Running import " + module + " test.");
        final SketchInfo info =
            new SketchInfo.Builder().sketchName("test import " + module)
                .libraryPolicy(LibraryPolicy.SELECTIVE).code(testText).sketch(src.toFile())
                .runMode(RunMode.UNIT_TEST).build();
        Runner.runSketchBlocking(info);
        assertEquals("OK\n",
            new String(baos.toByteArray()).replaceAll("\r\n", "\n").replaceAll("\r", "\n"));
      } finally {
        System.setOut(saved);
      }
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
  public void launcher() throws Exception {
    assertEquals("CMLx\n", run("launcher"));
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
  public void autoglobal() throws Exception {
    /*
    * Python Mode changes the semantics of Python by treating the main
    * module (the "sketch" file) as a special case in which any reference
    * to an existing global (module local) is treated as global, so that
    * you can mutate a global without the "global" keyword.
    */
    expectOK("autoglobal");
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
}
