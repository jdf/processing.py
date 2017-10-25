package jycessing;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

/** Utilities for querying the existence and properties of the system Python, if any. */
public class SystemPython {

  public static File getSystemPython() {
    return new File("/Users/feinberg/numpy/bin/python").getAbsoluteFile();
  }

  public static boolean nativePythonAvailable() {
    try {
      return Runtime.getRuntime().exec(getSystemPython().getAbsolutePath() + " --version").waitFor()
          == 0;
    } catch (final Exception e) {
      return false;
    }
  }

  public static List<String> getSysPath() {
    final List<String> result = new ArrayList<>();
    try {
      final Process p =
          new ProcessBuilder(
                  getSystemPython().getAbsolutePath(),
                  "-c",
                  "import sys\nfor p in sys.path:print p")
              .start();
      final BufferedReader in =
          new BufferedReader(new InputStreamReader(p.getInputStream(), StandardCharsets.UTF_8));
      final BufferedReader err =
          new BufferedReader(new InputStreamReader(p.getErrorStream(), StandardCharsets.UTF_8));
      String pathElement = null;
      while ((pathElement = in.readLine()) != null) {
        result.add(pathElement);
      }
      String s;
      while ((s = err.readLine()) != null) {
        System.err.println(s);
      }
      p.waitFor();
    } catch (InterruptedException | IOException e) {
      System.err.println(e);
    }
    return result;
  }
}
