package jycessing.mode;

public enum RunMode {
  UNIT_TEST {
    @Override
    public String[] args(final String sketchName, final int x, final int y) {
      return new String[] {sketchName};
    }
  },
  WINDOWED {
    @Override
    public String[] args(final String sketchName, final int x, final int y) {
      return new String[] {String.format("--editor-location=%d,%d", x, y), sketchName};
    }
  },
  PRESENTATION {
    @Override
    public String[] args(final String sketchName, final int x, final int y) {
      return new String[] {"--present", "--external", sketchName};
    }
  };
  abstract public String[] args(final String sketchName, final int x, final int y);
}
