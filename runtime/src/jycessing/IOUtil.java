package jycessing;

import static java.nio.file.FileVisitResult.CONTINUE;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.Charset;
import java.nio.file.FileVisitOption;
import java.nio.file.FileVisitResult;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.SimpleFileVisitor;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.EnumSet;

public class IOUtil {

  private static final Charset UTF8 = Charset.forName("utf-8");

  public static class ResourceReader {
    private final Class<?> clazz;

    public ResourceReader(final Class<?> clazz) {
      this.clazz = clazz;
    }

    public String readText(final String resource) {
      return IOUtil.readResourceAsText(clazz, resource);
    }
  }

  public static String readResourceAsText(final Class<?> clazz, final String resource) {
    try (final InputStream in = clazz.getResourceAsStream(resource)) {
      return readText(in);
    } catch (final IOException e) {
      throw new RuntimeException(e);
    }
  }

  public static String readText(final InputStream in) throws IOException {
    return new String(readFully(in), UTF8);
  }

  public static String readText(final Path path) throws IOException {
    return new String(Files.readAllBytes(path), UTF8);
  }

  /**
   * Recursively deletes the given directory or file.
   * @param target Path of file to be deleted.
   * @throws IOException
   */
  public static void rm(final Path target) throws IOException {
    Files.walkFileTree(target, new SimpleFileVisitor<Path>() {
      @Override
      public FileVisitResult visitFile(final Path file, final BasicFileAttributes attrs)
          throws IOException {
        Files.delete(file);
        return CONTINUE;
      }

      @Override
      public FileVisitResult postVisitDirectory(final Path dir, final IOException exc)
          throws IOException {
        if (exc != null) {
          throw exc;
        }
        Files.delete(dir);
        return CONTINUE;
      }
    });
  }

  public static void copy(final Path src, final Path target) throws IOException {
    final Path dest = Files.isDirectory(target) ? target.resolve(src.getFileName()) : target;
    final EnumSet<FileVisitOption> doNotResolveLinks = EnumSet.noneOf(FileVisitOption.class);
    Files.walkFileTree(src, doNotResolveLinks, Integer.MAX_VALUE, new TreeCopier(src, dest));
  }

  public static byte[] readFully(final InputStream in) throws IOException {
    try (final ByteArrayOutputStream bytes = new ByteArrayOutputStream(1024)) {
      final byte[] buf = new byte[1024];
      int n;
      while ((n = in.read(buf)) != -1) {
        bytes.write(buf, 0, n);
      }
      return bytes.toByteArray();
    }
  }
}
