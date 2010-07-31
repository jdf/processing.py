package jycessing;

import org.python.core.PyException;
import org.python.core.PyFloat;
import org.python.core.PyObject;
import org.python.core.PyString;
import org.python.core.PyStringMap;

import processing.core.PApplet;

@SuppressWarnings("serial")
public class PAppletJythonDriver extends PApplet {

	final PyObject setup;
	final PyObject draw;

	public PAppletJythonDriver(final PyStringMap locals) {
		setup = locals.__finditem__("setup");
		draw = locals.__finditem__("draw");

		initializeStatics(locals);

	}

	public static void initializeStatics(final PyStringMap locals) {
		locals.__setitem__("P3D", new PyString(PApplet.P3D));
		locals.__setitem__("TWO_PI", new PyFloat(PApplet.TWO_PI));
	}

	@Override
	public void setup() {
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
			super.draw();
		} else {
			draw.__call__();
		}
	}

}
