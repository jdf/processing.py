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
import java.awt.event.ComponentAdapter;
import java.awt.event.ComponentEvent;
import java.io.File;
import java.lang.Thread.UncaughtExceptionHandler;
import java.lang.reflect.Field;
import java.lang.reflect.Modifier;
import java.util.HashSet;
import java.util.concurrent.CountDownLatch;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import javax.swing.SwingUtilities;

import org.python.core.CompileMode;
import org.python.core.CompilerFlags;
import org.python.core.Py;
import org.python.core.PyBoolean;
import org.python.core.PyException;
import org.python.core.PyFloat;
import org.python.core.PyInteger;
import org.python.core.PyJavaType;
import org.python.core.PyObject;
import org.python.core.PySet;
import org.python.core.PyString;
import org.python.core.PyStringMap;
import org.python.core.PySyntaxError;
import org.python.core.PyTuple;
import org.python.core.PyType;
import org.python.core.PyUnicode;
import org.python.util.InteractiveConsole;

import processing.core.PApplet;
import processing.core.PConstants;
import processing.core.PImage;
import processing.opengl.PShader;

/**
 *
 * @author Jonathan Feinberg &lt;jdf@pobox.com&gt;
 *
 */
@SuppressWarnings("serial")
public class PAppletJythonDriver extends PApplet {

  private PythonSketchError terminalException = null;

  protected final PyStringMap builtins;
  protected final InteractiveConsole interp;
  private final String pySketchPath;
  private final String programText;

  private final CountDownLatch finishedLatch = new CountDownLatch(1);

  private enum Mode {
    STATIC, DRAW_LOOP
  }

  // A static-mode sketch must be interpreted from within the setup() method.
  // All others are interpreted during construction in order to harvest method
  // definitions, which we then invoke during the run loop.
  private final Mode mode;

  // The presence of either setup() or draw() indicates that this is not a
  // static sketch.
  private static final Pattern ACTIVE_METHOD_DEF = Pattern.compile(
      "^def\\s+(setup|draw)\\s*\\(\\s*\\)\\s*:", Pattern.MULTILINE);

  // These are all of the methods that PApplet might call in your sketch. If
  // you have implemented a method, we save it and call it.
  private PyObject setupMeth, drawMeth, mousePressedMeth, mouseClickedMeth, mouseMovedMeth,
      mouseReleasedMeth, mouseDraggedMeth, keyPressedMeth, keyReleasedMeth, keyTypedMeth, initMeth,
      stopMeth, sketchFullScreenMeth, sketchWidthMeth, sketchHeightMeth, sketchRendererMeth;

  // Adapted from Jython's PythonInterpreter.java exec(String s) to preserve
  // the source file name, so that errors have the file name instead of
  // "<string>"
  private void interpretSketch() throws PythonSketchError {
    try {
      Py.setSystemState(interp.getSystemState());
      Py.exec(Py.compile_flags(programText, pySketchPath, CompileMode.exec, new CompilerFlags()),
          interp.getLocals(), null);
      Py.flushLine();
    } catch (Throwable t) {
      checkForRendererChangeException(t);
      while (t.getCause() != null) {
        t = t.getCause();
      }
      throw toSketchException(t);
    }
  }

  private static PythonSketchError toSketchException(Throwable t) {
    if (t instanceof PythonSketchError) {
      return (PythonSketchError)t;
    }
    if (t instanceof PySyntaxError) {
      final PySyntaxError e = (PySyntaxError)t;
      final PyTuple tup = (PyTuple)e.value;
      final String message = (String)tup.get(0);
      final PyTuple context = (PyTuple)tup.get(1);
      final String file = (String)context.get(0);
      final int line = ((Integer)context.get(1)).intValue();
      final int column = ((Integer)context.get(2)).intValue();
      return new PythonSketchError(message, file, line, column);
    }
    if (t instanceof PyException) {
      final PyException e = (PyException)t;
      final Pattern tbParse =
          Pattern.compile("^\\s*File \"([^\"]+)\", line (\\d+)", Pattern.MULTILINE);
      final Matcher m = tbParse.matcher(e.toString());
      String file = null;
      int line = -1;
      while (m.find()) {
        file = m.group(1);
        line = Integer.parseInt(m.group(2)) - 1;
      }
      if (((PyType)e.type).getName().equals("ImportError")) {
        final Pattern importStar = Pattern.compile("import\\s+\\*");
        if (importStar.matcher(e.toString()).find()) {
          return new PythonSketchError("import * does not work in this environment.", file, line);
        }
      }
      return new PythonSketchError(e.value.asString(), file, line);
    }
    return new PythonSketchError(t.getMessage());
  }

