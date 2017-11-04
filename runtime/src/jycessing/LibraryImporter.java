package jycessing;

import java.io.File;
import java.io.FileFilter;
import java.io.FileReader;
import java.io.IOException;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.Set;
import java.util.regex.Pattern;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;

import org.python.core.Py;
import org.python.core.PyObject;
import org.python.core.PyStringMap;
import org.python.core.PySystemState;
import org.python.google.common.base.Joiner;
import org.python.util.InteractiveConsole;

import processing.core.PApplet;

/**
 * {@link LibraryImporter} contributes the add_library function to processing.py.
 *
 * <p>add_library causes the given Processing library (all of its jar files and library
 * subdirectories potentially containing native code) to be added to the system {@link ClassLoader},
 * the native code search path, and the Jython sys.path. It then generates import statements
 * bringing all top-level classes available in the main library jar file into the sketch's
 * namespace.
 *
 * <p>Note: Once jar files and directories have been added in this fashion to the classloader and
 * native lib search path, they're good and stuck there. In practice, this hasn't presented any
 * difficulty. But it's good to keep in mind.
 */
class LibraryImporter {
  private static void log(final String msg) {
    if (Runner.VERBOSE) {
      System.err.println(LibraryImporter.class.getSimpleName() + ": " + msg);
    }
  }

  private static final String PLATFORM = PApplet.platformNames[PApplet.platform];
  private static final String BITS = System.getProperty("os.arch").contains("64") ? "64" : "32";

  /*
   * Directories where libraries may be found.
   */
  private final List<File> libSearchPath;

  /*
   * Keep track of add_library() calls we've already seen, to avoid double-loading.
   */
  private final Set<String> loadedLibs = new HashSet<>();

  /*
   * The interpreter into which we inject import statements.
   */
  private final InteractiveConsole interp;

  public LibraryImporter(final List<File> libdirs, final InteractiveConsole interp) {
    this.libSearchPath = libdirs;
    this.interp = interp;

    // Define the add_library function in the sketch interpreter.
    final PyStringMap builtins = (PyStringMap) interp.getSystemState().getBuiltins();
    builtins.__setitem__(
        "add_library",
        new PyObject() {
          @Override
          public PyObject __call__(final PyObject[] args, final String[] kws) {
            log("Adding library " + args[0].asString());
            addLibrary(args[0].asString());
            return Py.None;
          }
        });
  }

  /**
   * Locate the library in the library folder "libName", find what it exports for the current
   * platform, and add exports to the system classpath, the system native library path, and jython's
   * sys.path.
   *
   * <p>Then, go through the main jar file of the library and import all of its publicly exposed
   * classes.
   *
   * @param libName The name of the library to import
   */
  protected void addLibrary(final String libName) {
    // Don't double-load anything.
    if (loadedLibs.contains(libName)) {
      log("...never mind, we already did");
      return;
    }
    loadedLibs.add(libName);

    File libDir = null;
    for (final File searchDir : libSearchPath) {
      // Permit hand-rolled single-jar libraries:
      final File handRolledJar = new File(searchDir.getAbsoluteFile(), libName + ".jar");
      if (handRolledJar.exists()) {
        log("Found hand-rolled jar lib " + handRolledJar);
        addJarToClassLoader(handRolledJar);
        importPublicClassesFromJar(handRolledJar);
        return;
      }

      final File potentialDir = new File(searchDir.getAbsoluteFile(), libName);
      if (potentialDir.exists()) {
        if (libDir == null) {
          libDir = potentialDir;
        } else {
          System.err.println("Multiple libraries could be " + libName + ";");
          System.err.println("Picking " + libDir + " over " + potentialDir);
        }
      }
    }

    if (libDir == null) {
      interp.exec("raise Exception('This sketch requires the \"" + libName + "\" library.')");
    }
    final File contentsDir = new File(libDir, "library");
    if (!contentsDir.exists()) {
      interp.exec("raise Exception('The library " + libName + " is malformed and won't import.')");
    }
    final File mainJar = new File(contentsDir, libName + ".jar");

    final List<File> resources = findResources(contentsDir);
    final PySystemState sys = Py.getSystemState();
    for (final File resource : resources) {
      final String name = resource.getName();
      if (name.endsWith(".jar") || name.endsWith(".zip")) {
        // Contains stuff we want
        addJarToClassLoader(resource.getAbsoluteFile());

        log("Appending " + resource.getAbsolutePath() + " to sys.path.");
        sys.path.append(Py.newString(resource.getAbsolutePath()));

        // Are we missing any extensions?
      } else if (name.matches("^.*\\.(so|dll|dylib|jnilib)$")) {
        // Add *containing directory* to native search path
        addDirectoryToNativeSearchPath(resource.getAbsoluteFile().getParentFile());
      }
    }

    if (mainJar.exists()) {
      importPublicClassesFromJar(mainJar);
    }
  }

  /**
   * Find all of the resources a library requires on this platform. See
   * https://github.com/processing/processing/wiki/Library-Basics.
   *
   * <p>First, finds the library. Second, tries to parse export.txt, and follow its instructions.
   * Third, tries to understand folder structure, and export according to that.
   *
   * @param libName The name of the library to add.
   * @return The list of files we need to import.
   */
  protected List<File> findResources(final File contentsDir) {
    log("Exploring " + contentsDir + " for resources.");
    List<File> resources;
    resources = findResourcesFromExportTxt(contentsDir);
    if (resources == null) {
      log("Falling back to directory structure.");
      resources = findResourcesFromDirectoryStructure(contentsDir);
    }
    return resources;
  }

