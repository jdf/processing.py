package jycessing.jni;

import processing.core.PApplet;
import processing.core.PConstants;

public class OSX {
  public static void bringToFront() {
    if (PApplet.platform == PConstants.MACOSX) {
      try {
        System.loadLibrary("jniosx");
        activateIgnoringOtherApps();
      } catch (final UnsatisfiedLinkError err) {
        System.err.println("Hmm. Can't load native code to bring window to front.");
      }
    }
  }

  private static native void activateIgnoringOtherApps();
}