  public PAppletJythonDriver(final InteractiveConsole interp, final String sketchPath,
                             final String programText) {
    this.programText = programText;
    this.pySketchPath = sketchPath;
    this.sketchPath = new File(sketchPath).getParent();
    this.mode = ACTIVE_METHOD_DEF.matcher(programText).find() ? Mode.DRAW_LOOP : Mode.STATIC;
    Runner.log("Mode: ", mode.name());
    this.builtins = (PyStringMap)interp.getSystemState().getBuiltins();
    this.interp = interp;
    initializeStatics(builtins);
    setFilter();
    setMap();
    setSet();
    builtins.__setitem__("g", Py.java2py(g));
    wrapProcessingVariables();

    addComponentListener(new ComponentAdapter() {
      @Override
      public void componentHidden(final ComponentEvent e) {
        finishedLatch.countDown();
      }
    });
  }

  @Override
  protected void exitActual() {
    finishedLatch.countDown();
  }

  public void findSketchMethods() throws PythonSketchError {
    if (mode == Mode.DRAW_LOOP) {
      // Executing the sketch will bind method names ("draw") to PyCode
      // objects (the sketch's draw method), which can then be invoked
      // during the run loop
      interpretSketch();
    }

    // Find and cache any PApplet callbacks defined in the Python sketch
    drawMeth = interp.get("draw");
    setupMeth = interp.get("setup");
    mousePressedMeth = interp.get("mousePressed");
    mouseClickedMeth = interp.get("mouseClicked");
    mouseMovedMeth = interp.get("mouseMoved");
    mouseReleasedMeth = interp.get("mouseReleased");
    mouseDraggedMeth = interp.get("mouseDragged");
    keyPressedMeth = interp.get("keyPressed");
    keyReleasedMeth = interp.get("keyReleased");
    keyTypedMeth = interp.get("keyTyped");
    sketchFullScreenMeth = interp.get("sketchFullScreen");
    sketchWidthMeth = interp.get("sketchWidth");
    sketchHeightMeth = interp.get("sketchHeight");
    sketchRendererMeth = interp.get("sketchRenderer");
    initMeth = interp.get("init");
    stopMeth = interp.get("stop");
  }

