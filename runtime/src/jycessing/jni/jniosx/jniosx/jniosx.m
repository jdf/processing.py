#include "jycessing_jni_OSX.h"

#import "AppKit/AppKit.h"

JNIEXPORT void JNICALL Java_jycessing_jni_OSX_activateIgnoringOtherApps
(JNIEnv *env, jclass klass) {
  [NSApp activateIgnoringOtherApps:true];
}
