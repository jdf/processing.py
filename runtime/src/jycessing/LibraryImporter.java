package jycessing;

import org.python.core.Py;
import org.python.core.PyObject;
import org.python.core.PyStringMap;
import org.python.google.common.base.Joiner;
import org.python.util.InteractiveConsole;

import java.io.File;
import java.io.IOException;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.Arrays;
import java.util.Enumeration;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;

/**
 * {@link LibraryImporter} contributes the add_library function to processing.py.
 * 
 * <p>add_library causes the given Processing library (all of its jar files and
 * library subdirectories potentially containing native code) to be added to the
 * system {@link ClassLoader}, the native code search path, and the Jython sys.path.
 * It then generates import statements bringing all top-level classes available
 * in the main library jar file into the sketch's namespace.
 * 
 * <p>Note: Once jar files and directories have been added in this fashion to the
 * classloader and native lib search path, they're good and stuck there. In practice,
 * this hasn't presented any difficulty. But it's good to keep in mind.
 */
class LibraryImporter {
  private static void log(final String msg) {
    if (Runner.VERBOSE) {
      System.err.println(LibraryImporter.class.getSimpleName() + ": " + msg);
    }
  }

  /*
   * Directories where libraries may be found.
   */
  private final List<File> libSearchPath;

  /*
   * Keep track of add_library() calls we've already seen, to avoid double-loading.
   */
  private final Set<String> loadedLibs = new HashSet<>();

  /*
   * The interpreter to exec "from com.foo import Bar" statements.
   */
  private final InteractiveConsole interp;

  public LibraryImporter(final List<File> libdirs, final InteractiveConsole interp) {
    this.libSearchPath = libdirs;
    this.interp = interp;

    // Define the add_library function in the sketch interpreter.
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

  protected void addLibrary(final String libName) {
    // Don't double-load anything.
    if (loadedLibs.contains(libName)) {
      return;
    }
    loadedLibs.add(libName);

    // Find a directory with the given library name in the libSearchPath.
    File libNameDir = null;
    for (final File libDir : libSearchPath) {
      libNameDir = new File(String.format("%s/%s", libDir.getAbsolutePath(), libName));
      if (libNameDir.exists()) {
        break;
      }
    }
    if (libNameDir == null || !libNameDir.exists()) {
      // Raise the exception in the interpreter, which will give us nice line numbers
      // when the error is reported in the PDE editor.
      interp.exec("raise Exception('This sketch requires the \"" + libName + "\" library.')");
    }

    final File library = new File(libNameDir, "library");

    addToRuntime(library);

    // Find the main library jar file, which can be found at libname/library/libname.jar.
    final String jarPath = String.format("%s/%s.jar", library.getAbsolutePath(), libName);
    try {
      importPublicClassesFromJar(jarPath);
    } catch (final IOException e) {
      throw new RuntimeException("While trying to add " + libName + " library:", e);
    }
  }

  /**
   * Recursively add the given file to the system classloader, the native lib
   * search path, and the Jython sys.path.
   * 
   * <p>The given file should be either a directory or a jar file.
   * 
   * @param file The directory or jar file to make available to sketch runtime.
   */
  private void addToRuntime(final File file) {
    addJarToClassLoader(file);
    if (file.isDirectory()) {
      addDirectoryToNativeSearchPath(file);
    }
    Py.getSystemState().path.insert(0, Py.newString(file.getAbsolutePath()));
    if (file.isDirectory()) {
      for (final File f : file.listFiles()) {
        if (f.isDirectory() || f.getName().endsWith(".jar")) {
          addToRuntime(f);
        }
      }
    }
  }

  /**
   * Use a brittle and egregious hack to forcibly add the given jar file to the
   * system classloader.
   * @param jar The jar to add to the system clsasloader.
   */
  private void addJarToClassLoader(final File jar) {
    try {
      final URL url = jar.toURI().toURL();
      final URLClassLoader ucl = (URLClassLoader)ClassLoader.getSystemClassLoader();
      // Linear search for url. It's ok for this to be slow.
      for (final URL existing : ucl.getURLs()) {
        if (existing.equals(url)) {
          return;
        }
      }
      log("Appending " + url + " to the system classloader.");
      final Method addUrl = URLClassLoader.class.getDeclaredMethod("addURL", URL.class);
      addUrl.setAccessible(true);
      addUrl.invoke(ucl, url);
    } catch (NoSuchMethodException | SecurityException | IllegalAccessException
        | IllegalArgumentException | InvocationTargetException | MalformedURLException e) {
      throw new RuntimeException(e);
    }
  }

  /**
   * Add the given path to the list of paths searched for DLLs (as in those
   * loaded by loadLibrary). A hack, which depends on the presence of a
   * particular field in ClassLoader. Known to work on all recent Sun JVMs and
   * OS X.
   *
   * <p>
   * See <a href="http://forums.sun.com/thread.jspa?threadID=707176">this
   * thread</a>.
   */
  private void addDirectoryToNativeSearchPath(final File dllDir) {
    final String newPath = dllDir.getAbsolutePath();
    try {
      final Field field = ClassLoader.class.getDeclaredField("usr_paths");
      field.setAccessible(true);
      final String[] paths = (String[])field.get(null);
      for (final String path : paths) {
        if (newPath.equals(path)) {
          return;
        }
      }
      final String[] tmp = Arrays.copyOf(paths, paths.length + 1);
      tmp[paths.length] = newPath;
      field.set(null, tmp);
      log("Added " + newPath + " to java.library.path.");
    } catch (final Exception e) {
      System.err.println("While attempting to add " + newPath
          + " to the processing.py library search path: " + e.getClass().getSimpleName() + "--"
          + e.getMessage());
    }
  }

  /*
  Then create and execute an import statement for each top-level, named class
  in the given jar file. For example, if the library jar contains classes

    com.foo.Banana.class
    com.foo.Banana$1.class
    com.foo.Banana$2.class
    com.bar.Kiwi.class
  
  then we'll generate these import statements:
  
    from com.foo import Banana
    from com.bar import Kiwi
  */
  private void importPublicClassesFromJar(final String jarPath) throws IOException {
    try (final ZipFile file = new ZipFile(jarPath)) {
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
    }
  }
}
