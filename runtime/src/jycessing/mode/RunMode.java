package jycessing.mode;

import jycessing.mode.run.SketchInfo;
import processing.core.PApplet;

public enum RunMode {
  UNIT_TEST {
    @Override
    public String[] args(final SketchInfo info) {
      return new String[] {info.sketchName, pathArg(info)};
    }
  },
  WINDOWED {
    @Override
    public String[] args(final SketchInfo info) {
      return new String[] {String.format("--editor-location=%d,%d", info.x, info.y),
          info.sketchName, pathArg(info)};
    }
  },
  PRESENTATION {
    @Override
    public String[] args(final SketchInfo info) {
      return new String[] {"--present", "--external", info.sketchName, pathArg(info)};
    }
  };
  abstract public String[] args(SketchInfo info);

  private static String pathArg(final SketchInfo info) {
    return PApplet.ARGS_SKETCH_FOLDER + "=" + info.sketch.getParent();
  }

}
