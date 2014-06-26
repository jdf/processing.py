package jycessing;

import java.awt.Point;
import java.io.Serializable;

import com.google.common.collect.ObjectArrays;

import jycessing.mode.run.SketchInfo;
import processing.core.PApplet;

public class RunMode implements Serializable {
  
  public final SketchType sketchType;
  public final DisplayType displayType;
  
  public RunMode(SketchType type, DisplayType display){
    this.sketchType = type;
    this.displayType = display;
  }
  
  public String[] args(final SketchInfo info) {
    return ObjectArrays.concat(displayType.args(info), sketchType.args(info), String.class);
  }
  
  public enum SketchType {
    FROM_PDE {
      @Override
      public String[] args(final SketchInfo info) {
        return new String[] { info.sketchName, pathArg(info), PApplet.ARGS_EXTERNAL,
            info.sketchName, pathArg(info) };
      }
    },
    EXPORT {
      @Override
      public String[] args(final SketchInfo info) {
        return new String[] { info.sketchName, pathArg(info) };
      }
    },
    SCRIPT {
      public String[] args(final SketchInfo info) {
        return new String[] { info.sketchName, pathArg(info) };
      }
    },
    UNIT_TEST {
      @Override
      public String[] args(final SketchInfo info) {
        return new String[] { info.sketchName, pathArg(info) };
      }
    };
    private static String pathArg(final SketchInfo info) {
      return PApplet.ARGS_SKETCH_FOLDER + "="
          + info.sketchHome.getAbsolutePath();
    }

    abstract public String[] args(SketchInfo info);
  }

  public static enum DisplayType {
    NONE {
      @Override
      public String[] args(final SketchInfo info) {
        return new String[] {};
      }
    },
    WINDOWED {
      private String locArg(final String arg, final Point p) {
        return String.format("%s=%d,%d", arg, p.x, p.y);
      }
      @Override
      public String[] args(final SketchInfo info) {
        final String locArg;
        if (info.sketchLoc == null) {
          if (info.editorLoc == null) {
            locArg = locArg(PApplet.ARGS_LOCATION, new Point(0, 0));
          } else {
            locArg = locArg(PApplet.ARGS_EDITOR_LOCATION, info.editorLoc);
          }
        } else {
          locArg = locArg(PApplet.ARGS_LOCATION, info.sketchLoc);
        }
        return new String[] { locArg };
      }
    },
    PRESENTATION {
      @Override
      public String[] args(final SketchInfo info) {
        return new String[] { PApplet.ARGS_FULL_SCREEN };
      }
    };

    abstract public String[] args(SketchInfo info);
  }

}
