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

import java.io.File;
import java.lang.reflect.Field;
import java.lang.reflect.Modifier;
import java.util.HashSet;
import java.util.regex.Pattern;

import org.python.core.CompileMode;
import org.python.core.CompilerFlags;
import org.python.core.Py;
import org.python.core.PyException;
import org.python.core.PyInteger;
import org.python.core.PyJavaType;
import org.python.core.PyObject;
import org.python.core.PySet;
import org.python.core.PyStringMap;
import org.python.core.PyType;
import org.python.util.InteractiveConsole;

import processing.core.PApplet;
import processing.core.PConstants;
import processing.core.PImage;
import processing.core.PVector;

/**
 * 
 * @author Jonathan Feinberg &lt;jdf@pobox.com&gt;
 * 
 */
@SuppressWarnings("serial")
abstract public class PAppletJythonDriver extends PApplet {

    abstract protected void populateBuiltins();

    abstract protected void setFields();

    protected final PyStringMap builtins;
    protected final InteractiveConsole interp;
    private final String pySketchPath;
    private final String programText;

    // A static-mode sketch must be interpreted from with the setup() method.
    // All others are interpreted during construction in order to harvest method
    // definitions, which we then invoke during the run loop.
    private final boolean isStaticMode;

    // The presence of either setup() or draw() indicates that this is not a
    // static sketch.
    private static final Pattern ACTIVE_METHOD_DEF = Pattern.compile(
            "^def\\s+(setup|draw)\\s*\\(\\s*\\)\\s*:", Pattern.MULTILINE);

    // These are all of the methods that PApplet might call in your sketch. If
    // you have implemented a method, we save it and call it.
    private final PyObject setupMeth, drawMeth, mousePressedMeth,
            mouseClickedMeth, mouseReleasedMeth, mouseDraggedMeth,
            keyPressedMeth, keyReleasedMeth, keyTypedMeth, stopMeth;

    // Adapted from Jython's PythonInterpreter.java exec(String s) to preserve
    // the source file name, so that errors have the file name instead of
    // "<string>"
    private void interpretSketch() {
        try {
            Py.setSystemState(interp.getSystemState());
            Py.exec(Py.compile_flags(programText, pySketchPath,
                    CompileMode.exec, new CompilerFlags()), interp.getLocals(),
                    null);
            Py.flushLine();
        } catch (Throwable t) {
            checkForRendererChangeException(t);
            while (t.getCause() != null)
                t = t.getCause();
            t.printStackTrace(System.err);
            System.exit(-1);
        }
    }

    public PAppletJythonDriver(final InteractiveConsole interp,
            final String sketchPath, final String programText) {
        this.programText = programText;
        this.pySketchPath = sketchPath;
        this.sketchPath = new File(sketchPath).getParent();
        this.isStaticMode = !ACTIVE_METHOD_DEF.matcher(programText).find();
        this.builtins = (PyStringMap) interp.getSystemState().getBuiltins();
        this.interp = interp;
        initializeStatics(builtins);
        setSet();
        populateBuiltins();
        setFields();
        builtins.__setitem__("this", Py.java2py(this));

        if (!isStaticMode) {
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
        mouseReleasedMeth = interp.get("mouseReleased");
        mouseDraggedMeth = interp.get("mouseDragged");
        keyPressedMeth = interp.get("keyPressed");
        keyReleasedMeth = interp.get("keyReleased");
        keyTypedMeth = interp.get("keyTyped");
        stopMeth = interp.get("stop");
    }

    /**
     * Permit the punning use of set() by mucking with the builtin "set" Type.
     * If you call it with 3 arguments, it acts like the Processing set(x, y,
     * whatever) method. If you call it with 0 or 1 args, it constructs a Python
     * set.
     */
    private void setSet() {
        builtins.__setitem__("set", new PyJavaType() {
            {
                builtin = true;
                init(PySet.class, new HashSet<PyJavaType>());
                invalidateMethodCache();
            }

            @Override
            public PyObject __call__(PyObject[] args, String[] kws) {
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
                        if (tx == PyInteger.TYPE && ty == PyInteger.TYPE
                                && tc == PyInteger.TYPE) {
                            set(x.asInt(), y.asInt(), c.asInt());
                            return Py.None;
                        } else if (tx == PyInteger.TYPE && ty == PyInteger.TYPE
                                && tc.getProxyType() != null
                                && tc.getProxyType() == PImage.class) {
                            set(x.asInt(),
                                    y.asInt(),
                                    (processing.core.PImage) c
                                            .__tojava__(processing.core.PImage.class));
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
     * Populate the Python builtins namespace with PConstants.
     */
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

    private void checkForRendererChangeException(final Throwable t) {
        if (t.getCause() instanceof RendererChangeException) {
            // This is an expected condition. PApplet uses an exception
            // to signal a change to the rendering context, so we unwrap
            // the Python exception to extract the signal, and pass it
            // up the stack.
            throw (RendererChangeException) t.getCause();
        }
    }

    /**
     * We have to override PApplet's size method in order to reset the Python
     * context's knowledge of the magic variables that reflect the state of the
     * sketch's world, particularly width and height.
     */
    @Override
    public void size(final int iwidth, final int iheight,
            final String irenderer, final String ipath) {
        super.size(iwidth, iheight, irenderer, ipath);
        setFields();
    }

    @Override
    public void setup() {
        // Put all of PApplet's globals into the Python context
        setFields();

        try {
            if (isStaticMode) {
                // A static sketch gets called once, from this spot.
                interpretSketch();
            } else if (setupMeth != null) {
                // Call the Python sketch's setup()
                setupMeth.__call__();
            }
        } catch (PyException e) {
            checkForRendererChangeException(e);
            throw e;
        }
    }

    @Override
    public void draw() {
        if (drawMeth == null) {
            super.draw();
        } else {
            // Put all of PApplet's globals into the Python context
            setFields();
            drawMeth.__call__();
        }
    }

    @Override
    public void mouseClicked() {
        if (mouseClickedMeth == null) {
            super.mouseClicked();
        } else {
            // Put all of PApplet's globals into the Python context
            setFields();
            mouseClickedMeth.__call__();
        }
    }

    @Override
    public void mousePressed() {
        if (mousePressedMeth == null) {
            super.mousePressed();
        } else {
            // Put all of PApplet's globals into the Python context
            setFields();
            mousePressedMeth.__call__();
        }
    }

    @Override
    public void mouseReleased() {
        if (mouseReleasedMeth == null) {
            super.mouseReleased();
        } else {
            // Put all of PApplet's globals into the Python context
            setFields();
            mouseReleasedMeth.__call__();
        }
    }

    @Override
    public void mouseDragged() {
        if (mouseDraggedMeth == null) {
            super.mouseDragged();
        } else {
            // Put all of PApplet's globals into the Python context
            setFields();
            mouseDraggedMeth.__call__();
        }
    }

    @Override
    public void keyPressed() {
        if (keyPressedMeth == null) {
            super.keyPressed();
        } else {
            // Put all of PApplet's globals into the Python context
            setFields();
            keyPressedMeth.__call__();
        }
    }

    @Override
    public void keyReleased() {
        if (keyReleasedMeth == null) {
            super.keyReleased();
        } else {
            // Put all of PApplet's globals into the Python context
            setFields();
            keyReleasedMeth.__call__();
        }
    }

    @Override
    public void keyTyped() {
        if (keyTypedMeth == null) {
            super.keyTyped();
        } else {
            // Put all of PApplet's globals into the Python context
            setFields();
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
