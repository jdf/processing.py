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

import org.python.antlr.ast.Global;
import org.python.core.CompileMode;
import org.python.core.CompilerFlags;
import org.python.core.Py;
import org.python.core.PyBoolean;
import org.python.core.PyCode;
import org.python.core.PyException;
import org.python.core.PyFloat;
import org.python.core.PyIndentationError;
import org.python.core.PyInteger;
import org.python.core.PyJavaType;
import org.python.core.PyObject;
import org.python.core.PySet;
import org.python.core.PyString;
import org.python.core.PyStringMap;
import org.python.core.PySyntaxError;
import org.python.core.PyTuple;
import org.python.core.PyType;
import org.python.util.InteractiveConsole;

import processing.core.PApplet;
import processing.core.PConstants;
import processing.core.PImage;
import processing.opengl.PShader;

import java.awt.EventQueue;
import java.awt.Window;
import java.awt.event.ComponentAdapter;
import java.awt.event.ComponentEvent;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.File;
import java.lang.Thread.UncaughtExceptionHandler;
import java.lang.reflect.Field;
import java.lang.reflect.Modifier;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import javax.swing.SwingUtilities;

/**
 *
 * @author Jonathan Feinberg &lt;jdf@pobox.com&gt;
 *
 */
@SuppressWarnings("serial")
public class PAppletJythonDriver extends PApplet {

  private static final String GLOBAL_STATEMENT_TEXT = IOUtil
      .readTextOrDie(PAppletJythonDriver.class.getResourceAsStream("add_global_statements.py"));

  static {
    // There's some bug that I don't understand yet that causes the native file
    // select box to fire twice, skipping confirmation the first time.
    useNativeSelect = false;
  }

  private PythonSketchError terminalException = null;

  protected final PyStringMap builtins;
  protected final InteractiveConsole interp;
  private final String pySketchPath;
  private final String programText;

  private final CountDownLatch finishedLatch = new CountDownLatch(1);

  /**
   * Because of a bad interaction between Java and Jython, integers with the high bit set
   * become negative integers when accessed in Jython, which means that a color like
   * opaque green (0xFF00FF00) does not survive the round-trip into from Python into
   * Java and back (i.e., the sequence
   * <pre>fill(0xFF00FF00)
   * rect(0, 0, 20, 20)
   * assert get(10, 10) == 0xFF00FF00</pre>
   * fails.
   * <p>Therefore, we override get(), loadPixels(), and updatePixels(), and we shadow
   * the PApplet pixels[] array with this:
   */
  private long[] longPixels;

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
      pauseMeth, resumeMeth, stopMeth, destroyMeth, sketchFullScreenMeth, sketchWidthMeth,
      sketchHeightMeth, sketchRendererMeth;

