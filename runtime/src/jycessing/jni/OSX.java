package jycessing.jni;

import jycessing.mode.PythonMode;
import processing.core.PApplet;
import processing.core.PConstants;

public class OSX {
  private static volatile boolean didLoad = false;

  public static void bringToFront() {
    if (!didLoad && (PApplet.platform == PConstants.MACOS)) {
      try {
        System.loadLibrary("jniosx");
        didLoad = true;
      } catch (final UnsatisfiedLinkError err) {
        System.err.println("Hmm. Can't load native code to bring window to front.");
      }
    }
    if (didLoad) {
      activateIgnoringOtherApps();
    }
  }

  public static void bringToFront(PythonMode mode) {
    if (!didLoad && (PApplet.platform == PConstants.MACOS)) {
      String path = null;
      try {
        path = mode.getContentFile("mode").getAbsolutePath() + "/libjniosx.dylib";
        System.load(path);
        didLoad = true;
      } catch (final UnsatisfiedLinkError err) {
        System.err.println(
            "Hmm. Can't load native code to bring window to front using the absolute path: " + path
                + ".");
      }
    }
    bringToFront();
  }

  private static native void activateIgnoringOtherApps();
}
