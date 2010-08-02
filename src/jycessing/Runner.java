package jycessing;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.Reader;

import org.python.core.Py;
import org.python.core.PyString;
import org.python.util.InteractiveConsole;

import processing.core.PApplet;

public class Runner {
	private static String wrap(final Reader r) throws IOException {
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

	public static void main(final String[] args) throws Exception {
		final String pathname = args[0];
		final String text = wrap(new FileReader(pathname));

		Py.initPython();
		final InteractiveConsole interp = new InteractiveConsole();
		final String path = new File(pathname).getCanonicalFile().getParent();
		Py.getSystemState().path.insert(0, new PyString(path));
		try {
			interp.getLocals().__setitem__(new PyString("__file__"), new PyString(pathname));
			final DriverImpl applet = new DriverImpl(interp);
			interp.exec(text);
			applet.findAppletMethods();
			PApplet.runSketch(new String[] { "Test" }, applet);
		} catch (Throwable t) {
			Py.printException(t);
			interp.cleanup();
			System.exit(-1);
		}
	}
}
