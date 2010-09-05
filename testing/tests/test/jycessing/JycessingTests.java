package test.jycessing;

import static junit.framework.Assert.assertEquals;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import jycessing.Runner;

import org.junit.Test;
import org.junit.runner.JUnitCore;

public class JycessingTests {

    private static String run(final String testResource) throws Exception {
        final ByteArrayOutputStream baos = new ByteArrayOutputStream();
        final PrintStream saved = System.out;
        try {
            System.setOut(new PrintStream(baos, true));
            Runner.main(new String[] { "testing/test_resources/test_"
                    + testResource + ".py" });
            return new String(baos.toByteArray()).replaceAll("\r\n", "\n")
                    .replaceAll("\r", "\n");
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
            final String testText = "import " + module + "\nprint 'OK'";
            Runner.runSketch(new String[] { testClass }, bogusFileName,
                    testText);
            assertEquals("OK\n",
                    new String(baos.toByteArray()).replaceAll("\r\n", "\n")
                            .replaceAll("\r", "\n"));
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
        assertEquals("128\nset(['banana'])\n", run("set"));
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

    public static void main(final String[] args) {
        JUnitCore.runClasses(JycessingTests.class);
    }
}
