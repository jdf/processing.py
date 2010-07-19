package jycessing;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.Reader;

import org.python.core.Py;
import org.python.core.PyException;
import org.python.core.PyObject;
import org.python.core.PyString;
import org.python.core.PyStringMap;
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
			//			sb.append("Test().runSketch()");
			return sb.toString();
		} finally {
			reader.close();
		}
	}

	public static class PSM extends PyStringMap {
		@Override
		public PyObject __finditem__(final String key) {
			System.err.println("finditem: " + key);
			return super.__finditem__(key);
		}

	}

	public static void main(final String[] args) throws Exception {
		final String pathname = "kinetictype.py";
		final String text = wrap(new FileReader(pathname));

		final InteractiveConsole interp = new InteractiveConsole(new PSM());
		final PyStringMap locals = (PyStringMap)interp.getLocals();
		final String path = new File(pathname).getCanonicalFile().getParent();
		Py.getSystemState().path.insert(0, new PyString(path));
		try {
			locals.__setitem__(new PyString("__file__"), new PyString(pathname));
			interp.exec(text);
		} catch (Throwable t) {
			Py.printException(t);
			interp.cleanup();
			System.exit(-1);
		}

		final PyObject setup = locals.__finditem__("setup");
		final PyObject draw = locals.__finditem__("draw");
		final PApplet applet = new PApplet() {
			@Override
			public void setup() {
				if (setup != null) {
					try {
						setup.__call__();
					} catch (PyException e) {
						if (e.getCause() instanceof RendererChangeException) {
							throw (RendererChangeException)e.getCause();
						}
					}
				}
			}

			@Override
			public void draw() {
				if (draw == null) {
					super.draw();
				} else {
					draw.__call__();
				}
			}
		};
		locals.__setitem__("P3D", new PyString(PApplet.P3D));
		locals.__setitem__("size", new PyObject() {
			@Override
			public PyObject __call__(final PyObject arg0, final PyObject arg1,
					final PyObject arg2) {
				applet.size(arg0.asInt(), arg1.asInt(), arg2.asString());
				return Py.None;
			}
		});
		PApplet.runSketch(new String[] { "Test" }, applet);
	}
}
