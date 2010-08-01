package jycessing;

import org.python.core.PyException;
import org.python.core.PyFloat;
import org.python.core.PyObject;
import org.python.core.PyString;
import org.python.util.PythonInterpreter;

import processing.core.PApplet;

@SuppressWarnings("serial")
public class PAppletJythonDriver extends PApplet {

	private static final PyObject NODRAW = new PyObject();
	final PythonInterpreter interp;
	PyObject draw;

	public PAppletJythonDriver(final PythonInterpreter interp) {
		this.interp = interp;
		initializeStatics(interp);

	}

	public static void initializeStatics(final PythonInterpreter interp) {
		interp.set("P3D", new PyString(PApplet.P3D));
		interp.set("TWO_PI", new PyFloat(PApplet.TWO_PI));
	}

	@Override
	public void setup() {
		final PyObject setup = interp.get("setup");
		if (setup != null) {
			try {
				setup.__call__();
			} catch (PyException e) {
				if (e.getCause() instanceof RendererChangeException) {
					throw (RendererChangeException)e.getCause();
				} else {
					throw e;
				}
			}
		}
	}

	@Override
	public void draw() {
		if (draw == null) {
			draw = interp.get("draw");
			if (draw == null) {
				draw = NODRAW;
			}
		}
		if (draw == NODRAW) {
			super.draw();
		} else {
			draw.__call__();
		}
	}
}
