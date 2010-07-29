package jycessing;

import org.python.core.Py;
import org.python.core.PyBoolean;
import org.python.core.PyException;
import org.python.core.PyFloat;
import org.python.core.PyInteger;
import org.python.core.PyObject;
import org.python.core.PyString;
import org.python.core.PyStringMap;
import org.python.core.PyType;

import processing.core.PApplet;
import processing.core.PFont;
import processing.core.PImage;
import processing.core.PMatrix;
import processing.core.PMatrix2D;
import processing.core.PMatrix3D;

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
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"background\" with " + args.length
							+ " parameters.");
				case 1:
					if (args[0].getType() == PyFloat.TYPE) {
						background((float)args[0].asDouble());
						return Py.None;

					} else if (args[0].getType().getProxyType() != null
							&& args[0].getType().getProxyType() == PImage.class) {
						background((processing.core.PImage)args[0]
								.__tojava__(processing.core.PImage.class));
						return Py.None;
					} else if (args[0].getType() == PyInteger.TYPE) {
						background(args[0].asInt());
						return Py.None;

					} else {
						throw new IllegalArgumentException(
								"Couldn't figure out which \"background\" to call.");
					}
				case 2:
					if (args[0].getType() == PyFloat.TYPE && args[1].getType() == PyFloat.TYPE) {
						background((float)args[0].asDouble(), (float)args[1].asDouble());
						return Py.None;

					} else if (args[0].getType() == PyInteger.TYPE
							&& args[1].getType() == PyFloat.TYPE) {
						background(args[0].asInt(), (float)args[1].asDouble());
						return Py.None;

					} else {
						throw new IllegalArgumentException(
								"Couldn't figure out which \"background\" to call.");
					}
				case 3:
					background((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble());
					return Py.None;
				case 4:
					background((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble(), (float)args[3].asDouble());
					return Py.None;
				}
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

		locals.__setitem__("frameCount", new PyObject() {
			@Override
			public PyObject __int__() {
				return new PyInteger(frameCount);
			}

			@Override
			public PyString __repr__() {
				return new PyString(String.valueOf(frameCount));
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

			@Override
			public PyString __repr__() {
				return new PyString(String.valueOf(frameRate));
			}
		});

		locals.__setitem__("pushMatrix", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kw) {
				pushMatrix();
				return Py.None;
			}
		});

		locals.__setitem__("popMatrix", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kw) {
				popMatrix();
				return Py.None;
			}
		});

		locals.__setitem__("scale", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"scale\" with " + args.length
							+ " parameters.");
				case 1:
					scale((float)args[0].asDouble());
					return Py.None;
				case 2:
					scale((float)args[0].asDouble(), (float)args[1].asDouble());
					return Py.None;
				case 3:
					scale((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble());
					return Py.None;
				}
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
				System.err.println("loadFont type: " + filename.getType().getProxyType());
				return Py.java2py(loadFont(filename.asString()));
			}
		});
		locals.__setitem__("getMatrix", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kw) {
				return Py.java2py(getMatrix());
			}
		});
		locals.__setitem__("applyMatrix", new PyObject() {
			public PyObject __call__(final PyObject m) {
				applyMatrix((PMatrix)m.__tojava__(PMatrix.class));
				return Py.None;
			}
		});

		locals.__setitem__("bezierVertex", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"bezierVertex\" with " + args.length
							+ " parameters.");
				case 6:
					bezierVertex((float)args[0].asDouble(), (float)args[1].asDouble(),
							(float)args[2].asDouble(), (float)args[3].asDouble(), (float)args[4]
									.asDouble(), (float)args[5].asDouble());
					return Py.None;
				case 9:
					bezierVertex((float)args[0].asDouble(), (float)args[1].asDouble(),
							(float)args[2].asDouble(), (float)args[3].asDouble(), (float)args[4]
									.asDouble(), (float)args[5].asDouble(), (float)args[6].asDouble(),
							(float)args[7].asDouble(), (float)args[8].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("curve", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"curve\" with " + args.length
							+ " parameters.");
				case 8:
					curve((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble(), (float)args[3].asDouble(), (float)args[4].asDouble(),
							(float)args[5].asDouble(), (float)args[6].asDouble(), (float)args[7]
									.asDouble());
					return Py.None;
				case 12:
					curve((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble(), (float)args[3].asDouble(), (float)args[4].asDouble(),
							(float)args[5].asDouble(), (float)args[6].asDouble(), (float)args[7]
									.asDouble(), (float)args[8].asDouble(), (float)args[9].asDouble(),
							(float)args[10].asDouble(), (float)args[11].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("rotate", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"rotate\" with " + args.length
							+ " parameters.");
				case 1:
					rotate((float)args[0].asDouble());
					return Py.None;
				case 4:
					rotate((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble(), (float)args[3].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("modelZ", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"modelZ\" with " + args.length
							+ " parameters.");
				case 3:
					return new PyFloat(modelZ((float)args[0].asDouble(), (float)args[1].asDouble(),
							(float)args[2].asDouble()));
				}
			}
		});

		locals.__setitem__("modelY", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"modelY\" with " + args.length
							+ " parameters.");
				case 3:
					return new PyFloat(modelY((float)args[0].asDouble(), (float)args[1].asDouble(),
							(float)args[2].asDouble()));
				}
			}
		});

		locals.__setitem__("imageMode", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"imageMode\" with " + args.length
							+ " parameters.");
				case 1:
					imageMode(args[0].asInt());
					return Py.None;
				}
			}
		});

		locals.__setitem__("stroke", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"stroke\" with " + args.length
							+ " parameters.");
				case 1:
					if (args[0].getType() == PyInteger.TYPE) {
						stroke(args[0].asInt());
						return Py.None;

					} else if (args[0].getType() == PyFloat.TYPE) {
						stroke((float)args[0].asDouble());
						return Py.None;

					} else {
						throw new IllegalArgumentException(
								"Couldn't figure out which \"stroke\" to call.");
					}
				case 2:
					if (args[0].getType() == PyFloat.TYPE && args[1].getType() == PyFloat.TYPE) {
						stroke((float)args[0].asDouble(), (float)args[1].asDouble());
						return Py.None;

					} else if (args[0].getType() == PyInteger.TYPE
							&& args[1].getType() == PyFloat.TYPE) {
						stroke(args[0].asInt(), (float)args[1].asDouble());
						return Py.None;

					} else {
						throw new IllegalArgumentException(
								"Couldn't figure out which \"stroke\" to call.");
					}
				case 3:
					stroke((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble());
					return Py.None;
				case 4:
					stroke((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble(), (float)args[3].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("noTint", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"noTint\" with " + args.length
							+ " parameters.");
				case 0:
					noTint();
					return Py.None;
				}
			}
		});

		locals.__setitem__("arc", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"arc\" with " + args.length
							+ " parameters.");
				case 6:
					arc((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble(), (float)args[3].asDouble(), (float)args[4].asDouble(),
							(float)args[5].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("modelX", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"modelX\" with " + args.length
							+ " parameters.");
				case 3:
					return new PyFloat(modelX((float)args[0].asDouble(), (float)args[1].asDouble(),
							(float)args[2].asDouble()));
				}
			}
		});

		locals.__setitem__("strokeCap", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"strokeCap\" with " + args.length
							+ " parameters.");
				case 1:
					strokeCap(args[0].asInt());
					return Py.None;
				}
			}
		});

		locals.__setitem__("textLeading", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"textLeading\" with " + args.length
							+ " parameters.");
				case 1:
					textLeading((float)args[0].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("texture", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"texture\" with " + args.length
							+ " parameters.");
				case 1:
					texture((processing.core.PImage)args[0]
							.__tojava__(processing.core.PImage.class));
					return Py.None;
				}
			}
		});

		locals.__setitem__("setMatrix", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"setMatrix\" with " + args.length
							+ " parameters.");
				case 1:
					if (args[0].getType().getProxyType() != null
							&& args[0].getType().getProxyType() == PMatrix2D.class) {
						setMatrix((processing.core.PMatrix2D)args[0]
								.__tojava__(processing.core.PMatrix2D.class));
						return Py.None;

					} else if (args[0].getType().getProxyType() != null
							&& args[0].getType().getProxyType() == PMatrix.class) {
						setMatrix((processing.core.PMatrix)args[0]
								.__tojava__(processing.core.PMatrix.class));
						return Py.None;

					} else if (args[0].getType().getProxyType() != null
							&& args[0].getType().getProxyType() == PMatrix3D.class) {
						setMatrix((processing.core.PMatrix3D)args[0]
								.__tojava__(processing.core.PMatrix3D.class));
						return Py.None;

					} else {
						throw new IllegalArgumentException(
								"Couldn't figure out which \"setMatrix\" to call.");
					}
				}
			}
		});

		locals.__setitem__("tint", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"tint\" with " + args.length
							+ " parameters.");
				case 1:
					if (args[0].getType() == PyInteger.TYPE) {
						tint(args[0].asInt());
						return Py.None;

					} else if (args[0].getType() == PyFloat.TYPE) {
						tint((float)args[0].asDouble());
						return Py.None;

					} else {
						throw new IllegalArgumentException(
								"Couldn't figure out which \"tint\" to call.");
					}
				case 2:
					if (args[0].getType() == PyFloat.TYPE && args[1].getType() == PyFloat.TYPE) {
						tint((float)args[0].asDouble(), (float)args[1].asDouble());
						return Py.None;

					} else if (args[0].getType() == PyInteger.TYPE
							&& args[1].getType() == PyFloat.TYPE) {
						tint(args[0].asInt(), (float)args[1].asDouble());
						return Py.None;

					} else {
						throw new IllegalArgumentException(
								"Couldn't figure out which \"tint\" to call.");
					}
				case 3:
					tint((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble());
					return Py.None;
				case 4:
					tint((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble(), (float)args[3].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("curveDetail", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"curveDetail\" with " + args.length
							+ " parameters.");
				case 1:
					curveDetail(args[0].asInt());
					return Py.None;
				}
			}
		});

		locals.__setitem__("popMatrix", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"popMatrix\" with " + args.length
							+ " parameters.");
				case 0:
					popMatrix();
					return Py.None;
				}
			}
		});

		locals.__setitem__("textDescent", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"textDescent\" with " + args.length
							+ " parameters.");
				case 0:
					return new PyFloat(textDescent());
				}
			}
		});

		locals.__setitem__("image", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"image\" with " + args.length
							+ " parameters.");
				case 3:
					image((processing.core.PImage)args[0].__tojava__(processing.core.PImage.class),
							(float)args[1].asDouble(), (float)args[2].asDouble());
					return Py.None;
				case 5:
					image((processing.core.PImage)args[0].__tojava__(processing.core.PImage.class),
							(float)args[1].asDouble(), (float)args[2].asDouble(), (float)args[3]
									.asDouble(), (float)args[4].asDouble());
					return Py.None;
				case 9:
					image((processing.core.PImage)args[0].__tojava__(processing.core.PImage.class),
							(float)args[1].asDouble(), (float)args[2].asDouble(), (float)args[3]
									.asDouble(), (float)args[4].asDouble(), args[5].asInt(), args[6]
									.asInt(), args[7].asInt(), args[8].asInt());
					return Py.None;
				}
			}
		});

		locals.__setitem__("endCamera", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"endCamera\" with " + args.length
							+ " parameters.");
				case 0:
					endCamera();
					return Py.None;
				}
			}
		});

		locals.__setitem__("vertex", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"vertex\" with " + args.length
							+ " parameters.");
				case 1:
					vertex((float[])args[0].__tojava__(float[].class));
					return Py.None;
				case 2:
					vertex((float)args[0].asDouble(), (float)args[1].asDouble());
					return Py.None;
				case 3:
					vertex((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble());
					return Py.None;
				case 4:
					vertex((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble(), (float)args[3].asDouble());
					return Py.None;
				case 5:
					vertex((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble(), (float)args[3].asDouble(), (float)args[4].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("lerpColor", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"lerpColor\" with " + args.length
							+ " parameters.");
				case 3:
					return new PyInteger(lerpColor(args[0].asInt(), args[1].asInt(), (float)args[2]
							.asDouble()));
				case 4:
					return new PyInteger(lerpColor(args[0].asInt(), args[1].asInt(), (float)args[2]
							.asDouble(), args[3].asInt()));
				}
			}
		});

		locals.__setitem__("smooth", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"smooth\" with " + args.length
							+ " parameters.");
				case 0:
					smooth();
					return Py.None;
				}
			}
		});

		locals.__setitem__("resetMatrix", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"resetMatrix\" with " + args.length
							+ " parameters.");
				case 0:
					resetMatrix();
					return Py.None;
				}
			}
		});

		locals.__setitem__("beginRaw", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"beginRaw\" with " + args.length
							+ " parameters.");
				case 1:
					beginRaw((processing.core.PGraphics)args[0]
							.__tojava__(processing.core.PGraphics.class));
					return Py.None;
				}
			}
		});

		locals.__setitem__("sphere", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"sphere\" with " + args.length
							+ " parameters.");
				case 1:
					sphere((float)args[0].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("line", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"line\" with " + args.length
							+ " parameters.");
				case 4:
					line((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble(), (float)args[3].asDouble());
					return Py.None;
				case 6:
					line((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble(), (float)args[3].asDouble(), (float)args[4].asDouble(),
							(float)args[5].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("directionalLight", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"directionalLight\" with "
							+ args.length + " parameters.");
				case 6:
					directionalLight((float)args[0].asDouble(), (float)args[1].asDouble(),
							(float)args[2].asDouble(), (float)args[3].asDouble(), (float)args[4]
									.asDouble(), (float)args[5].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("printCamera", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"printCamera\" with " + args.length
							+ " parameters.");
				case 0:
					printCamera();
					return Py.None;
				}
			}
		});

		locals.__setitem__("colorMode", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"colorMode\" with " + args.length
							+ " parameters.");
				case 1:
					colorMode(args[0].asInt());
					return Py.None;
				case 2:
					colorMode(args[0].asInt(), (float)args[1].asDouble());
					return Py.None;
				case 4:
					colorMode(args[0].asInt(), (float)args[1].asDouble(),
							(float)args[2].asDouble(), (float)args[3].asDouble());
					return Py.None;
				case 5:
					colorMode(args[0].asInt(), (float)args[1].asDouble(),
							(float)args[2].asDouble(), (float)args[3].asDouble(), (float)args[4]
									.asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("edge", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"edge\" with " + args.length
							+ " parameters.");
				case 1:
					edge(args[0].__nonzero__());
					return Py.None;
				}
			}
		});

		locals.__setitem__("green", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"green\" with " + args.length
							+ " parameters.");
				case 1:
					return new PyFloat(green(args[0].asInt()));
				}
			}
		});

		locals.__setitem__("beginShape", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"beginShape\" with " + args.length
							+ " parameters.");
				case 0:
					beginShape();
					return Py.None;
				case 1:
					beginShape(args[0].asInt());
					return Py.None;
				}
			}
		});

		locals.__setitem__("popStyle", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"popStyle\" with " + args.length
							+ " parameters.");
				case 0:
					popStyle();
					return Py.None;
				}
			}
		});

		locals.__setitem__("skewX", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"skewX\" with " + args.length
							+ " parameters.");
				case 1:
					skewX((float)args[0].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("pointLight", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"pointLight\" with " + args.length
							+ " parameters.");
				case 6:
					pointLight((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble(), (float)args[3].asDouble(), (float)args[4].asDouble(),
							(float)args[5].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("textWidth", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"textWidth\" with " + args.length
							+ " parameters.");
				case 1:
					if (args[0].getType() == PyString.TYPE) {
						return new PyFloat(textWidth(args[0].asString().charAt(0)));
					} else if (args[0].getType() == PyString.TYPE) {
						return new PyFloat(textWidth(args[0].asString()));
					} else {
						throw new IllegalArgumentException(
								"Couldn't figure out which \"textWidth\" to call.");
					}
				case 3:
					return new PyFloat(textWidth((char[])args[0].__tojava__(char[].class), args[1]
							.asInt(), args[2].asInt()));
				}
			}
		});

		locals.__setitem__("skewY", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"skewY\" with " + args.length
							+ " parameters.");
				case 1:
					skewY((float)args[0].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("emissive", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"emissive\" with " + args.length
							+ " parameters.");
				case 1:
					if (args[0].getType() == PyFloat.TYPE) {
						emissive((float)args[0].asDouble());
						return Py.None;

					} else if (args[0].getType() == PyInteger.TYPE) {
						emissive(args[0].asInt());
						return Py.None;

					} else {
						throw new IllegalArgumentException(
								"Couldn't figure out which \"emissive\" to call.");
					}
				case 3:
					emissive((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("point", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"point\" with " + args.length
							+ " parameters.");
				case 2:
					point((float)args[0].asDouble(), (float)args[1].asDouble());
					return Py.None;
				case 3:
					point((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("rectMode", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"rectMode\" with " + args.length
							+ " parameters.");
				case 1:
					rectMode(args[0].asInt());
					return Py.None;
				}
			}
		});

		locals.__setitem__("curvePoint", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"curvePoint\" with " + args.length
							+ " parameters.");
				case 5:
					return new PyFloat(curvePoint((float)args[0].asDouble(), (float)args[1]
							.asDouble(), (float)args[2].asDouble(), (float)args[3].asDouble(),
							(float)args[4].asDouble()));
				}
			}
		});

		locals.__setitem__("red", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"red\" with " + args.length
							+ " parameters.");
				case 1:
					return new PyFloat(red(args[0].asInt()));
				}
			}
		});

		locals.__setitem__("sphereDetail", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"sphereDetail\" with " + args.length
							+ " parameters.");
				case 1:
					sphereDetail(args[0].asInt());
					return Py.None;
				case 2:
					sphereDetail(args[0].asInt(), args[1].asInt());
					return Py.None;
				}
			}
		});

		locals.__setitem__("quad", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"quad\" with " + args.length
							+ " parameters.");
				case 8:
					quad((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble(), (float)args[3].asDouble(), (float)args[4].asDouble(),
							(float)args[5].asDouble(), (float)args[6].asDouble(), (float)args[7]
									.asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("triangle", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"triangle\" with " + args.length
							+ " parameters.");
				case 6:
					triangle((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble(), (float)args[3].asDouble(), (float)args[4].asDouble(),
							(float)args[5].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("saturation", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"saturation\" with " + args.length
							+ " parameters.");
				case 1:
					return new PyFloat(saturation(args[0].asInt()));
				}
			}
		});

		locals.__setitem__("background", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"background\" with " + args.length
							+ " parameters.");
				case 1:
					if (args[0].getType() == PyFloat.TYPE) {
						background((float)args[0].asDouble());
						return Py.None;

					} else if (args[0].getType().getProxyType() != null
							&& args[0].getType().getProxyType() == PImage.class) {
						background((processing.core.PImage)args[0]
								.__tojava__(processing.core.PImage.class));
						return Py.None;

					} else if (args[0].getType() == PyInteger.TYPE) {
						background(args[0].asInt());
						return Py.None;

					} else {
						throw new IllegalArgumentException(
								"Couldn't figure out which \"background\" to call.");
					}
				case 2:
					if (args[0].getType() == PyFloat.TYPE && args[1].getType() == PyFloat.TYPE) {
						background((float)args[0].asDouble(), (float)args[1].asDouble());
						return Py.None;

					} else if (args[0].getType() == PyInteger.TYPE
							&& args[1].getType() == PyFloat.TYPE) {
						background(args[0].asInt(), (float)args[1].asDouble());
						return Py.None;

					} else {
						throw new IllegalArgumentException(
								"Couldn't figure out which \"background\" to call.");
					}
				case 3:
					background((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble());
					return Py.None;
				case 4:
					background((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble(), (float)args[3].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("noFill", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"noFill\" with " + args.length
							+ " parameters.");
				case 0:
					noFill();
					return Py.None;
				}
			}
		});

		locals.__setitem__("getMatrix", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"getMatrix\" with " + args.length
							+ " parameters.");
				case 0:
					return Py.java2py(getMatrix());
				case 1:
					if (args[0].getType().getProxyType() != null
							&& args[0].getType().getProxyType() == PMatrix3D.class) {
						return Py.java2py(getMatrix((processing.core.PMatrix3D)args[0]
								.__tojava__(processing.core.PMatrix3D.class)));
					} else if (args[0].getType().getProxyType() != null
							&& args[0].getType().getProxyType() == PMatrix2D.class) {
						return Py.java2py(getMatrix((processing.core.PMatrix2D)args[0]
								.__tojava__(processing.core.PMatrix2D.class)));
					} else {
						throw new IllegalArgumentException(
								"Couldn't figure out which \"getMatrix\" to call.");
					}
				}
			}
		});

		locals.__setitem__("textAscent", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"textAscent\" with " + args.length
							+ " parameters.");
				case 0:
					return new PyFloat(textAscent());
				}
			}
		});

		locals.__setitem__("translate", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"translate\" with " + args.length
							+ " parameters.");
				case 2:
					translate((float)args[0].asDouble(), (float)args[1].asDouble());
					return Py.None;
				case 3:
					translate((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("bezierTangent", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"bezierTangent\" with " + args.length
							+ " parameters.");
				case 5:
					return new PyFloat(bezierTangent((float)args[0].asDouble(), (float)args[1]
							.asDouble(), (float)args[2].asDouble(), (float)args[3].asDouble(),
							(float)args[4].asDouble()));
				}
			}
		});

		locals.__setitem__("ambientLight", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"ambientLight\" with " + args.length
							+ " parameters.");
				case 3:
					ambientLight((float)args[0].asDouble(), (float)args[1].asDouble(),
							(float)args[2].asDouble());
					return Py.None;
				case 6:
					ambientLight((float)args[0].asDouble(), (float)args[1].asDouble(),
							(float)args[2].asDouble(), (float)args[3].asDouble(), (float)args[4]
									.asDouble(), (float)args[5].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("noSmooth", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"noSmooth\" with " + args.length
							+ " parameters.");
				case 0:
					noSmooth();
					return Py.None;
				}
			}
		});

		locals.__setitem__("spotLight", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"spotLight\" with " + args.length
							+ " parameters.");
				case 11:
					spotLight((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble(), (float)args[3].asDouble(), (float)args[4].asDouble(),
							(float)args[5].asDouble(), (float)args[6].asDouble(), (float)args[7]
									.asDouble(), (float)args[8].asDouble(), (float)args[9].asDouble(),
							(float)args[10].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("hue", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"hue\" with " + args.length
							+ " parameters.");
				case 1:
					return new PyFloat(hue(args[0].asInt()));
				}
			}
		});

		locals.__setitem__("normal", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"normal\" with " + args.length
							+ " parameters.");
				case 3:
					normal((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("textMode", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"textMode\" with " + args.length
							+ " parameters.");
				case 1:
					textMode(args[0].asInt());
					return Py.None;
				}
			}
		});

		locals.__setitem__("rotateX", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"rotateX\" with " + args.length
							+ " parameters.");
				case 1:
					rotateX((float)args[0].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("strokeJoin", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"strokeJoin\" with " + args.length
							+ " parameters.");
				case 1:
					strokeJoin(args[0].asInt());
					return Py.None;
				}
			}
		});

		locals.__setitem__("rotateZ", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"rotateZ\" with " + args.length
							+ " parameters.");
				case 1:
					rotateZ((float)args[0].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("displayable", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"displayable\" with " + args.length
							+ " parameters.");
				case 0:
					return new PyBoolean(displayable());
				}
			}
		});

		locals.__setitem__("shininess", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"shininess\" with " + args.length
							+ " parameters.");
				case 1:
					shininess((float)args[0].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("rotateY", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"rotateY\" with " + args.length
							+ " parameters.");
				case 1:
					rotateY((float)args[0].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("ambient", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"ambient\" with " + args.length
							+ " parameters.");
				case 1:
					if (args[0].getType() == PyFloat.TYPE) {
						ambient((float)args[0].asDouble());
						return Py.None;

					} else if (args[0].getType() == PyInteger.TYPE) {
						ambient(args[0].asInt());
						return Py.None;

					} else {
						throw new IllegalArgumentException(
								"Couldn't figure out which \"ambient\" to call.");
					}
				case 3:
					ambient((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("frustum", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"frustum\" with " + args.length
							+ " parameters.");
				case 6:
					frustum((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble(), (float)args[3].asDouble(), (float)args[4].asDouble(),
							(float)args[5].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("perspective", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"perspective\" with " + args.length
							+ " parameters.");
				case 0:
					perspective();
					return Py.None;
				case 4:
					perspective((float)args[0].asDouble(), (float)args[1].asDouble(),
							(float)args[2].asDouble(), (float)args[3].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("curveTightness", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"curveTightness\" with " + args.length
							+ " parameters.");
				case 1:
					curveTightness((float)args[0].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("text", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"text\" with " + args.length
							+ " parameters.");
				case 1:
					if (args[0].getType() == PyString.TYPE) {
						text(args[0].asString());
						return Py.None;

					} else if (args[0].getType() == PyString.TYPE) {
						text(args[0].asString().charAt(0));
						return Py.None;

					} else {
						throw new IllegalArgumentException(
								"Couldn't figure out which \"text\" to call.");
					}
				case 3:
					if (args[0].getType() == PyString.TYPE && args[1].getType() == PyFloat.TYPE
							&& args[2].getType() == PyFloat.TYPE) {
						text(args[0].asString().charAt(0), (float)args[1].asDouble(), (float)args[2]
								.asDouble());
						return Py.None;

					} else if (args[0].getType() == PyFloat.TYPE
							&& args[1].getType() == PyFloat.TYPE && args[2].getType() == PyFloat.TYPE) {
						text((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
								.asDouble());
						return Py.None;

					} else if (args[0].getType() == PyInteger.TYPE
							&& args[1].getType() == PyFloat.TYPE && args[2].getType() == PyFloat.TYPE) {
						text(args[0].asInt(), (float)args[1].asDouble(), (float)args[2].asDouble());
						return Py.None;

					} else if (args[0].getType() == PyString.TYPE
							&& args[1].getType() == PyFloat.TYPE && args[2].getType() == PyFloat.TYPE) {
						text(args[0].asString(), (float)args[1].asDouble(), (float)args[2].asDouble());
						return Py.None;

					} else {
						for (PyObject arg : args) {
							System.err.println(arg.getType());
						}
						throw new IllegalArgumentException(
								"Couldn't figure out which \"text\" to call.");
					}
				case 4:
					if (args[0].getType() == PyString.TYPE && args[1].getType() == PyFloat.TYPE
							&& args[2].getType() == PyFloat.TYPE && args[3].getType() == PyFloat.TYPE) {
						text(args[0].asString().charAt(0), (float)args[1].asDouble(), (float)args[2]
								.asDouble(), (float)args[3].asDouble());
						return Py.None;

					} else if (args[0].getType() == PyInteger.TYPE
							&& args[1].getType() == PyFloat.TYPE && args[2].getType() == PyFloat.TYPE
							&& args[3].getType() == PyFloat.TYPE) {
						text(args[0].asInt(), (float)args[1].asDouble(), (float)args[2].asDouble(),
								(float)args[3].asDouble());
						return Py.None;

					} else if (args[0].getType() == PyString.TYPE
							&& args[1].getType() == PyFloat.TYPE && args[2].getType() == PyFloat.TYPE
							&& args[3].getType() == PyFloat.TYPE) {
						text(args[0].asString(), (float)args[1].asDouble(),
								(float)args[2].asDouble(), (float)args[3].asDouble());
						return Py.None;

					} else if (args[0].getType() == PyFloat.TYPE
							&& args[1].getType() == PyFloat.TYPE && args[2].getType() == PyFloat.TYPE
							&& args[3].getType() == PyFloat.TYPE) {
						text((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
								.asDouble(), (float)args[3].asDouble());
						return Py.None;

					} else {
						throw new IllegalArgumentException(
								"Couldn't figure out which \"text\" to call.");
					}
				case 5:
					if (args[0].getType().getProxyType() != null
							&& args[0].getType().getProxyType() == char[].class
							&& args[1].getType() == PyInteger.TYPE
							&& args[2].getType() == PyInteger.TYPE && args[3].getType() == PyFloat.TYPE
							&& args[4].getType() == PyFloat.TYPE) {
						text((char[])args[0].__tojava__(char[].class), args[1].asInt(), args[2]
								.asInt(), (float)args[3].asDouble(), (float)args[4].asDouble());
						return Py.None;

					} else if (args[0].getType() == PyString.TYPE
							&& args[1].getType() == PyFloat.TYPE && args[2].getType() == PyFloat.TYPE
							&& args[3].getType() == PyFloat.TYPE && args[4].getType() == PyFloat.TYPE) {
						text(args[0].asString(), (float)args[1].asDouble(),
								(float)args[2].asDouble(), (float)args[3].asDouble(), (float)args[4]
										.asDouble());
						return Py.None;

					} else {
						throw new IllegalArgumentException(
								"Couldn't figure out which \"text\" to call.");
					}
				case 6:
					if (args[0].getType() == PyString.TYPE && args[1].getType() == PyFloat.TYPE
							&& args[2].getType() == PyFloat.TYPE && args[3].getType() == PyFloat.TYPE
							&& args[4].getType() == PyFloat.TYPE && args[5].getType() == PyFloat.TYPE) {
						text(args[0].asString(), (float)args[1].asDouble(),
								(float)args[2].asDouble(), (float)args[3].asDouble(), (float)args[4]
										.asDouble(), (float)args[5].asDouble());
						return Py.None;

					} else if (args[0].getType().getProxyType() != null
							&& args[0].getType().getProxyType() == char[].class
							&& args[1].getType() == PyInteger.TYPE
							&& args[2].getType() == PyInteger.TYPE && args[3].getType() == PyFloat.TYPE
							&& args[4].getType() == PyFloat.TYPE && args[5].getType() == PyFloat.TYPE) {
						text((char[])args[0].__tojava__(char[].class), args[1].asInt(), args[2]
								.asInt(), (float)args[3].asDouble(), (float)args[4].asDouble(),
								(float)args[5].asDouble());
						return Py.None;

					} else {
						throw new IllegalArgumentException(
								"Couldn't figure out which \"text\" to call.");
					}
				}
			}
		});

		locals.__setitem__("ellipse", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"ellipse\" with " + args.length
							+ " parameters.");
				case 4:
					ellipse((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble(), (float)args[3].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("shape", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"shape\" with " + args.length
							+ " parameters.");
				case 1:
					shape((processing.core.PShape)args[0].__tojava__(processing.core.PShape.class));
					return Py.None;
				case 3:
					shape((processing.core.PShape)args[0].__tojava__(processing.core.PShape.class),
							(float)args[1].asDouble(), (float)args[2].asDouble());
					return Py.None;
				case 5:
					shape((processing.core.PShape)args[0].__tojava__(processing.core.PShape.class),
							(float)args[1].asDouble(), (float)args[2].asDouble(), (float)args[3]
									.asDouble(), (float)args[4].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("rect", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"rect\" with " + args.length
							+ " parameters.");
				case 4:
					rect((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble(), (float)args[3].asDouble());
					return Py.None;
				case 6:
					rect((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble(), (float)args[3].asDouble(), (float)args[4].asDouble(),
							(float)args[5].asDouble());
					return Py.None;
				case 8:
					rect((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble(), (float)args[3].asDouble(), (float)args[4].asDouble(),
							(float)args[5].asDouble(), (float)args[6].asDouble(), (float)args[7]
									.asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("specular", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"specular\" with " + args.length
							+ " parameters.");
				case 1:
					if (args[0].getType() == PyFloat.TYPE) {
						specular((float)args[0].asDouble());
						return Py.None;

					} else if (args[0].getType() == PyInteger.TYPE) {
						specular(args[0].asInt());
						return Py.None;

					} else {
						throw new IllegalArgumentException(
								"Couldn't figure out which \"specular\" to call.");
					}
				case 3:
					specular((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("shapeMode", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"shapeMode\" with " + args.length
							+ " parameters.");
				case 1:
					shapeMode(args[0].asInt());
					return Py.None;
				}
			}
		});

		locals.__setitem__("lightFalloff", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"lightFalloff\" with " + args.length
							+ " parameters.");
				case 3:
					lightFalloff((float)args[0].asDouble(), (float)args[1].asDouble(),
							(float)args[2].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("bezier", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"bezier\" with " + args.length
							+ " parameters.");
				case 8:
					bezier((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble(), (float)args[3].asDouble(), (float)args[4].asDouble(),
							(float)args[5].asDouble(), (float)args[6].asDouble(), (float)args[7]
									.asDouble());
					return Py.None;
				case 12:
					bezier((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble(), (float)args[3].asDouble(), (float)args[4].asDouble(),
							(float)args[5].asDouble(), (float)args[6].asDouble(), (float)args[7]
									.asDouble(), (float)args[8].asDouble(), (float)args[9].asDouble(),
							(float)args[10].asDouble(), (float)args[11].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("printProjection", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"printProjection\" with " + args.length
							+ " parameters.");
				case 0:
					printProjection();
					return Py.None;
				}
			}
		});

		locals.__setitem__("applyMatrix", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"applyMatrix\" with " + args.length
							+ " parameters.");
				case 1:
					if (args[0].getType().getProxyType() != null
							&& args[0].getType().getProxyType() == PMatrix.class) {
						applyMatrix((processing.core.PMatrix)args[0]
								.__tojava__(processing.core.PMatrix.class));
						return Py.None;

					} else if (args[0].getType().getProxyType() != null
							&& args[0].getType().getProxyType() == PMatrix3D.class) {
						applyMatrix((processing.core.PMatrix3D)args[0]
								.__tojava__(processing.core.PMatrix3D.class));
						return Py.None;

					} else if (args[0].getType().getProxyType() != null
							&& args[0].getType().getProxyType() == PMatrix2D.class) {
						applyMatrix((processing.core.PMatrix2D)args[0]
								.__tojava__(processing.core.PMatrix2D.class));
						return Py.None;

					} else {
						throw new IllegalArgumentException(
								"Couldn't figure out which \"applyMatrix\" to call.");
					}
				case 6:
					applyMatrix((float)args[0].asDouble(), (float)args[1].asDouble(),
							(float)args[2].asDouble(), (float)args[3].asDouble(), (float)args[4]
									.asDouble(), (float)args[5].asDouble());
					return Py.None;
				case 16:
					applyMatrix((float)args[0].asDouble(), (float)args[1].asDouble(),
							(float)args[2].asDouble(), (float)args[3].asDouble(), (float)args[4]
									.asDouble(), (float)args[5].asDouble(), (float)args[6].asDouble(),
							(float)args[7].asDouble(), (float)args[8].asDouble(), (float)args[9]
									.asDouble(), (float)args[10].asDouble(), (float)args[11].asDouble(),
							(float)args[12].asDouble(), (float)args[13].asDouble(), (float)args[14]
									.asDouble(), (float)args[15].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("breakShape", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"breakShape\" with " + args.length
							+ " parameters.");
				case 0:
					breakShape();
					return Py.None;
				}
			}
		});

		locals.__setitem__("endRaw", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"endRaw\" with " + args.length
							+ " parameters.");
				case 0:
					endRaw();
					return Py.None;
				}
			}
		});

		locals.__setitem__("noLights", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"noLights\" with " + args.length
							+ " parameters.");
				case 0:
					noLights();
					return Py.None;
				}
			}
		});

		locals.__setitem__("strokeWeight", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"strokeWeight\" with " + args.length
							+ " parameters.");
				case 1:
					strokeWeight((float)args[0].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("scale", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"scale\" with " + args.length
							+ " parameters.");
				case 1:
					scale((float)args[0].asDouble());
					return Py.None;
				case 2:
					scale((float)args[0].asDouble(), (float)args[1].asDouble());
					return Py.None;
				case 3:
					scale((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("ellipseMode", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"ellipseMode\" with " + args.length
							+ " parameters.");
				case 1:
					ellipseMode(args[0].asInt());
					return Py.None;
				}
			}
		});

		locals.__setitem__("beginCamera", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"beginCamera\" with " + args.length
							+ " parameters.");
				case 0:
					beginCamera();
					return Py.None;
				}
			}
		});

		locals.__setitem__("lightSpecular", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"lightSpecular\" with " + args.length
							+ " parameters.");
				case 3:
					lightSpecular((float)args[0].asDouble(), (float)args[1].asDouble(),
							(float)args[2].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("brightness", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"brightness\" with " + args.length
							+ " parameters.");
				case 1:
					return new PyFloat(brightness(args[0].asInt()));
				}
			}
		});

		locals.__setitem__("curveVertex", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"curveVertex\" with " + args.length
							+ " parameters.");
				case 2:
					curveVertex((float)args[0].asDouble(), (float)args[1].asDouble());
					return Py.None;
				case 3:
					curveVertex((float)args[0].asDouble(), (float)args[1].asDouble(),
							(float)args[2].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("lights", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"lights\" with " + args.length
							+ " parameters.");
				case 0:
					lights();
					return Py.None;
				}
			}
		});

		locals.__setitem__("style", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"style\" with " + args.length
							+ " parameters.");
				case 1:
					style((processing.core.PStyle)args[0].__tojava__(processing.core.PStyle.class));
					return Py.None;
				}
			}
		});

		locals.__setitem__("bezierDetail", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"bezierDetail\" with " + args.length
							+ " parameters.");
				case 1:
					bezierDetail(args[0].asInt());
					return Py.None;
				}
			}
		});

		locals.__setitem__("alpha", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"alpha\" with " + args.length
							+ " parameters.");
				case 1:
					return new PyFloat(alpha(args[0].asInt()));
				}
			}
		});

		locals.__setitem__("textAlign", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"textAlign\" with " + args.length
							+ " parameters.");
				case 1:
					textAlign(args[0].asInt());
					return Py.None;
				case 2:
					textAlign(args[0].asInt(), args[1].asInt());
					return Py.None;
				}
			}
		});

		locals.__setitem__("screenY", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"screenY\" with " + args.length
							+ " parameters.");
				case 2:
					return new PyFloat(
							screenY((float)args[0].asDouble(), (float)args[1].asDouble()));
				case 3:
					return new PyFloat(screenY((float)args[0].asDouble(),
							(float)args[1].asDouble(), (float)args[2].asDouble()));
				}
			}
		});

		locals.__setitem__("screenX", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"screenX\" with " + args.length
							+ " parameters.");
				case 2:
					return new PyFloat(
							screenX((float)args[0].asDouble(), (float)args[1].asDouble()));
				case 3:
					return new PyFloat(screenX((float)args[0].asDouble(),
							(float)args[1].asDouble(), (float)args[2].asDouble()));
				}
			}
		});

		locals.__setitem__("printMatrix", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"printMatrix\" with " + args.length
							+ " parameters.");
				case 0:
					printMatrix();
					return Py.None;
				}
			}
		});

		locals.__setitem__("screenZ", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"screenZ\" with " + args.length
							+ " parameters.");
				case 3:
					return new PyFloat(screenZ((float)args[0].asDouble(),
							(float)args[1].asDouble(), (float)args[2].asDouble()));
				}
			}
		});

		locals.__setitem__("ortho", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"ortho\" with " + args.length
							+ " parameters.");
				case 0:
					ortho();
					return Py.None;
				case 6:
					ortho((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble(), (float)args[3].asDouble(), (float)args[4].asDouble(),
							(float)args[5].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("setSize", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"setSize\" with " + args.length
							+ " parameters.");
				case 2:
					setSize(args[0].asInt(), args[1].asInt());
					return Py.None;
				}
			}
		});

		locals.__setitem__("endShape", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"endShape\" with " + args.length
							+ " parameters.");
				case 0:
					endShape();
					return Py.None;
				case 1:
					endShape(args[0].asInt());
					return Py.None;
				}
			}
		});

		locals.__setitem__("fill", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"fill\" with " + args.length
							+ " parameters.");
				case 1:
					if (args[0].getType() == PyInteger.TYPE) {
						fill(args[0].asInt());
						return Py.None;

					} else if (args[0].getType() == PyFloat.TYPE) {
						fill((float)args[0].asDouble());
						return Py.None;

					} else {
						throw new IllegalArgumentException(
								"Couldn't figure out which \"fill\" to call.");
					}
				case 2:
					if (args[0].getType() == PyFloat.TYPE && args[1].getType() == PyFloat.TYPE) {
						fill((float)args[0].asDouble(), (float)args[1].asDouble());
						return Py.None;

					} else if (args[0].getType() == PyInteger.TYPE
							&& args[1].getType() == PyFloat.TYPE) {
						fill(args[0].asInt(), (float)args[1].asDouble());
						return Py.None;

					} else {
						throw new IllegalArgumentException(
								"Couldn't figure out which \"fill\" to call.");
					}
				case 3:
					fill((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble());
					return Py.None;
				case 4:
					fill((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble(), (float)args[3].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("camera", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"camera\" with " + args.length
							+ " parameters.");
				case 0:
					camera();
					return Py.None;
				case 9:
					camera((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble(), (float)args[3].asDouble(), (float)args[4].asDouble(),
							(float)args[5].asDouble(), (float)args[6].asDouble(), (float)args[7]
									.asDouble(), (float)args[8].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("textFont", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"textFont\" with " + args.length
							+ " parameters.");
				case 1:
					textFont((processing.core.PFont)args[0].__tojava__(processing.core.PFont.class));
					return Py.None;
				case 2:
					textFont(
							(processing.core.PFont)args[0].__tojava__(processing.core.PFont.class),
							(float)args[1].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("pushStyle", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"pushStyle\" with " + args.length
							+ " parameters.");
				case 0:
					pushStyle();
					return Py.None;
				}
			}
		});

		locals.__setitem__("hint", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"hint\" with " + args.length
							+ " parameters.");
				case 1:
					hint(args[0].asInt());
					return Py.None;
				}
			}
		});

		locals.__setitem__("pushMatrix", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"pushMatrix\" with " + args.length
							+ " parameters.");
				case 0:
					pushMatrix();
					return Py.None;
				}
			}
		});

		locals.__setitem__("textureMode", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"textureMode\" with " + args.length
							+ " parameters.");
				case 1:
					textureMode(args[0].asInt());
					return Py.None;
				}
			}
		});

		locals.__setitem__("textSize", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"textSize\" with " + args.length
							+ " parameters.");
				case 1:
					textSize((float)args[0].asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("flush", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"flush\" with " + args.length
							+ " parameters.");
				case 0:
					flush();
					return Py.None;
				}
			}
		});

		locals.__setitem__("color", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"color\" with " + args.length
							+ " parameters.");
				case 1:
					if (args[0].getType() == PyInteger.TYPE) {
						return new PyInteger(color(args[0].asInt()));
					} else if (args[0].getType() == PyFloat.TYPE) {
						return new PyInteger(color((float)args[0].asDouble()));
					} else {
						throw new IllegalArgumentException(
								"Couldn't figure out which \"color\" to call.");
					}
				case 2:
					if (args[0].getType() == PyFloat.TYPE && args[1].getType() == PyFloat.TYPE) {
						return new PyInteger(color((float)args[0].asDouble(), (float)args[1]
								.asDouble()));
					} else if (args[0].getType() == PyInteger.TYPE
							&& args[1].getType() == PyFloat.TYPE) {
						return new PyInteger(color(args[0].asInt(), (float)args[1].asDouble()));
					} else if (args[0].getType() == PyInteger.TYPE
							&& args[1].getType() == PyInteger.TYPE) {
						return new PyInteger(color(args[0].asInt(), args[1].asInt()));
					} else {
						throw new IllegalArgumentException(
								"Couldn't figure out which \"color\" to call.");
					}
				case 3:
					if (args[0].getType() == PyFloat.TYPE && args[1].getType() == PyFloat.TYPE
							&& args[2].getType() == PyFloat.TYPE) {
						return new PyInteger(color((float)args[0].asDouble(), (float)args[1]
								.asDouble(), (float)args[2].asDouble()));
					} else if (args[0].getType() == PyInteger.TYPE
							&& args[1].getType() == PyInteger.TYPE
							&& args[2].getType() == PyInteger.TYPE) {
						return new PyInteger(color(args[0].asInt(), args[1].asInt(), args[2].asInt()));
					} else {
						throw new IllegalArgumentException(
								"Couldn't figure out which \"color\" to call.");
					}
				case 4:
					if (args[0].getType() == PyInteger.TYPE && args[1].getType() == PyInteger.TYPE
							&& args[2].getType() == PyInteger.TYPE
							&& args[3].getType() == PyInteger.TYPE) {
						return new PyInteger(color(args[0].asInt(), args[1].asInt(), args[2].asInt(),
								args[3].asInt()));
					} else if (args[0].getType() == PyFloat.TYPE
							&& args[1].getType() == PyFloat.TYPE && args[2].getType() == PyFloat.TYPE
							&& args[3].getType() == PyFloat.TYPE) {
						return new PyInteger(color((float)args[0].asDouble(), (float)args[1]
								.asDouble(), (float)args[2].asDouble(), (float)args[3].asDouble()));
					} else {
						throw new IllegalArgumentException(
								"Couldn't figure out which \"color\" to call.");
					}
				}
			}
		});

		locals.__setitem__("blue", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"blue\" with " + args.length
							+ " parameters.");
				case 1:
					return new PyFloat(blue(args[0].asInt()));
				}
			}
		});

		locals.__setitem__("noStroke", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"noStroke\" with " + args.length
							+ " parameters.");
				case 0:
					noStroke();
					return Py.None;
				}
			}
		});

		locals.__setitem__("bezierPoint", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"bezierPoint\" with " + args.length
							+ " parameters.");
				case 5:
					return new PyFloat(bezierPoint((float)args[0].asDouble(), (float)args[1]
							.asDouble(), (float)args[2].asDouble(), (float)args[3].asDouble(),
							(float)args[4].asDouble()));
				}
			}
		});

		locals.__setitem__("box", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"box\" with " + args.length
							+ " parameters.");
				case 1:
					box((float)args[0].asDouble());
					return Py.None;
				case 3:
					box((float)args[0].asDouble(), (float)args[1].asDouble(), (float)args[2]
							.asDouble());
					return Py.None;
				}
			}
		});

		locals.__setitem__("curveTangent", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"curveTangent\" with " + args.length
							+ " parameters.");
				case 5:
					return new PyFloat(curveTangent((float)args[0].asDouble(), (float)args[1]
							.asDouble(), (float)args[2].asDouble(), (float)args[3].asDouble(),
							(float)args[4].asDouble()));
				}
			}
		});

		locals.__setitem__("bezierVertex", new PyObject() {
			public PyObject __call__(final PyObject[] args, final String[] kws) {
				switch (args.length) {
				default:
					throw new RuntimeException("Can't call \"bezierVertex\" with " + args.length
							+ " parameters.");
				case 6:
					bezierVertex((float)args[0].asDouble(), (float)args[1].asDouble(),
							(float)args[2].asDouble(), (float)args[3].asDouble(), (float)args[4]
									.asDouble(), (float)args[5].asDouble());
					return Py.None;
				case 9:
					bezierVertex((float)args[0].asDouble(), (float)args[1].asDouble(),
							(float)args[2].asDouble(), (float)args[3].asDouble(), (float)args[4]
									.asDouble(), (float)args[5].asDouble(), (float)args[6].asDouble(),
							(float)args[7].asDouble(), (float)args[8].asDouble());
					return Py.None;
				}
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
