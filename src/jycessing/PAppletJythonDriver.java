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

		initializeStatics(locals);

		locals.__setitem__("size", new PyObject() {
			public PyObject __call__(final PyObject a, final PyObject b, final PyObject c) {
				size(a.asInt(), b.asInt(), c.asString());
				return Py.None;
			}
		});
		locals.__setitem__("fill", new PyObject() {
			public PyObject __call__(final PyObject arg) {
				final PyType t = arg.getType();
				if (t == PyInteger.TYPE) {
					fill(arg.asInt());
				} else if (t == PyFloat.TYPE) {
					fill((float)arg.asDouble());
				}
				return Py.None;
			}

			public PyObject __call__(final PyObject x, final PyObject y, final PyObject z) {
				fill((float)x.asDouble(), (float)y.asDouble(), (float)z.asDouble());
				return Py.None;
			}

			public PyObject __call__(final PyObject x, final PyObject y, final PyObject z,
					final PyObject a) {
				fill((float)x.asDouble(), (float)y.asDouble(), (float)z.asDouble(), (float)a
						.asDouble());
				return Py.None;
			}

			public PyObject __call__(final PyObject a, final PyObject b) {
				final PyType t = a.getType();
				if (t == PyInteger.TYPE) {
					fill(a.asInt(), (float)b.asDouble());
				} else if (t == PyFloat.TYPE) {
					fill((float)a.asDouble(), (float)b.asDouble());
				}
				return Py.None;
			}

		});
		locals.__setitem__("background", new PyObject() {
			public PyObject __call__(final PyObject arg) {
				final PyType t = arg.getType();
				if (t == PyInteger.TYPE) {
					background(arg.asInt());
				} else if (t == PyFloat.TYPE) {
					background((float)arg.asDouble());
				} else if (t == PyJavaType.TYPE) {
					background((PImage)arg.__tojava__(PImage.class));
				}
				return Py.None;
			}

			public PyObject __call__(final PyObject x, final PyObject y, final PyObject z) {
				background((float)x.asDouble(), (float)y.asDouble(), (float)z.asDouble());
				return Py.None;
			}

			public PyObject __call__(final PyObject x, final PyObject y, final PyObject z,
					final PyObject a) {
				background((float)x.asDouble(), (float)y.asDouble(), (float)z.asDouble(),
						(float)a.asDouble());
				return Py.None;
			}

			public PyObject __call__(final PyObject a, final PyObject b) {
				final PyType t = a.getType();
				if (t == PyInteger.TYPE) {
					background(a.asInt(), (float)b.asDouble());
				} else if (t == PyFloat.TYPE) {
					background((float)a.asDouble(), (float)b.asDouble());
				}
				return Py.None;
			}
		});

		locals.__setitem__("translate", new PyObject() {
			public PyObject __call__(final PyObject x, final PyObject y, final PyObject z) {
				translate((float)x.asDouble(), (float)y.asDouble(), (float)z.asDouble());
				return Py.None;
			}
		});

		locals.__setitem__("rotateY", new PyObject() {
			public PyObject __call__(final PyObject angle) {
				rotateY((float)angle.asDouble());
				return Py.None;
			}
		});

		locals.__setitem__("sin", new PyObject() {
			public PyObject __call__(final PyObject angle) {
				return new PyFloat(sin((float)angle.asDouble()));
			}
		});

		locals.__setitem__("millis", new PyObject() {
			public PyObject __call__() {
				return new PyInteger(millis());
			}
		});
		locals.__setitem__("frameRate", new PyObject() {
			@Override
			public PyFloat __float__() {
				return new PyFloat(frameRate);
			}

			public PyObject __call__(final PyObject newRateTarget) {
				frameRate((float)newRateTarget.asDouble());
				return Py.None;
			}

			@Override
			public PyObject __int__() {
				return new PyInteger((int)frameRate);
			}
		});

		locals.__setitem__("pushMatrix", new PyObject() {
			public PyObject __call__() {
				pushMatrix();
				return Py.None;
			}
		});

		locals.__setitem__("popMatrix", new PyObject() {
			public PyObject __call__() {
				popMatrix();
				return Py.None;
			}
		});

		locals.__setitem__("scale", new PyObject() {
			public PyObject __call__(final PyObject s) {
				scale((float)s.asDouble());
				return Py.None;
			}

			public PyObject __call__(final PyObject sx, final PyObject sy) {
				scale((float)sx.asDouble(), (float)sy.asDouble());
				return Py.None;
			}

			public PyObject __call__(final PyObject x, final PyObject y, final PyObject z) {
				scale((float)x.asDouble(), (float)y.asDouble(), (float)z.asDouble());
				return Py.None;
			}
		});
		locals.__setitem__("text", new PyObject() {
			public PyObject __call__(final PyObject a, final PyObject b, final PyObject c) {
				text(a.asString(), (float)b.asDouble(), (float)c.asDouble());
				return Py.None;
			}
		});
		locals.__setitem__("textWidth", new PyObject() {
			public PyObject __call__(final PyObject string) {
				return new PyFloat(textWidth(string.asString()));
			}
		});
		locals.__setitem__("textFont", new PyObject() {
			public PyObject __call__(final PyObject which) {
				textFont((PFont)which.__tojava__(PFont.class));
				return Py.None;
			}

			public PyObject __call__(final PyObject which, final PyObject size) {
				textFont((PFont)which.__tojava__(PFont.class), (float)size.asDouble());
				return Py.None;
			}
		});
		locals.__setitem__("loadFont", new PyObject() {
			public PyObject __call__(final PyObject filename) {
				return Py.java2py(loadFont(filename.asString()));
			}
		});
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