  protected void wrapProcessingVariables() {
    builtins.__setitem__("mouseX", new PyInteger(-1) {
      @Override
      public int getValue() {
        return mouseX;
      }
    });
    builtins.__setitem__("width", new PyInteger(-1) {
      @Override
      public int getValue() {
        return width;
      }
    });
    builtins.__setitem__("height", new PyInteger(-1) {
      @Override
      public int getValue() {
        return height;
      }
    });
    builtins.__setitem__("pmouseY", new PyInteger(-1) {
      @Override
      public int getValue() {
        return pmouseY;
      }
    });
    builtins.__setitem__("paused", new PyBoolean(false) {
      @Override
      public boolean getBooleanValue() {
        return paused;
      }
    });
    builtins.__setitem__("focused", new PyBoolean(false) {
      @Override
      public boolean getBooleanValue() {
        return focused;
      }
    });
    builtins.__setitem__("displayHeight", new PyInteger(-1) {
      @Override
      public int getValue() {
        return displayHeight;
      }
    });
    builtins.__setitem__("keyPressed", new PyBoolean(false) {
      @Override
      public boolean getBooleanValue() {
        return keyPressed;
      }
    });
    builtins.__setitem__("mousePressed", new PyBoolean(false) {
      @Override
      public boolean getBooleanValue() {
        return mousePressed;
      }
    });
    builtins.__setitem__("frameCount", new PyInteger(-1) {
      @Override
      public int getValue() {
        return frameCount;
      }
    });
    builtins.__setitem__("mouseButton", new PyInteger(-1) {
      @Override
      public int getValue() {
        return mouseButton;
      }
    });
    builtins.__setitem__("pmouseX", new PyInteger(-1) {
      @Override
      public int getValue() {
        return pmouseX;
      }
    });
    builtins.__setitem__("keyCode", new PyInteger(-1) {
      @Override
      public int getValue() {
        return keyCode;
      }
    });
    builtins.__setitem__("frameRate", new PyFloat(-1) {
      @Override
      public double getValue() {
        return frameRate;
      }

      @Override
      public PyObject __call__(final PyObject[] args, final String[] kws) {
        switch (args.length) {
          default:
            throw new RuntimeException("Can't call \"frameRate\" with " + args.length
                + " parameters.");
          case 1: {
            frameRate((float)args[0].asDouble());
            return Py.None;
          }
        }
      }
    });
    builtins.__setitem__("displayWidth", new PyInteger(-1) {
      @Override
      public int getValue() {
        return displayWidth;
      }
    });
    builtins.__setitem__("mouseY", new PyInteger(-1) {
      @Override
      public int getValue() {
        return mouseY;
      }
    });
    /*
     * If key is "CODED", i.e., an arrow key or other non-printable, pass that
     * value through as-is. If it's printable, convert it to a unicode string,
     * so that the user can compare key == 'x' instead of key == ord('x').
     */
    builtins.__setitem__("key", new PyObject() {
      private char lastKey = (char)-1;
      private PyObject cachedProxy = null;

      private PyObject getProxy() {
        if (key != lastKey || cachedProxy == null) {
          cachedProxy = key == CODED ? new PyInteger(key) : new PyUnicode(Character.toString(key));
          lastKey = key;
        }
        return cachedProxy;
      }

      @Override
      public PyObject __eq__(PyObject other) {
        return getProxy().__eq__(other);
      }

      @Override
      public PyString __str__() {
        return getProxy().__str__();
      }

      @Override
      public PyUnicode __unicode__() {
        return getProxy().__unicode__();
      }
    });
  }

  @Override
  public void start() {
    // I want to quit on runtime exceptions.
    // Processing just sits there by default.
    Thread.setDefaultUncaughtExceptionHandler(new UncaughtExceptionHandler() {
      public void uncaughtException(Thread t, Throwable e) {
        terminalException = toSketchException(e);
        finishedLatch.countDown();
      }
    });
    super.start();
  }

  @Override
  public void init() {
    try {
      if (initMeth != null) {
        builtins.__setitem__("frame", Py.java2py(frame));
        initMeth.__call__();
      }
    } finally {
      super.init();
    }
  }

  public void runAndBlock(final String[] args) throws PythonSketchError {
    PApplet.runSketch(args, this);
    try {
      finishedLatch.await();
    } catch (InterruptedException interrupted) {
      // Treat an interruption as a request to the applet to terminate.
      exit();
      try {
        finishedLatch.await();
      } catch (InterruptedException e) {
        // fallthrough
      }
    } finally {
      ((Window)SwingUtilities.getRoot(this)).dispose();
    }
    if (terminalException != null) {
      throw terminalException;
    }
  }

