package test.jycessing;

import static org.junit.Assert.assertEquals;

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

import org.junit.Test;

public class JycessingTests {

  private static String run(final String testResource) throws Exception {
    final ByteArrayOutputStream baos = new ByteArrayOutputStream();
    final PrintStream saved = System.out;
    try {
      System.err.println("Running " + testResource + " test.");
      final Path source = Paths.get("testing/resources/test_" + testResource + ".py");
      final String sourceText = new String(Files.readAllBytes(source), "utf-8");
      final SketchInfo info =
          new SketchInfo.Builder().libraries(Runner.getLibraries())
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
      Files.copy(new ByteArrayInputStream(testText.getBytes()), src,
          StandardCopyOption.REPLACE_EXISTING);
      final ByteArrayOutputStream baos = new ByteArrayOutputStream();
      final PrintStream saved = System.out;
      try {
        System.setOut(new PrintStream(baos, true));
        System.err.println("Running import " + module + " test.");
        final SketchInfo info =
            new SketchInfo.Builder().libraries(Runner.getLibraries())
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
    assertEquals("128\nset(['banana'])\nissubclass: True\nMySet(['baz'])\n", run("set"));
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
  public void loadPixels() throws Exception {
    expectOK("loadPixels");
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
}
