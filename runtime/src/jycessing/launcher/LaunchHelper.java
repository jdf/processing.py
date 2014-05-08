package jycessing.launcher;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;

import jycessing.IOUtil;

/**
 * Launch and deployment service for various platforms.
 * 
 * @author Ralf Biedert <rb@xr.io>
 */
public class LaunchHelper {

  /**
   * Copies one of our resources to a given file.
   *  
   * @param name
   * @param path
   * @throws IOException
   */
  public static void copyResourceTo(final String name, final Path path) throws IOException {
    try (InputStream in = LaunchHelper.class.getResourceAsStream(name)) {
      Files.write(path, IOUtil.readFully(LaunchHelper.class.getResourceAsStream(name)));
    }
  }
}
