package jycessing.launcher;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

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
  public static void copyTo(String name, String path) throws IOException {
    final InputStream in = LaunchHelper.class.getResourceAsStream(name);
    final OutputStream out = new FileOutputStream(path);

    byte[] buffer = new byte[128 * 1024];
    int len;
    while ((len = in.read(buffer)) != -1) {
      out.write(buffer, 0, len);
    }

    out.close();
    in.close();
  }
}
