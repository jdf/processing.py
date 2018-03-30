package jycessing.jni;

import processing.core.PApplet;
import processing.core.PConstants;

public class OSX {
  private static volatile boolean didLoad = false;

  static {
    if (PApplet.platform == PConstants.MACOSX) {
      try {
        System.loadLibrary("jniosx");
        didLoad = true;
      } catch (final UnsatisfiedLinkError err) {
        System.err.println("Hmm. Can't load native code to bring window to front.");
      }
    }
  }

  public static void bringToFront() {
    if (didLoad) {
      activateIgnoringOtherApps();
    }
  }

  private static native void activateIgnoringOtherApps();
}