  /**
   * Permit the punning use of set() by mucking with the builtin "set" Type.
   * If you call it with 3 arguments, it acts like the Processing set(x, y,
   * whatever) method. If you call it with 0 or 1 args, it constructs a Python
   * set.
   */
  private void setSet() {
    builtins.__setitem__("set", new PyType(PyType.TYPE) {
      {
        builtin = true;
        init(PySet.class, new HashSet<PyJavaType>());
        invalidateMethodCache();
      }

      @Override
      public PyObject __call__(final PyObject[] args, final String[] kws) {
        switch (args.length) {
          default:
            return super.__call__(args, kws);
          case 3: {
            final PyObject x = args[0];
            final PyType tx = x.getType();
            final PyObject y = args[1];
            final PyType ty = y.getType();
            final PyObject c = args[2];
            final PyType tc = c.getType();
            if (tx == PyInteger.TYPE && ty == PyInteger.TYPE && tc == PyInteger.TYPE) {
              set(x.asInt(), y.asInt(), c.asInt());
              return Py.None;
            } else if (tx == PyInteger.TYPE && ty == PyInteger.TYPE && tc.getProxyType() != null
                && tc.getProxyType() == PImage.class) {
              set(x.asInt(), y.asInt(),
                  (processing.core.PImage)c.__tojava__(processing.core.PImage.class));
              return Py.None;
            } else {
              return super.__call__(args, kws);
            }
          }
        }
      }
    });
  }

  /**
   * Permit both the Processing map() (which is a linear interpolation function) and
   * the Python map() (which is a list transformation).
   */
  private void setMap() {
    final PyObject builtinMap = builtins.__getitem__("map");
    builtins.__setitem__("map", new PyObject() {

      @Override
      public PyObject __call__(final PyObject[] args, final String[] kws) {
        switch (args.length) {
          default:
            return builtinMap.__call__(args, kws);
          case 5: {
            final PyObject value = args[0];
            final PyObject start1 = args[1];
            final PyObject stop1 = args[2];
            final PyObject start2 = args[3];
            final PyObject stop2 = args[4];
            if (value.isNumberType() && start1.isNumberType() && stop1.isNumberType()
                && start2.isNumberType() && stop2.isNumberType()) {
              return Py.newFloat(map((float)value.asDouble(), (float)start1.asDouble(),
                  (float)stop1.asDouble(), (float)start2.asDouble(), (float)stop2.asDouble()));
            } else {
              return builtinMap.__call__(args, kws);
            }
          }
        }
      }
    });
  }

  /**
   * Permit both the Processing filter() (which does image processing) and the
   * Python filter() (which does list comprehensions).
   */
  private void setFilter() {
    final PyObject builtinFilter = builtins.__getitem__("filter");
    builtins.__setitem__("filter", new PyObject() {
      @Override
      public PyObject __call__(final PyObject[] args, final String[] kws) {
        switch (args.length) {
          case 1:
            final PyObject value = args[0];
            if (value.isNumberType()) {
              filter(value.asInt());
            } else {
              filter(Py.tojava(value, PShader.class));
            }
            return Py.None;
          case 2:
            final PyObject a = args[0];
            final PyObject b = args[1];
            if (a.isNumberType()) {
              filter(a.asInt(), (float)b.asDouble());
              return Py.None;
            }
            //$FALL-THROUGH$
          default:
            return builtinFilter.__call__(args, kws);
        }
      }
    });
  }

  /**
   * Populate the Python builtins namespace with PConstants.
   */
  public static void initializeStatics(final PyStringMap builtins) {
    for (final Field f : PConstants.class.getDeclaredFields()) {
      final int mods = f.getModifiers();
      if (Modifier.isPublic(mods) || Modifier.isStatic(mods)) {
        try {
          builtins.__setitem__(f.getName(), Py.java2py(f.get(null)));
        } catch (final Exception e) {
          e.printStackTrace();
        }
      }
    }
  }

  private void checkForRendererChangeException(final Throwable t) {
    if (t.getCause() instanceof RendererChangeException) {
      // This is an expected condition. PApplet uses an exception
      // to signal a change to the rendering context, so we unwrap
      // the Python exception to extract the signal, and pass it
      // up the stack.
      throw (RendererChangeException)t.getCause();
    }
  }

