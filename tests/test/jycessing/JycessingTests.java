package test.jycessing;

import junit.framework.Assert;
import jycessing.Runner;

import org.junit.Test;

public class JycessingTests {
    @Test
    public void urllib2() {
        try {
            Runner.runSketch(new String[] { "urllib2" }, "urllib2.py", "import urllib2");
        } catch (Exception e) {
            Assert.fail(e.getMessage());
        }
    }
}
