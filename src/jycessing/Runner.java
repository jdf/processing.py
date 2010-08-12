/*
 * Copyright 2010 Jonathan Feinberg
 * 
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License. You may obtain a copy of
 * the License at
 * 
 *     http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations under
 * the License.
 */
package jycessing;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileFilter;
import java.io.FileReader;
import java.io.FilenameFilter;
import java.io.IOException;
import java.io.Reader;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.net.URL;
import java.net.URLClassLoader;

import org.python.core.Py;
import org.python.core.PyString;
import org.python.util.InteractiveConsole;

import processing.core.PApplet;

public class Runner {
	static boolean VERBOSE = false;

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

	// See http://robertmaldon.blogspot.com/2007/11/dynamically-add-to-eclipse-junit.html
	private static void addJar(final URL url) throws Exception {
		final URLClassLoader classLoader = (URLClassLoader)ClassLoader.getSystemClassLoader();
		final Method method = URLClassLoader.class.getDeclaredMethod("addURL", URL.class);
		method.setAccessible(true);
		method.invoke(classLoader, new Object[] { url });
		if (VERBOSE) {
			System.err.println("Added " + url + " to classpath.");
		}
	}

	// See http://forums.sun.com/thread.jspa?threadID=707176
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
			System.err.println("I need the path of your Python script as an argument.");
		}
		if (Boolean.getBoolean("verbose")) {
			VERBOSE = true;
		}
		final String pathname = args[args.length - 1];
		final String text = read(new FileReader(pathname));
		searchForExtraStuff(new File("libraries"));
		Py.initPython();
		final InteractiveConsole interp = new InteractiveConsole();
		final String path = new File(pathname).getCanonicalFile().getParent();
                System.setProperty("user.dir", path);
		Py.getSystemState().path.insert(0, new PyString(path));
		try {
			interp.getLocals().__setitem__(new PyString("__file__"), new PyString(pathname));
			final PAppletJythonDriver applet = new DriverImpl(interp, text);
			PApplet.runSketch(args, applet);
		} catch (Throwable t) {
			Py.printException(t);
			interp.cleanup();
			System.exit(-1);
		}
	}
}
