package jycessing;

/*
 * Copyright (c) 2008, 2010, Oracle and/or its affiliates. All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 *   - Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *
 *   - Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in the
 *     documentation and/or other materials provided with the distribution.
 *
 *   - Neither the name of Oracle nor the names of its
 *     contributors may be used to endorse or promote products derived
 *     from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
 * IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR
 * CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 * PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 * NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

import static java.nio.file.FileVisitResult.CONTINUE;
import static java.nio.file.FileVisitResult.SKIP_SUBTREE;
import static java.nio.file.StandardCopyOption.COPY_ATTRIBUTES;
import static java.nio.file.StandardCopyOption.REPLACE_EXISTING;

import java.io.IOException;
import java.nio.file.FileAlreadyExistsException;
import java.nio.file.FileSystemLoopException;
import java.nio.file.FileVisitResult;
import java.nio.file.FileVisitor;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.attribute.BasicFileAttributes;
import java.nio.file.attribute.FileTime;

class TreeCopier implements FileVisitor<Path> {

  /** Copy source file to target location. */
  static void copyFile(final Path source, final Path target) {
    try {
      Files.copy(source, target, COPY_ATTRIBUTES, REPLACE_EXISTING);
    } catch (final IOException x) {
      System.err.format("Unable to copy: %s: %s%n", source, x);
    }
  }

  private final Path source;
  private final Path target;

  TreeCopier(final Path source, final Path target) {
    this.source = source;
    this.target = target;
  }

  @Override
  public FileVisitResult preVisitDirectory(final Path dir, final BasicFileAttributes attrs) {
    // before visiting entries in a directory we copy the directory
    // (okay if directory already exists).
    final Path newdir = target.resolve(source.relativize(dir));
    try {
      Files.copy(dir, newdir, COPY_ATTRIBUTES);
    } catch (final FileAlreadyExistsException x) {
      // ignore
    } catch (final IOException x) {
      System.err.format("Unable to create: %s: %s%n", newdir, x);
      return SKIP_SUBTREE;
    }
    return CONTINUE;
  }

  @Override
  public FileVisitResult visitFile(final Path file, final BasicFileAttributes attrs) {
    copyFile(file, target.resolve(source.relativize(file)));
    return CONTINUE;
  }

  @Override
  public FileVisitResult postVisitDirectory(final Path dir, final IOException exc) {
    // fix up modification time of directory when done
    if (exc == null) {
      final Path newdir = target.resolve(source.relativize(dir));
      try {
        final FileTime time = Files.getLastModifiedTime(dir);
        Files.setLastModifiedTime(newdir, time);
      } catch (final IOException x) {
        System.err.format("Unable to copy all attributes to: %s: %s%n", newdir, x);
      }
    }
    return CONTINUE;
  }

  @Override
  public FileVisitResult visitFileFailed(final Path file, final IOException exc) {
    if (exc instanceof FileSystemLoopException) {
      System.err.println("cycle detected: " + file);
    } else {
      System.err.format("Unable to copy: %s: %s%n", file, exc);
    }
    return CONTINUE;
  }
}
