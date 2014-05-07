package jycessing;

import static java.nio.file.FileVisitResult.CONTINUE;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.nio.file.FileVisitOption;
import java.nio.file.FileVisitResult;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.SimpleFileVisitor;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.EnumSet;

public class IOUtil {

  // Slurp the given Reader into a String.
  public static String read(final Reader r) throws IOException {
    try (final BufferedReader reader = new BufferedReader(r)) {
      final StringBuilder sb = new StringBuilder(1024);
      String line;
      while ((line = reader.readLine()) != null) {
        sb.append(line).append("\n");
      }
      return sb.toString();
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
}
