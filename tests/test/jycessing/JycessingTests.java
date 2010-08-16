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
            Runner.main(new String[] { "test_resources/test_" + testResource + ".py" });
            return new String(baos.toByteArray()).replaceAll("\r\n", "\n").replaceAll(
                    "\r", "\n");
        } finally {
            System.setOut(saved);
        }
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
        assertEquals("OK\n", run("urllib2"));
    }

    @Test
    public void urllib() throws Exception {
        assertEquals("OK\n", run("urllib"));
    }

    public static void main(final String[] args) {
        JUnitCore.runClasses(JycessingTests.class);
    }
}
