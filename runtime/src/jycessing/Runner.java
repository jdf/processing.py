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
import java.io.File;
import java.io.FileFilter;
import java.io.FilenameFilter;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Properties;
import java.util.Set;

import jycessing.launcher.LaunchHelper;
import jycessing.launcher.StandaloneSketch;
import jycessing.mode.export.ExportedSketch;

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

  private static final String BUILD_NUMBER = loadBuildNumber();

  private static String loadBuildNumber() {
    final Properties buildProperties = new Properties();
    try (InputStream in = Runner.class.getResourceAsStream("build.properties")) {
      buildProperties.load(in);
      return buildProperties.getProperty("build.number", "????");
    } catch (final IOException e) {
      System.err.println("Can't read build.properties.");
      return "????";
    }
  }

  private static final String LAUNCHER_TEXT = IOUtil.readResourceAsText(LaunchHelper.class,
      "launcher.py");
  private static final String CORE_TEXT = IOUtil.readResourceAsText(Runner.class, "core.py");

  // -Dverbose=true for some logging
  static public boolean VERBOSE = Boolean.getBoolean("verbose");

  static void log(final Object... objs) {
    if (!VERBOSE) {
      return;
    }
    for (final Object o : objs) {
      System.err.print(String.valueOf(o));
    }
    System.err.println();
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
      @Override
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
      @Override
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
      @Override
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

  public static RunnableSketch sketch;

  /**
   * 
   * Entrypoint for non-PDE sketches. If we find ARGS_EXPORTED in the argument list,
   * Launch as an exported sketch.
   * Otherwise, launch as a standalone processing.py sketch.
   * 
   */
  public static void main(final String[] args) throws Exception {
    if (args.length < 1) {
      throw new RuntimeException("I need the path of your Python script as an argument.");
    }

    final Properties buildnum = new Properties();
    try (InputStream buildnumberStream = Runner.class.getResourceAsStream(BUILD_PROPERTIES)) {
      buildnum.load(buildnumberStream);
    }
    log("processing.py build ", buildnum.getProperty("build.number"));
    if (Arrays.asList(args).contains(ExportedSketch.ARGS_EXPORTED)) {
      sketch = new ExportedSketch(args);
    } else {
      sketch = new StandaloneSketch(args);
    }

    runSketchBlocking(sketch, new StreamPrinter(System.out), new StreamPrinter(System.err));

    System.exit(0);
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

  private static class WarmupSketch implements RunnableSketch {
    final File sketchFile;

    WarmupSketch() {
      File temp;
      try {
        temp = File.createTempFile("warmup", ".pyde");
      } catch (IOException e) {
        temp = null;
        // drop
      }
      this.sketchFile = temp;
    }

    @Override
    public File getMainFile() {
      return sketchFile;
    }

    @Override
    public String getMainCode() {
      return "print \"warming up!\"\nexit()";
    }

    @Override
    public File getHomeDirectory() {
      return sketchFile.getAbsoluteFile().getParentFile();
    }

    @Override
    public String[] getPAppletArguments() {
      return new String[] {"warmup.pyde"};
    }

    @Override
    public List<File> getLibraryDirectories() {
      return new ArrayList<>();
    }

    @Override
    public LibraryPolicy getLibraryPolicy() {
      return LibraryPolicy.PROMISCUOUS;
    }

    @Override
    public boolean shouldRun() {
      return false;
    }
  }

  /**
   * warmup() front-loads a huge amount of slow IO so that when the user gets around
   * to running a sketch, most of the slow work is already done. 
   */
  public static void warmup() {
    try {
      runSketchBlocking(new WarmupSketch(), new DevNullPrinter(), new DevNullPrinter());
    } catch (final PythonSketchError e) {
      // drop
    }
  }

  public synchronized static void runSketchBlocking(final RunnableSketch sketch,
      final Printer stdout, final Printer stderr) throws PythonSketchError {
    runSketchBlocking(sketch, stdout, stderr, null);
  }

  public synchronized static void runSketchBlocking(final RunnableSketch sketch,
      final Printer stdout, final Printer stderr,
      final SketchPositionListener sketchPositionListener) throws PythonSketchError {
    final Properties props = new Properties();

    // Suppress sys-package-manager output.
    props.setProperty("python.verbose", "error");

    // Can be handy for class loading issues and the like.
    // props.setProperty("python.verbose", "debug");

    final StringBuilder pythonPath = new StringBuilder();

    final List<File> libDirs = sketch.getLibraryDirectories();

    final String sketchDirPath = sketch.getHomeDirectory().getAbsolutePath();
    pythonPath.append(File.pathSeparator).append(sketchDirPath);

    props.setProperty("python.path", pythonPath.toString());
    props.setProperty("python.main", sketch.getMainFile().getAbsolutePath());
    props.setProperty("python.main.root", sketchDirPath);

    final String[] args = sketch.getPAppletArguments();
    PythonInterpreter.initialize(null, props, args);

    final PySystemState sys = Py.getSystemState();
    final PyStringMap originalModules = ((PyStringMap)sys.modules).copy();
    final PyList originalPath = new PyList((PyObject)sys.path);
    final PyStringMap builtins = (PyStringMap)sys.getBuiltins();
    final PyStringMap originalBuiltins = builtins.copy();
    try {
      final InteractiveConsole interp = new InteractiveConsole();

      // Add the sketch directory to the Python library path for auxilliary modules.
      sys.path.insert(0, Py.newString(sketchDirPath));

      // For moar useful error messages.
      interp.set("__file__", sketch.getMainFile().getAbsolutePath());

      interp.exec("import sys\n");

      // Add the add_library function to the sketch namespace.
      if (libDirs != null) {
        new LibraryImporter(sketch.getLibraryDirectories(), interp);

        if (sketch.getLibraryPolicy() == LibraryPolicy.PROMISCUOUS) {
          log("Promiscusouly adding all libraries in " + libDirs);
          // Recursively search the "libraries" directory for jar files and
          // directories containing dynamic libraries.
          final Set<String> libs = new HashSet<>();
          for (final File dir : libDirs) {
            searchForExtraStuff(dir, libs);
          }
          for (final String lib : libs) {
            sys.path.insert(0, Py.newString(lib));
          }
        }
      }

      // Make fake "launcher" module available to sketches - will only work with standalone sketches
      interp.exec(LAUNCHER_TEXT);

      /*
       * Here's what core.py does:
       * Bring all of the core Processing classes into the python builtins namespace,
       * so they'll be available, without qualification, from all modules.
       * Expose all of the PAppletJythonDriver's
       * bound methods (such as loadImage(), noSmooth(), noise(), etc.) in the builtins
       * namespace.
       */
      interp.set("__cwd__", sketch.getHomeDirectory().getAbsolutePath());
      interp.set("__python_mode_build__", BUILD_NUMBER);
      interp.set("__stdout__", stdout);
      interp.set("__stderr__", stderr);
      final PAppletJythonDriver applet =
          new PAppletJythonDriver(interp, sketch.getMainFile().toString(), sketch.getMainCode(),
              stdout);
      interp.set("__papplet__", applet);
      interp.exec(CORE_TEXT);

      // We have to do this because static mode sketches may load data
      // files during parsing!
      applet.sketchPath = sketch.getHomeDirectory().getAbsolutePath();

      applet.setSketchPositionListener(sketchPositionListener);

      applet.findSketchMethods();

      // Hide the splash before we run the sketch, if possible
      final SplashScreen splash = SplashScreen.getSplashScreen();
      if (splash != null) {
        splash.close();
      }

      try {
        if (sketch.shouldRun()) {
          applet.runAndBlock(args);
        }
      } finally {
        interp.cleanup();
      }
    } finally {
      sys.modules = originalModules;
      sys.path.clear();
      sys.path.addAll(originalPath);
      builtins.clear();
      for (final PyObject k : originalBuiltins.keys().asIterable()) {
        builtins.__setitem__(k, originalBuiltins.get(k));
      }
      resetCodecsModule();
    }
  }

  /**
   * The urllib module unit tests exposed a bug in how the codecs module
   * is mangled when the world is reset around it. This hack forces it to
   * reinitialize.
   */
  private static void resetCodecsModule() {
    ReflectionUtil.setObject(Py.getSystemState(), "codecState", null);
  }
}
