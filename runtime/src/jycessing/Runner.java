/*
 * Copyright 2010 Jonathan Feinberg
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License. You may obtain a copy of
 * the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations under
 * the License.
 */
package jycessing;

import java.awt.SplashScreen;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileFilter;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FilenameFilter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.io.Reader;
import java.io.UnsupportedEncodingException;
import java.net.URISyntaxException;
import java.net.URLDecoder;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Properties;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import jycessing.annotations.PythonUsage;
import jycessing.launcher.LaunchHelper;
import jycessing.mode.RunMode;
import jycessing.mode.run.SketchInfo;

import org.python.core.Py;
import org.python.core.PyList;
import org.python.core.PyObject;
import org.python.core.PyStringMap;
import org.python.core.PySystemState;
import org.python.util.InteractiveConsole;
import org.python.util.PythonInterpreter;

import processing.core.PApplet;
import processing.core.PConstants;

public class Runner {

  private static final String BUILD_PROPERTIES = "build.properties";

  private static final String ARCH;
  static {
    final int archBits = Integer.parseInt(System.getProperty("sun.arch.data.model"));
    if (PApplet.platform == PConstants.MACOSX) {
      ARCH = "macosx" + archBits;
    } else if (PApplet.platform == PConstants.WINDOWS) {
      ARCH = "macosx" + archBits;
    } else if (PApplet.platform == PConstants.LINUX) {
      ARCH = "linux" + archBits;
    } else {
      ARCH = "unknown" + archBits;
    }
  }

  private static final String LAUNCHER_TEXT = readOrDie(LaunchHelper.class
      .getResourceAsStream("launcher.py"));
  private static final String CORE_TEXT = readOrDie(Runner.class.getResourceAsStream("core.py"));

  static boolean VERBOSE = false;

  static void log(final Object... objs) {
    if (!VERBOSE) {
      return;
    }
    for (final Object o : objs) {
      System.err.print(String.valueOf(o));
    }
    System.err.println();
  }