  private List<File> findResourcesFromExportTxt(final File contentsDir) {
    final File exportTxt = new File(contentsDir, "export.txt");
    if (!exportTxt.exists()) {
      log("No export.txt in " + contentsDir.getAbsolutePath());
      return null;
    }
    final Map<String, String[]> exportTable;
    try {
      exportTable = parseExportTxt(exportTxt);
    } catch (final Exception e) {
      log("Couldn't parse export.txt: " + e.getMessage());
      return null;
    }

    final String[] resourceNames;

    // Check from most-specific to least-specific:
    if (exportTable.containsKey("application." + PLATFORM + BITS)) {
      log("Found 'application." + PLATFORM + BITS + "' in export.txt");
      resourceNames = exportTable.get("application." + PLATFORM + BITS);
    } else if (exportTable.containsKey("application." + PLATFORM)) {
      log("Found 'application." + PLATFORM + "' in export.txt");
      resourceNames = exportTable.get("application." + PLATFORM);
    } else if (exportTable.containsKey("application")) {
      log("Found 'application' in export.txt");
      resourceNames = exportTable.get("application");
    } else {
      log("No matching platform in " + exportTxt.getAbsolutePath());
      return null;
    }
    final List<File> resources = new ArrayList<>();
    for (final String resourceName : resourceNames) {
      final File resource = new File(contentsDir, resourceName);
      if (resource.exists()) {
        resources.add(resource);
      } else {
        log(
            resourceName
                + " is mentioned in "
                + exportTxt.getAbsolutePath()
                + "but doesn't actually exist. Moving on.");
        continue;
      }
    }
    return resources;
  }

  private File findPlatformDir(final File contentsDir) {
    final List<String> childNames = Arrays.asList(contentsDir.list());
    final String variant =
        (PLATFORM.equals("linux") && System.getProperty("os.arch").equals("arm"))
            ? "-armv6hf"
            : BITS;
    for (final String dirName : new String[] {PLATFORM + variant, PLATFORM}) {
      final File potentialPlatformDir = new File(contentsDir, dirName);
      if (potentialPlatformDir.isDirectory()) {
        return potentialPlatformDir;
      }
    }
    return null;
  }

  private List<File> findResourcesFromDirectoryStructure(final File contentsDir) {
    final List<File> resources = new ArrayList<File>();

    // Find platform-specific stuff
    final File platformDir = findPlatformDir(contentsDir);
    if (platformDir != null) {
      log("Found platform-specific directory " + platformDir.getAbsolutePath());
      for (final File resource : platformDir.listFiles()) {
        resources.add(resource);
      }
    }

    // Find multi-platform stuff; always do this
    final File[] commonResources =
        contentsDir.listFiles(
            new FileFilter() {
              @Override
              public boolean accept(final File file) {
                return !file.isDirectory();
              }
            });
    for (final File resource : commonResources) {
      resources.add(resource);
    }
    return resources;
  }

  /**
   * Parse an export.txt file to figure out what we need to load for this platform. This is all
   * duplicated from processing.app.Library / processing.app.Base, but we don't have the PDE around
   * at runtime so we can't use them.
   *
   * @param exportTxt The export.txt file; must exist.
   */
  private Map<String, String[]> parseExportTxt(final File exportTxt) throws Exception {
    log("Parsing " + exportTxt.getAbsolutePath());

    final Properties exportProps = new Properties();
    try (final FileReader in = new FileReader(exportTxt)) {
      exportProps.load(in);
    }

    final Map<String, String[]> exportTable = new HashMap<>();

    for (final String platform : exportProps.stringPropertyNames()) {
      final String exportCSV = exportProps.getProperty(platform);
      final String[] exports = PApplet.splitTokens(exportCSV, ",");
      for (int i = 0; i < exports.length; i++) {
        exports[i] = exports[i].trim();
      }
      exportTable.put(platform, exports);
    }
    return exportTable;
  }

  /**
   * Use a brittle and egregious hack to forcibly add the given jar file to the system classloader.
   *
   * @param jar The jar to add to the system classloader.
   */
  private void addJarToClassLoader(final File jar) {
    try {
      final URL url = jar.toURI().toURL();
      final URLClassLoader ucl = (URLClassLoader) ClassLoader.getSystemClassLoader();
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
    } catch (NoSuchMethodException
        | SecurityException
        | IllegalAccessException
        | IllegalArgumentException
        | InvocationTargetException
        | MalformedURLException e) {
      throw new RuntimeException(e);
    }
  }

  /**
   * Add the given path to the list of paths searched for DLLs (as in those loaded by loadLibrary).
   * A hack, which depends on the presence of a particular field in ClassLoader. Known to work on
   * all recent Sun JVMs and OS X.
   *
   * <p>See <a href="http://forums.sun.com/thread.jspa?threadID=707176">this thread</a>.
   */
  private void addDirectoryToNativeSearchPath(final File dllDir) {
    final String newPath = dllDir.getAbsolutePath();
    try {
      final Field field = ClassLoader.class.getDeclaredField("usr_paths");
      field.setAccessible(true);
      final String[] paths = (String[]) field.get(null);
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
      System.err.println(
          "While attempting to add "
              + newPath
              + " to the processing.py library search path: "
              + e.getClass().getSimpleName()
              + "--"
              + e.getMessage());
    }
  }

  private static final Pattern validPythonIdentifier = Pattern.compile("[a-zA-Z_][a-zA-Z0-9_]*");

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
  private void importPublicClassesFromJar(final File jarPath) {
    log("Importing public classes from " + jarPath.getAbsolutePath());
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

        if (!validPythonIdentifier.matcher(className).matches()) {
          log("Rejecting " + name);
          continue;
        }

        final String importStatement = String.format("from %s import %s", packageName, className);
        log(importStatement);
        interp.exec(importStatement);
      }
    } catch (final IOException e) {
      throw new RuntimeException(e);
    }
  }
}