  /**
   * We have to override PApplet's size method in order to reset the Python
   * context's knowledge of the magic variables that reflect the state of the
   * sketch's world, particularly width and height.
   */
  @Override
  public void size(final int iwidth, final int iheight, final String irenderer, final String ipath) {
    super.size(iwidth, iheight, irenderer, ipath);
    builtins.__setitem__("g", Py.java2py(g));
    builtins.__setitem__("frame", Py.java2py(frame));
  }

  @Override
  public void setup() {
    builtins.__setitem__("frame", Py.java2py(frame));

    try {
      if (mode == Mode.STATIC) {
        // A static sketch gets called once, from this spot.
        Runner.log("Interpreting static-mode sketch.");
        interpretSketch();
      } else if (setupMeth != null) {
        // Call the Python sketch's setup()
        setupMeth.__call__();
      }
    } catch (final PyException e) {
      checkForRendererChangeException(e);
      terminalException = toSketchException(e);
      exit();
    } catch (final Exception e) {
      terminalException = toSketchException(e);
      exit();
    }
  }

  @Override
  public void draw() {
    if (drawMeth == null) {
      Runner.log("Calling super.draw() in what I assume is a static-mode sketch.");
      super.draw();
    } else if (!finished) {
      drawMeth.__call__();
    }
  }

  @Override
  public void loadPixels() {
    super.loadPixels();
    builtins.__setitem__("pixels", Py.java2py(pixels));
  }

  @Override
  public void mouseClicked() {
    if (mouseClickedMeth == null) {
      super.mouseClicked();
    } else {
      mouseClickedMeth.__call__();
    }
  }

  @Override
  public void mouseMoved() {
    if (mouseMovedMeth == null) {
      super.mouseMoved();
    } else {
      mouseMovedMeth.__call__();
    }
  }

  @Override
  public boolean sketchFullScreen() {
    if (sketchFullScreenMeth == null) {
      return super.sketchFullScreen();
    } else {
      return sketchFullScreenMeth.__call__().__nonzero__();
    }
  }

  @Override
  public int sketchWidth() {
    if (sketchWidthMeth == null) {
      return super.sketchWidth();
    } else {
      return sketchWidthMeth.__call__().asInt();
    }
  }

  @Override
  public String sketchRenderer() {
    if (sketchRendererMeth == null) {
      return super.sketchRenderer();
    } else {
      return sketchRendererMeth.__call__().asString();
    }
  }

  @Override
  public int sketchHeight() {
    if (sketchHeightMeth == null) {
      return super.sketchWidth();
    } else {
      return sketchHeightMeth.__call__().asInt();
    }
  }

  @Override
  public void mousePressed() {
    if (mousePressedMeth == null) {
      super.mousePressed();
    } else {
      mousePressedMeth.__call__();
    }
  }

  @Override
  public void mouseReleased() {
    if (mouseReleasedMeth == null) {
      super.mouseReleased();
    } else {
      mouseReleasedMeth.__call__();
    }
  }

  @Override
  public void mouseDragged() {
    if (mouseDraggedMeth == null) {
      super.mouseDragged();
    } else {
      mouseDraggedMeth.__call__();
    }
  }

  @Override
  public void keyPressed() {
    if (keyPressedMeth == null) {
      super.keyPressed();
    } else {
      keyPressedMeth.__call__();
    }
  }

  @Override
  public void keyReleased() {
    if (keyReleasedMeth == null) {
      super.keyReleased();
    } else {
      keyReleasedMeth.__call__();
    }
  }

  @Override
  public void keyTyped() {
    if (keyTypedMeth == null) {
      super.keyTyped();
    } else {
      keyTypedMeth.__call__();
    }
  }

  // Minim sketches seem to want to override stop()
  @Override
  public void stop() {
    try {
      if (stopMeth != null) {
        stopMeth.__call__();
      }
    } finally {
      super.stop();
    }
  }
}