  // Slurp the given Reader into a String.
  private static String read(final Reader r) throws IOException {
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

  private static String readOrDie(final InputStream in) {
    try {
      return read(in);
    } catch (final IOException e) {
      throw new RuntimeException(e);
    }
  }

  private static String read(final InputStream in) throws IOException {
    return read(new InputStreamReader(in, "UTF-8"));
  }

  /**
   * Recursively search the given directory for jar files and directories
   * containing dynamic libraries, adding them to the classpath and the
   * library path respectively.
   */
  private static void searchForExtraStuff(final File dir, final Set<String> entries) {
    if (dir == null) {
      throw new IllegalArgumentException("null dir");
    }

    final String dirName = dir.getName();
    if (!dirName.equals(ARCH) && dirName.matches("^(macosx|windows|linux)(32|64)$")) {
      log("Ignoring wrong architecture " + dir);
      return;
    }

    log("Searching: ", dir);

    final File[] dlls = dir.listFiles(new FilenameFilter() {
      public boolean accept(final File dir, final String name) {
        return name.matches("^.+\\.(so|dll|jnilib|dylib)$");
      }
    });
    if (dlls != null && dlls.length > 0) {
      entries.add(dir.getAbsolutePath());
    } else {
      log("No DLLs in ", dir);
    }

    final File[] jars = dir.listFiles(new FilenameFilter() {
      public boolean accept(final File dir, final String name) {
        return name.matches("^.+\\.jar$");
      }
    });
    if (!(jars == null || jars.length == 0)) {
      for (final File jar : jars) {
        entries.add(jar.getAbsolutePath());
      }
    } else {
      log("No JARs in ", dir);
    }

    final File[] dirs = dir.listFiles(new FileFilter() {
      public boolean accept(final File f) {
        return f.isDirectory() && f.getName().charAt(0) != '.';
      }
    });
    if (!(dirs == null || dirs.length == 0)) {
      for (final File d : dirs) {
        searchForExtraStuff(d, entries);
      }
    } else {
      log("No dirs in ", dir);
    }
  }

  public static void main(final String[] args) throws Exception {
    runFromCommandLineArguments(args);
    System.exit(0);
  }

  /**
   * Returns the path of the main processing-py.jar file.
   * 
   * Used from launcher.py
   * 
   * @return the path of processing-py.jar.
   */
  @PythonUsage(methodName = "getMainJarFile")
  public static File getMainJarFile() {
    // On a Mac, when launched as an app, this will contain ".app/Contents/Java/processing-py.jar"
    try {
      return new File(Runner.class.getProtectionDomain().getCodeSource().getLocation().toURI());
    } catch (final URISyntaxException e) {
      e.printStackTrace();
    }
    return null;
  }

  /**
   * Returns the 'root' folder of this instance. Used when running with a
   * wrapper.
   * 
   * @return the distribution root directory.
   */
  public static File getRuntimeRoot() {
    final File jar = getMainJarFile();

    // If we are on a mac
    if (jar.getAbsolutePath().contains(".app/Contents/")) {
      return getMainJarFile().getParentFile().getParentFile();
    }

    // If we are on Windows
    return getMainJarFile().getParentFile();
  }

  /**
   * @param args
   * @throws IOException
   * @throws FileNotFoundException
   * @throws Exception
   */
  public static void runFromCommandLineArguments(final String[] args) throws Exception {

    // In case we have no args, throw Exception. Also, since we don't know which script
    // to run, we cannot redirect our input at this point.
    if (args.length < 1) {
      throw new RuntimeException("I need the path of your Python script as an argument.");
    }

    // The last argument is the path to the Python sketch
    String sketchPath = args[args.length - 1];

    // In case the sketch path points to "internal" we get it from the wrapper
    if (Arrays.asList(args).contains("--internal")) {
      sketchPath = new File(getRuntimeRoot(), "Runtime/sketch.py").getAbsolutePath();
    }

    // Debug when using launcher
    if (Arrays.asList(args).contains("--redirect")) {

      // Get sketch path, name, out and err names
      final File file = new File(sketchPath).getCanonicalFile();
      final String name = file.getName().replaceAll("\\.py", "");
      final String out = file.getParent() + "/" + name + ".out.txt";
      final String err = file.getParent() + "/" + name + ".err.txt";

      // Redirect actual input
      System.setOut(new PrintStream(new FileOutputStream(out)));
      System.setErr(new PrintStream(new FileOutputStream(err)));
    }

    // -Dverbose=true for some logging
    VERBOSE = Boolean.getBoolean("verbose");

    final Properties buildnum = new Properties();
    final InputStream buildnumberStream = Runner.class.getResourceAsStream(BUILD_PROPERTIES);
    try {
      buildnum.load(buildnumberStream);
    } finally {
      buildnumberStream.close();
    }
    log("processing.py build ", buildnum.getProperty("build.number"));

    // This will throw an exception and die if the given file is not there
    // or not readable.
    final String sketchSource = read(new FileReader(sketchPath));

    final SketchInfo info =
        new SketchInfo.Builder()
            .libraries(getLibraries())
            .libraryPolicy(LibraryPolicy.PROMISCUOUS)
            .runMode(
                Arrays.asList(args).contains("--present") ? RunMode.PRESENTATION : RunMode.WINDOWED)
            .sketch(new File(sketchPath)).code(sketchSource).build();
    // Hide the splash, if possible
    final SplashScreen splash = SplashScreen.getSplashScreen();
    if (splash != null) {
      splash.close();
    }
    runSketchBlocking(info);
  }

  private static final Pattern JAR_RESOURCE = Pattern
      .compile("jar:file:(.+?)/processing-py\\.jar!/jycessing/" + Pattern.quote(BUILD_PROPERTIES));
  private static final Pattern FILE_RESOURCE = Pattern.compile("file:(.+?)/bin/jycessing/"
      + Pattern.quote(BUILD_PROPERTIES));

  /**
   * Returns the library dir, when run as a command-line app.
   * 
   * Used from launcher.py
   * 
   * @return the processing.py libraries directory.
   */
  @PythonUsage(methodName = "getLibrariesDir")
  public static File getLibraries() {
    final String propsResource;
    try {
      propsResource =
          URLDecoder.decode(Runner.class.getResource(BUILD_PROPERTIES).toString(), "UTF-8");
    } catch (final UnsupportedEncodingException e) {
      throw new RuntimeException("Impossible: " + e);
    }

    {
      final Matcher m = JAR_RESOURCE.matcher(propsResource);
      if (m.matches()) {
        log("We're running from a JAR file.");
        return new File(m.group(1), "libraries");
      }
    }
    {
      final Matcher m = FILE_RESOURCE.matcher(propsResource);
      if (m.matches()) {
        log("We're running from class files.");
        return new File(m.group(1), "libraries");
      }
    }
    System.err.println("WARNING: I can't figure out where my libraries directory is.");
    return new File("libraries");
  }

  /**
   * Specifies how to deal with the libraries directory.
   */
  public enum LibraryPolicy {
    /**
     * Preemptively put every jar file and directory under the library path on sys.path.
     */
    PROMISCUOUS,

    /**
     * Only put jar files and directories onto sys.path as called for by add_library.
     */
    SELECTIVE
  }

  public static void runSketchBlocking(final SketchInfo info) throws PythonSketchError {
    final Properties props = new Properties();

    // Suppress sys-package-manager output.
    props.setProperty("python.verbose", "error");

    // Can be handy for class loading issues and the like.
    // props.setProperty("python.verbose", "debug");

    final StringBuilder pythonPath = new StringBuilder();
    if (info.libraries != null) {
      pythonPath.append(info.libraries.getAbsolutePath());
    }
    final String sketchDirPath = info.sketch.getParentFile().getAbsolutePath();
    pythonPath.append(File.pathSeparator).append(sketchDirPath);

    props.setProperty("python.path", pythonPath.toString());
    props.setProperty("python.main", info.sketch.getAbsolutePath());
    props.setProperty("python.main.root", sketchDirPath);

    final String[] args = info.runMode.args(info.sketch.getAbsolutePath(), info.x, info.y);
    PythonInterpreter.initialize(null, props, args);

    final PySystemState sys = Py.getSystemState();
    final PyStringMap originalModules = ((PyStringMap)sys.modules).copy();
    final PyList originalPath = new PyList((PyObject)sys.path);
    try {
      final InteractiveConsole interp = new InteractiveConsole();

      // This hack seems to be necessary in order to redirect stdout for unit
      // tests
      interp.setOut(System.out);

      // Add the sketch directory to the Python library path for auxilliary modules.
      sys.path.insert(0, Py.newString(sketchDirPath));

      // For moar useful error messages.
      interp.set("__file__", info.sketch.getAbsolutePath());

      interp.exec("import sys\n");

      // Add the add_library function to the sketch namespace.
      if (info.libraries != null) {
        final LibraryImporter libraryImporter = new LibraryImporter(info.libraries, interp);
        libraryImporter.initialize();

        if (info.libraryPolicy == LibraryPolicy.PROMISCUOUS) {
          log("Promiscusouly adding all libraries in " + info.libraries);
          // Recursively search the "libraries" directory for jar files and
          // directories containing dynamic libraries.
          final Set<String> libs = new HashSet<String>();
          searchForExtraStuff(info.libraries, libs);
          for (final String lib : libs) {
            interp.exec(String.format("sys.path.append(\"%s\")\n", lib));
          }
        }
      }

      interp.exec(LAUNCHER_TEXT);

      /*
       * Here's what core.py does:
       * Bring all of the core Processing classes into the python builtins namespace,
       * so they'll be available, without qualification, from all modules.
       * Construct a PAppletJythonDriver (which is a PApplet), then expose all of its
       * bound methods (such as loadImage(), noSmooth(), noise(), etc.) in the builtins
       * namespace.
       * 
       * We provide the Jython interpreter and sketch source code to the environment
       * so that core.py can construct the PAppletJythonDriver with all the stuff it
       * needs. 
       */
      interp.set("__interp__", interp);
      interp.set("__path__", info.sketch.getAbsolutePath());
      interp.set("__source__", info.code);
      interp.exec(CORE_TEXT);

      final PAppletJythonDriver applet =
          (PAppletJythonDriver)interp.get("__papplet__").__tojava__(PAppletJythonDriver.class);

      applet.findSketchMethods();

      // Tell the applet where to load and save data files, etc.
      final String[] massagedArgs = new String[args.length + 1];
      System.arraycopy(args, 0, massagedArgs, 0, args.length);
      massagedArgs[args.length] = PApplet.ARGS_SKETCH_FOLDER + "=" + sketchDirPath;

      final PreparedPythonSketch preparedPythonSketch =
          new PreparedPythonSketch(interp, applet, massagedArgs);
      preparedPythonSketch.runBlocking();
    } finally {
      sys.modules = originalModules;
      sys.path.clear();
      sys.path.addAll(originalPath);
    }
  }
}
