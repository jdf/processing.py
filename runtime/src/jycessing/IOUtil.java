package jycessing;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;

public class IOUtil {

  // Slurp the given Reader into a String.
  public static String read(final Reader r) throws IOException {
    final BufferedReader reader = new BufferedReader(r);
    final StringBuilder sb = new StringBuilder(1024);
    String line;
    try {
      while ((line = reader.readLine()) != null) {
        sb.append(line).append("\n");
      }
      return sb.toString();
    } finally {
      reader.close();
    }
  }

  public static String readOrDie(final InputStream in) {
    try {
      return read(in);
    } catch (final IOException e) {
      throw new RuntimeException(e);
    }
  }

  public static String read(final InputStream in) throws IOException {
    return read(new InputStreamReader(in, "UTF-8"));
  }

}
