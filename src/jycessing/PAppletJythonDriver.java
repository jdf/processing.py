package jycessing;

import java.lang.reflect.Field;
import java.lang.reflect.Modifier;

import org.python.core.Py;
import org.python.core.PyException;
import org.python.core.PyObject;
import org.python.core.PyStringMap;
import org.python.util.PythonInterpreter;

import processing.core.PApplet;
import processing.core.PConstants;

@SuppressWarnings("serial")
abstract public class PAppletJythonDriver extends PApplet {

	abstract protected void populateBuiltins();

	abstract protected void setNonPrimitives();

	private static final PyObject NODRAW = new PyObject();
	protected final PyStringMap builtins;
	protected final PythonInterpreter interp;
	PyObject draw;

	public PAppletJythonDriver(final PythonInterpreter interp) {
		interp.getSystemState();
		this.builtins = (PyStringMap)interp.getSystemState().getBuiltins();
		this.interp = interp;
		initializeStatics(builtins);
		populateBuiltins();
	}

	public static void initializeStatics(final PyStringMap builtins) {
		for (final Field f : PConstants.class.getDeclaredFields()) {
			final int mods = f.getModifiers();
			if (Modifier.isPublic(mods) || Modifier.isStatic(mods)) {
				try {
					builtins.__setitem__(f.getName(), Py.java2py(f.get(null)));
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		}
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
			setNonPrimitives();
			super.draw();
		} else {
			draw.__call__();
		}
	}
}
