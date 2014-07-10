package jycessing.mode;

import java.awt.Point;

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
    private String locArg(final String arg, final Point p) {
      return String.format("%s=%d,%d", arg, p.x, p.y);
    }

    @Override
    public String[] args(final SketchInfo info) {
      if (info.sketchLoc != null) {
        return new String[] { PApplet.ARGS_EXTERNAL, locArg(PApplet.ARGS_LOCATION, info.sketchLoc), info.sketchName, pathArg(info) };
      }

      if (info.editorLoc != null) {
        return new String[] { PApplet.ARGS_EXTERNAL, locArg(PApplet.ARGS_EDITOR_LOCATION, info.editorLoc), info.sketchName, pathArg(info) };
      }

      return new String[] { PApplet.ARGS_EXTERNAL, info.sketchName, pathArg(info) };
    }
  },
  PRESENTATION {
    @Override
    public String[] args(final SketchInfo info) {
      return new String[] {PApplet.ARGS_FULL_SCREEN, PApplet.ARGS_EXTERNAL, info.sketchName,
          pathArg(info)};
    }
  };
  abstract public String[] args(SketchInfo info);

  private static String pathArg(final SketchInfo info) {
    return PApplet.ARGS_SKETCH_FOLDER + "=" + info.sketchHome.getAbsolutePath();
  }

}
