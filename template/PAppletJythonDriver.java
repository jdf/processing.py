package jycessing;

import org.python.core.Py;
import org.python.core.PyException;
import org.python.core.PyFloat;
import org.python.core.PyInteger;
import org.python.core.PyJavaType;
import org.python.core.PyObject;
import org.python.core.PyString;
import org.python.core.PyStringMap;
import org.python.core.PyType;

import processing.core.PApplet;
import processing.core.PFont;
import processing.core.PImage;

@SuppressWarnings("serial")
public class PAppletJythonDriver extends PApplet {

	final PyObject setup;
	final PyObject draw;

	public PAppletJythonDriver(final PyStringMap locals) {
		setup = locals.__finditem__("setup");
		draw = locals.__finditem__("draw");

		// BEGIN GENERATED CODE
		// END GENERATED CODE
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
