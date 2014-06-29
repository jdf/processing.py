package jycessing;

import java.awt.Point;
import java.io.File;
import java.io.Serializable;
import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import com.google.common.collect.ObjectArrays;

import jycessing.mode.run.SketchInfo;
import processing.core.PApplet;

public class RunMode implements Serializable {
  
  private static void log(String message) {
    if (Runner.VERBOSE) {
      System.err.println(message);
    }
  }
  
  public final SketchType sketchType;
  public final DisplayType displayType;
  
  public RunMode(SketchType type, DisplayType display){
    this.sketchType = type;
    this.displayType = display;
  }
  
  public String[] args(final SketchInfo info) {
    return ObjectArrays.concat(displayType.args(info), sketchType.args(info), String.class);
  }
  
  public String toString() {
    return "RunMode("+sketchType+","+displayType+")";
  }
  
  public File getLibraryDir(final String sketchPath){
    return sketchType.getLibraryDir(sketchPath);
  }
  
  public File getHomeDir(final String sketchPath){
    return sketchType.getHomeDir(sketchPath);
  }
  
  public File getSourceDir(final String sketchPath){
    return sketchType.getSourceDir(sketchPath);
  }
  
  public enum SketchType {
    FROM_PDE {
      @Override
      public String[] args(final SketchInfo info) {
        return new String[] { info.sketchName, pathArg(info), PApplet.ARGS_EXTERNAL };
      }
    },
    EXPORT {
      @Override
      public String[] args(final SketchInfo info) {
        return new String[] { info.sketchName, pathArg(info) };
      }
      @Override
      public File getLibraryDir(final String sketchPath){
        final File exportDir = new File(sketchPath).getAbsoluteFile().getParentFile().getParentFile();
        final File libDir = new File(exportDir, "lib");
        if (libDir.exists()) {
          return libDir;
        }
        
        return null;
      }
      @Override
      public File getHomeDir(final String sketchPath){
        return new File(sketchPath).getAbsoluteFile().getParentFile().getParentFile();
      }
      @Override
      public File getSourceDir(final String sketchPath){
        return new File(sketchPath).getAbsoluteFile().getParentFile();
      }
    },
    SCRIPT {
      @Override
      public String[] args(final SketchInfo info) {
        return new String[] { info.sketchName, pathArg(info) };
      }
      
      @Override
      public File getLibraryDir(final String sketchPath){
        final String BUILD_PROPERTIES = "build.properties";
        final Pattern JAR_RESOURCE = Pattern.compile("jar:file:(.+?)/processing-py\\.jar!/jycessing/" 
            + Pattern.quote(BUILD_PROPERTIES));
        final Pattern FILE_RESOURCE = Pattern.compile("file:(.+?)/bin/jycessing/"
            + Pattern.quote(BUILD_PROPERTIES));
        
        final String propsResource;
        try {
          propsResource = URLDecoder.decode(
              Runner.class.getResource(BUILD_PROPERTIES).toString(), "UTF-8");
        } catch (final UnsupportedEncodingException e) {
          throw new RuntimeException("Impossible: " + e);
        }

        {
          final Matcher m = JAR_RESOURCE.matcher(propsResource);
          if (m.matches()) {
            log("We're running from a JAR file.");
            return new File(m.group(1), "libraries");
          }
        }
        {
          final Matcher m = FILE_RESOURCE.matcher(propsResource);
          if (m.matches()) {
            log("We're running from class files.");
            return new File(m.group(1), "libraries");
          }
        }
        return null;
      }
      @Override
      public File getHomeDir(final String sketchPath){
        return new File(sketchPath).getAbsoluteFile().getParentFile();
      }
      @Override
      public File getSourceDir(final String sketchPath){
        return new File(sketchPath).getAbsoluteFile().getParentFile();
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

    abstract public String[] args(final SketchInfo info);
    public File getLibraryDir(final String sketchPath) {
      return null;
    }
    public File getHomeDir(final String sketchPath) {
      return null;
    }
    public File getSourceDir(final String sketchPath) {
      return null;
    }
  }

  public enum DisplayType {
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
        ArrayList<String> args = new ArrayList<>();
        if (info.backgroundColor != null) {
          args.add(PApplet.ARGS_BGCOLOR+"="+info.backgroundColor);
        }
        
        if (info.stopColor != null) {
          args.add(PApplet.ARGS_STOP_COLOR+"="+info.stopColor);
        } else {
          args.add(PApplet.ARGS_HIDE_STOP);
        }
        
        args.add(PApplet.ARGS_FULL_SCREEN);
        
        return args.toArray(new String[0]);
      }
    };

    abstract public String[] args(SketchInfo info);
  }

}
