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

import java.awt.Window;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileFilter;
import java.io.FileReader;
import java.io.FilenameFilter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.Properties;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import javax.swing.SwingUtilities;

import org.python.core.Py;
import org.python.core.PyString;
import org.python.util.InteractiveConsole;
import org.python.util.PythonInterpreter;

import processing.core.PApplet;

public class Runner {
    static boolean VERBOSE = false;

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

    private static String read(final InputStream in) throws IOException {
        return read(new InputStreamReader(in, "UTF-8"));
    }

    /**
     * Add a URL (referring to a jar file or class directory) to the current
     * classloader. Of course, this is a filthy hack, which depends on an
     * implementation detail (i.e., that the system classloader is a
     * URLClassLoader). But it certainly works with all known Sun JVMs of recent
     * vintage, and with OS X's JVMs.
     *
     * <p>
     * See <a href=
     * "http://robertmaldon.blogspot.com/2007/11/dynamically-add-to-eclipse-junit.html"
     * >this blog post</a>.
     *
     */
    private static void addJar(final URL url) throws Exception {
        final URLClassLoader classLoader = (URLClassLoader)ClassLoader
                .getSystemClassLoader();
        for (final URL u : classLoader.getURLs()) {
            if (u.equals(url)) {
                return;
            }
        }
        final Method method = URLClassLoader.class.getDeclaredMethod("addURL",
                URL.class);
        method.setAccessible(true);
        method.invoke(classLoader, new Object[] { url });
        if (VERBOSE) {
            System.err.println("Added " + url + " to classpath.");
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
    private static void addLibraryPath(final String newPath) throws Exception {
        final Field field = ClassLoader.class.getDeclaredField("usr_paths");
        field.setAccessible(true);
        final String[] paths = (String[])field.get(null);
        for (final String path : paths) {
            if (newPath.equals(path)) {
                return;
            }
        }
        final String[] tmp = new String[paths.length + 1];
        System.arraycopy(paths, 0, tmp, 0, paths.length);
        tmp[paths.length] = newPath;
        field.set(null, tmp);
        if (VERBOSE) {
            System.err.println("Added " + newPath + " to java.library.path.");
        }
    }

    /**
     * Recursively search the given directory for jar files and directories
     * containing dynamic libraries, adding them to the classpath and the
     * library path respectively.
     */
    private static void searchForExtraStuff(final File dir) throws Exception {
        final File[] dlls = dir.listFiles(new FilenameFilter() {
            public boolean accept(final File dir, final String name) {
                return name.matches("^.+\\.(so|dll|jnilib)$");
            }
        });
        if (dlls != null && dlls.length > 0) {
            addLibraryPath(dir.getAbsolutePath());
        }
        final File[] jars = dir.listFiles(new FilenameFilter() {
            public boolean accept(final File dir, final String name) {
                return name.matches("^.+\\.jar$");
            }
        });
        for (final File jar : jars) {
            addJar(jar.toURI().toURL());
        }
        final File[] dirs = dir.listFiles(new FileFilter() {
            public boolean accept(final File f) {
                return f.isDirectory() && f.getName().charAt(0) != '.';
            }
        });
        for (final File d : dirs) {
            searchForExtraStuff(d);
        }
    }

    public static void main(final String[] args) throws Exception {
        if (args.length < 1) {
            System.err
                    .println("I need the path of your Python script as an argument.");
        }

        // -Dverbose=true for some logging
        VERBOSE = Boolean.getBoolean("verbose");

        final Properties buildnum = new Properties();
        buildnum.load(Runner.class
                .getResourceAsStream("buildnumber.properties"));
        if (VERBOSE) {
            System.err.println("processing.py build "
                    + buildnum.getProperty("buildnumber"));
        }

        // The last argument is the path to the Python sketch
        final String sketchPath = args[args.length - 1];

        // This will throw an exception and die if the given file is not there
        // or not readable.
        final String sketchSource = read(new FileReader(sketchPath));

        runSketch(args, sketchPath, sketchSource);
    }

    private static final Pattern JAR_RESOURCE = Pattern
            .compile("jar:file:(.+?)/processing-py.jar!/jycessing/buildnumber.properties");
    private static final Pattern FILE_RESOURCE = Pattern
            .compile("file:(.+?)/bin/jycessing/buildnumber.properties");

    private static File getLibrariesDir() {
        final String propsResource = Runner.class.getResource(
                "buildnumber.properties").toString();
        {
            final Matcher m = JAR_RESOURCE.matcher(propsResource);
            if (m.matches()) {
                if (VERBOSE) {
                    System.err.println("We're running from a JAR file.");
                }
                return new File(m.group(1), "libraries");
            }
        }
        {
            final Matcher m = FILE_RESOURCE.matcher(propsResource);
            if (m.matches()) {
                if (VERBOSE) {
                    System.err.println("We're running from class files.");
                }
                return new File(m.group(1), "libraries");
            }
        }
        System.err
                .println("WARNING: I can't figure out where my libraries directory is.");
        return new File("libraries");
    }

    public static void runSketch(final String[] args, final String sketchPath,
            final String sketchSource) throws Exception {
        // Recursively search the "libraries" directory for jar files and
        // directories containing dynamic libraries, adding them to the
        // classpath and the library path respectively.

        // jar:file:/opt/feinberg/processing.py/processing-py.jar
        // or
        // file:/opt/feinberg/processing.py/bin/jycessing/buildnumber.properties

        final File libraries = getLibrariesDir();
        searchForExtraStuff(libraries);

        // Where is the sketch located?
        final String sketchDir = new File(sketchPath).getCanonicalFile()
                .getParent();

        final Properties props = new Properties();
        props.setProperty("python.path", libraries.getAbsolutePath()
                + File.pathSeparator + sketchDir);
        PythonInterpreter.initialize(null, props, new String[] { "" });

        Py.initPython();
        final InteractiveConsole interp = new InteractiveConsole();

        // This hack seems to be necessary in order to redirect stdout for unit
        // tests
        interp.setOut(System.out);

        // Tell PApplet to make its home there, so that it can find the data
        // folder
        System.setProperty("user.dir", sketchDir);

        // Add it to the Python library path for auxilliary modules
        Py.getSystemState().path.insert(0, new PyString(sketchDir));

        // For error messages
        interp.getLocals().__setitem__("__file__", new PyString(sketchPath));

        interp.exec(read(Runner.class.getResourceAsStream("core.py")));
        // Bind the sketch to a PApplet
        final PAppletJythonDriver applet = new DriverImpl(interp, sketchPath,
                sketchSource);

        try {
            PApplet.runSketch(args, applet);
            applet.blockUntilFinished();
            if (VERBOSE) {
                System.err.println("Applet is finished. Disposing window.");
            }
            ((Window)SwingUtilities.getRoot(applet)).dispose();
        } catch (final Throwable t) {
            Py.printException(t);
        } finally {
            if (VERBOSE) {
                System.err.println("Cleaning up interpreter.");
            }
            interp.cleanup();
        }

    }
}
