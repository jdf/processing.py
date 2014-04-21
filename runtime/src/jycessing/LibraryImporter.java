package jycessing;

import java.io.File;
import java.io.IOException;
import java.util.Arrays;
import java.util.Enumeration;
import java.util.HashSet;
import java.util.Set;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;

import jycessing.mode.PythonMode;

import org.python.core.Py;
import org.python.core.PyObject;
import org.python.core.PyStringMap;
import org.python.google.common.base.Joiner;
import org.python.util.InteractiveConsole;

/**
 * {@link LibraryImporter} adds the add_library function to processing.py.
 * 
 * <p>add_library causes the given Processing library (all of its jar files and
 * library subdirectories potentially containing native code) to be added to the
 * Jython sys.path, and generates import statements bringing all top-level
 * classes available in the main library jar file into the sketch's namespace.
 * 
 * @author feinberg
 */
class LibraryImporter {
  private static void log(final String msg) {
    if (PythonMode.VERBOSE) {
      System.err.println(LibraryImporter.class.getSimpleName() + ": " + msg);
    }
  }

  private final File libdir;
  private final InteractiveConsole interp;
  private final Set<String> loadedLibs = new HashSet<String>();

  private boolean didAddLibraries = false;

  public LibraryImporter(final File libdir, final InteractiveConsole interp) {
    this.libdir = libdir;
    this.interp = interp;
  }

  public void initialize() {
    final PyStringMap builtins = (PyStringMap)interp.getSystemState().getBuiltins();
    builtins.__setitem__("add_library", new PyObject() {
      @Override
      public PyObject __call__(final PyObject[] args, final String[] kws) {
        log("Adding library " + args[0].asString());
        addLibrary(args[0].asString());
        return Py.None;
      }
    });
  }

  private void appendToSysPath(final File file) {
    final String appendStatement =
        String.format("sys.path.append(\"%s\")\n", file.getAbsolutePath());
    log(appendStatement);
    interp.exec(appendStatement);
    if (file.isDirectory()) {
      for (final File f : file.listFiles()) {
        if (f.isDirectory() || f.getName().endsWith(".jar")) {
          appendToSysPath(f);
        }
      }
    }
  }

  protected void addLibrary(final String libName) {
    didAddLibraries = true;

    if (loadedLibs.contains(libName)) {
      return;
    }
    loadedLibs.add(libName);

    final File libClassDir =
        new File(String.format("%s/%s/library", libdir.getAbsolutePath(), libName));

    appendToSysPath(libClassDir);

    final String jarPath = String.format("%s/%s.jar", libClassDir.getAbsolutePath(), libName);

    try {
      final ZipFile file = new ZipFile(jarPath);
      final Enumeration<? extends ZipEntry> entries = file.entries();
      while (entries.hasMoreElements()) {
        final ZipEntry entry = entries.nextElement();
        if (entry.isDirectory()) {
          continue;
        }
        final String name = entry.getName();
        if (!name.endsWith(".class")) {
          log("Rejecting non-class " + name);
          continue;
        }
        final int slash = name.lastIndexOf('/');
        if (slash == -1) {
          log("Rejecting " + name);
          continue;
        }
        if (name.contains("$")) {
          log("Rejecting " + name);
          continue;
        }
        final String[] path = name.split("/");
        final String className = path[path.length - 1].replace(".class", "");
        final String packageName =
            Joiner.on(".").join(Arrays.asList(path).subList(0, path.length - 1));

        final String importStatement = String.format("from %s import %s", packageName, className);
        log(importStatement);
        interp.exec(importStatement);
      }
      file.close();
    } catch (final IOException e) {
      throw new RuntimeException("While trying to add " + libName + " library:", e);
    }
  }

  public boolean didAddLibraries() {
    return didAddLibraries;
  }
}