  // Adapted from Jython's PythonInterpreter.java exec(String s) to preserve
  // the source file name, so that errors have the file name instead of
  // "<string>"
  private void interpretSketch() throws PythonSketchError {
    try {
      Py.setSystemState(interp.getSystemState());
      interp.set("__processing_source__", programText);
      final PyCode code =
          Py.compile_flags(GLOBAL_STATEMENT_TEXT, pySketchPath, CompileMode.exec,
              new CompilerFlags());
      Py.exec(code, interp.getLocals(), null);
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
    if (t instanceof RuntimeException && t.getCause() != null) {
      t = t.getCause();
    }
    if (t instanceof PythonSketchError) {
      return (PythonSketchError)t;
    }
    if (t instanceof PySyntaxError) {
      final PySyntaxError e = (PySyntaxError)t;
      return extractSketchErrorFromPyExceptionValue((PyTuple)e.value);
    }
    if (t instanceof PyIndentationError) {
      final PyIndentationError e = (PyIndentationError)t;
      return extractSketchErrorFromPyExceptionValue((PyTuple)e.value);
    }
    if (t instanceof PyException) {
      final PyException e = (PyException)t;
      final Pattern tbParse =
          Pattern.compile("^\\s*File \"([^\"]+)\", line (\\d+)", Pattern.MULTILINE);
      final Matcher m = tbParse.matcher(e.toString());
      String file = null;
      int line = -1;
      while (m.find()) {
        final String fileName = m.group(1);
        // Ignore stack elements that come from exec()ing code in the interpreter from Java.
        if (fileName.equals("<string>")) {
          continue;
        }
        file = fileName;
        // Throw away the path.
        if (new File(file).exists()) {
          file = new File(file).getName();
        }
        line = Integer.parseInt(m.group(2)) - 1;
      }
      if (((PyType)e.type).getName().equals("ImportError")) {
        final Pattern importStar = Pattern.compile("import\\s+\\*");
        if (importStar.matcher(e.toString()).find()) {
          return new PythonSketchError("import * does not work in this environment.", file, line);
        }
      }
      return new PythonSketchError(Py.formatException(e.type, e.value), file, line);
    }
    return new PythonSketchError(t.getClass().getSimpleName() + ": " + t.getMessage());
  }

  private static PythonSketchError extractSketchErrorFromPyExceptionValue(final PyTuple tup) {
    final String message = maybeMakeFriendlyMessage((String)tup.get(0));
    final PyTuple context = (PyTuple)tup.get(1);
    final String file = new File((String)context.get(0)).getName();
    final int line = ((Integer)context.get(1)).intValue() - 1;
    final int column = ((Integer)context.get(2)).intValue();
    return new PythonSketchError(message, file, line, column);
  }

  private static String maybeMakeFriendlyMessage(final String message) {
    if (message.contains("expecting INDENT")) {
      return "This line needs be indented.";
    }
    return message;
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
    setLerpColor();
    setGet();
    builtins.__setitem__("g", Py.java2py(g));
    // There's a bug in ast.Global that makes it impossible to construct a valid Global
    // using the constructor that takes a list of names. This crazy thing is a workaround
    // for that.
    builtins.__setitem__("__global__", new PyObject() {
      @Override
      public PyObject __call__(final PyObject names) {
        final List<String> newNames = new ArrayList<>();
        for (final Object o : names.asIterable()) {
          newNames.add(o.toString());
        }
        final Global glowball = new Global();
        ReflectionUtil.setObject(glowball, "names", newNames);
        return glowball;
      }
    });

    addComponentListener(new ComponentAdapter() {
      @Override
      public void componentHidden(final ComponentEvent e) {
        finishedLatch.countDown();
      }
    });
  }

  @Override
  protected void exitActual() {
    stop();
    destroy();
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
    pauseMeth = interp.get("pause");
    resumeMeth = interp.get("resume");
    destroyMeth = interp.get("destroy");
    if (mousePressedMeth != null) {
      // The user defined a mousePressed() method, which will hide the magical
      // Processing variable boolean mousePressed. We have to do some magic.
      interp.getLocals().__setitem__("mousePressed", new PyBoolean(false) {
        @Override
        public boolean getBooleanValue() {
          return mousePressed;
        }

        @Override
        public PyObject __call__(final PyObject[] args, final String[] kws) {
          return mousePressedMeth.__call__(args, kws);
        }
      });
    }

  }

  /*
   * Most of the time we're wrapping small, positive integers (like the mouse
   * position, the keyCode, and the frameCount). So we pre-allocate a bunch of
   * them to avoid garbage collection.
   */
  private static final PyInteger[] CHEAP_INTS = new PyInteger[20000];
  static {
    for (int i = 0; i < CHEAP_INTS.length; i++) {
      CHEAP_INTS[i] = Py.newInteger(i);
    }
  }

  private static PyInteger pyint(final int i) {
    return i >= 0 && i < CHEAP_INTS.length ? CHEAP_INTS[i] : Py.newInteger(i);
  }

  protected void wrapProcessingVariables() {
    wrapMouseVariables();
    builtins.__setitem__("displayWidth", pyint(displayWidth));
    builtins.__setitem__("displayHeight", pyint(displayHeight));
    builtins.__setitem__("paused", Py.newBoolean(paused));
    builtins.__setitem__("focused", Py.newBoolean(focused));
    builtins.__setitem__("keyPressed", Py.newBoolean(keyPressed));
    builtins.__setitem__("frameCount", pyint(frameCount));
    builtins.__setitem__("frameRate", new PyFloat(frameRate) {
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

    wrapKeyVariables();
  }

  // We only change the "key" variable as necessary to avoid generating
  // lots of PyUnicode garbage.
  private char lastKey = Character.MIN_VALUE;

  private void wrapKeyVariables() {
    if (lastKey != key) {
      lastKey = key;
      /*
       * If key is "CODED", i.e., an arrow key or other non-printable, pass that
       * value through as-is. If it's printable, convert it to a unicode string,
       * so that the user can compare key == 'x' instead of key == ord('x').
       */
      final PyObject pyKey = key == CODED ? pyint(key) : Py.newUnicode(key);
      builtins.__setitem__("key", pyKey);
    }
    builtins.__setitem__("keyCode", pyint(keyCode));
  }

  private void wrapMouseVariables() {
    builtins.__setitem__("mouseX", pyint(mouseX));
    builtins.__setitem__("mouseY", pyint(mouseY));
    builtins.__setitem__("pmouseX", pyint(pmouseX));
    builtins.__setitem__("pmouseY", pyint(pmouseY));
    builtins.__setitem__("mouseButton", pyint(mouseButton));
    if (mousePressedMeth == null) {
      builtins.__setitem__("mousePressed", Py.newBoolean(mousePressed));
    }
  }

  @Override
  public void start() {
    // I want to quit on runtime exceptions.
    // Processing just sits there by default.
    Thread.setDefaultUncaughtExceptionHandler(new UncaughtExceptionHandler() {
      @Override
      public void uncaughtException(final Thread t, final Throwable e) {
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
    EventQueue.invokeLater(new Runnable() {
      @Override
      public void run() {
        frame.toFront();
      }
    });
    frame.addWindowListener(new WindowAdapter() {
      @Override
      public void windowClosing(final WindowEvent e) {
        exit();
      }
    });
    try {
      finishedLatch.await();
    } catch (final InterruptedException interrupted) {
      // Treat an interruption as a request to the applet to terminate.
      exit();
      try {
        finishedLatch.await();
      } catch (final InterruptedException e) {
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
    final PyType originalSet = (PyType)builtins.__getitem__("set");
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
            return originalSet.__call__(args, kws);
          case 3: {
            final int x = args[0].asInt();
            final int y = args[1].asInt();
            final PyObject c = args[2];
            final PyType tc = c.getType();
            if (tc.getProxyType() != null && PImage.class.isAssignableFrom(tc.getProxyType())) {
              set(x, y, (processing.core.PImage)c.__tojava__(processing.core.PImage.class));
              return Py.None;
            } else {
              set(x, y, interpretColorArg(c));
              return Py.None;
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

  public String hex(final long n) {
    return Long.toHexString(n);
  }

  /*
   * If you fill(0xAARRGGBB), for some reason Jython decides to
   * invoke the fill(float) method, unless we provide a long int
   * version to catch it.
   */
  public void fill(final long argb) {
    fill((int)(argb & 0xFFFFFFFF));
  }

  public void stroke(final long argb) {
    stroke((int)(argb & 0xFFFFFFFF));
  }

  /*
   * Python can't parse web colors, we we let the user do '#RRGGBB'
   * as a string.
   */
  public void fill(final String argbSpec) {
    fill(parseColorSpec(argbSpec));
  }

  public void stroke(final String argbSpec) {
    stroke(parseColorSpec(argbSpec));
  }

  private int parseColorSpec(final String argbSpec) {
    if (argbSpec.startsWith("#")) {
      try {
        return 0xFF000000 | Integer.decode(argbSpec);
      } catch (final NumberFormatException e) {
      }
    }
    throw new RuntimeException("I can't understand \"" + argbSpec + "\" as a color.");
  }

  /**
   * The positional arguments to lerpColor may be long integers or CSS-style
   * string specs.
   * @param arg A color argument.
   * @return the integer correspnding to the intended color.
   */
  private int interpretColorArg(final PyObject arg) {
    return arg.getType() == PyString.TYPE ? parseColorSpec(arg.asString())
        : (int)(arg.asLong() & 0xFFFFFFFF);
  }

  /**
   * Permit both the instance method lerpColor and the static method lerpColor.
   * Also permit 0xAARRGGBB, '#RRGGBB', and 0-255.
   */
  private void setLerpColor() {
    builtins.__setitem__("lerpColor", new PyObject() {
      @Override
      public PyObject __call__(final PyObject[] args, final String[] kws) {
        final int c1 = interpretColorArg(args[0]);
        final int c2 = interpretColorArg(args[1]);
        final float amt = (float)args[2].asDouble();
        switch (args.length) {
          case 3:
            return Py.newInteger(lerpColor(c1, c2, amt));
          case 4:
            final int colorMode = (int)(args[3].asLong() & 0xFFFFFFFF);
            return Py.newInteger(lerpColor(c1, c2, amt, colorMode));
            //$FALL-THROUGH$
          default:
            throw new RuntimeException("lerpColor takes either 3 or 4 arguments, but I got "
                + args.length + ".");
        }
      }
    });
  }

  /**
   * Fix the result of pixel gets, which wind up as negative ints rather than
   * unsigned quantities.
   */
  private void setGet() {
    builtins.__setitem__("get", new PyObject() {
      @Override
      public PyObject __call__(final PyObject[] args, final String[] kws) {
        switch (args.length) {
          case 0:
            return Py.java2py(get());
          case 2:
            return Py.newLong(get(args[0].asInt(), args[1].asInt()) & 0xFFFFFFFFL);
          case 4:
            return Py.java2py(get(args[0].asInt(), args[1].asInt(), args[2].asInt(),
                args[3].asInt()));
            //$FALL-THROUGH$
          default:
            throw new RuntimeException("get() takes 0, 2, or 4 arguments, but I got " + args.length
                + ".");
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

  private void checkForRendererChangeException(Throwable t) {
    // This is an expected condition. PApplet uses an exception
    // to signal a change to the rendering context, so we unwrap
    // the Python exception to extract the signal, and pass it
    // up the stack.
    while (t != null) {
      if (t instanceof RendererChangeException) {
        throw (RendererChangeException)t;
      }
      t = t.getCause();
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
    builtins.__setitem__("width", Py.newInteger(width));
    builtins.__setitem__("height", Py.newInteger(height));
  }

  @Override
  public void setup() {
    builtins.__setitem__("frame", Py.java2py(frame));
    wrapProcessingVariables();
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
      checkForRendererChangeException(e);
      terminalException = toSketchException(e);
      exit();
    }
  }

  @Override
  public void draw() {
    wrapProcessingVariables();
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
    if (longPixels == null || longPixels.length != pixels.length) {
      longPixels = new long[pixels.length];
    }
    for (int i = 0; i < pixels.length; i++) {
      longPixels[i] = pixels[i] & 0xFFFFFFFFL;
    }
    builtins.__setitem__("pixels", Py.java2py(longPixels));
  }

  @Override
  public void updatePixels() {
    for (int i = 0; i < longPixels.length; i++) {
      pixels[i] = (int)(longPixels[i] & 0xFFFFFFFFL);
    }
    super.updatePixels();
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
  public void mouseClicked() {
    if (mouseClickedMeth == null) {
      super.mouseClicked();
    } else {
      wrapMouseVariables();
      mouseClickedMeth.__call__();
    }
  }

  @Override
  public void mouseMoved() {
    if (mouseMovedMeth == null) {
      super.mouseMoved();
    } else {
      wrapMouseVariables();
      mouseMovedMeth.__call__();
    }
  }


  @Override
  public void mousePressed() {
    if (mousePressedMeth == null) {
      super.mousePressed();
    } else {
      wrapMouseVariables();
      mousePressedMeth.__call__();
    }
  }

  @Override
  public void mouseReleased() {
    if (mouseReleasedMeth == null) {
      super.mouseReleased();
    } else {
      wrapMouseVariables();
      mouseReleasedMeth.__call__();
    }
  }

  @Override
  public void mouseDragged() {
    if (mouseDraggedMeth == null) {
      super.mouseDragged();
    } else {
      wrapMouseVariables();
      mouseDraggedMeth.__call__();
    }
  }

  @Override
  public void keyPressed() {
    if (keyPressedMeth == null) {
      super.keyPressed();
    } else {
      wrapKeyVariables();
      keyPressedMeth.__call__();
    }
  }

  @Override
  public void keyReleased() {
    if (keyReleasedMeth == null) {
      super.keyReleased();
    } else {
      wrapKeyVariables();
      keyReleasedMeth.__call__();
    }
  }

  @Override
  public void keyTyped() {
    if (keyTypedMeth == null) {
      super.keyTyped();
    } else {
      wrapKeyVariables();
      keyTypedMeth.__call__();
    }
  }

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

  @Override
  public void pause() {
    try {
      if (pauseMeth != null) {
        pauseMeth.__call__();
      }
    } finally {
      super.pause();
    }
  }

  @Override
  public void resume() {
    try {
      if (resumeMeth != null) {
        resumeMeth.__call__();
      }
    } finally {
      super.resume();
    }
  }

  @Override
  public void destroy() {
    try {
      if (destroyMeth != null) {
        destroyMeth.__call__();
      }
    } finally {
      super.destroy();
    }
  }

  /**
   * Processing uses reflection to call file selection callbacks by name.
   * We fake out that stuff with one of these babies.
   */
  public class FileSelectCallbackProxy {
    private final PyObject callback;

    public FileSelectCallbackProxy(final String name) {
      callback = interp.get(name);
      if (callback == null) {
        throw new RuntimeException("I can't find a callback function named \"" + name + "\"");
      }
    }

    // Called only by reflection.
    @SuppressWarnings("unused")
    public void handleCallback(final File selection) {
      callback.__call__(Py.java2py(selection));
    }
  }

  @Override
  public void selectFolder(final String prompt, final String callback, final File file) {
    super.selectFolder(prompt, "handleCallback", file, new FileSelectCallbackProxy(callback));
  }

  @Override
  public void selectInput(final String prompt, final String callback, final File file) {
    super.selectInput(prompt, "handleCallback", file, new FileSelectCallbackProxy(callback));
  }

  @Override
  public void selectOutput(final String prompt, final String callback, final File file) {
    super.selectOutput(prompt, "handleCallback", file, new FileSelectCallbackProxy(callback));
  }

  // These two functions are a workaround for a Jython bug that prevents the print statement
  // from using the stdout and stderr set on the interpreter. See core.py.
  public void printout(final Object o) {
    System.out.print(String.valueOf(o));
    System.out.flush();
  }

  public void printerr(final Object o) {
    System.err.print(String.valueOf(o));
    System.err.flush();
  }
}
