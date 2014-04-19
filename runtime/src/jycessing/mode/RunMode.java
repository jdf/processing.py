package jycessing.mode;

public enum RunMode {
  UNIT_TEST {
    @Override
    public String[] args(final String sketchPath, final int x, final int y) {
      return new String[] {sketchPath};
    }
  },
  WINDOWED {
    @Override
    public String[] args(final String sketchPath, final int x, final int y) {
      return new String[] {String.format("--editor-location=%d,%d", x, y), sketchPath};
    }
  },
  PRESENTATION {
    @Override
    public String[] args(final String sketchPath, final int x, final int y) {
      return new String[] {"--present", "--external", sketchPath};
    }
  };
  abstract public String[] args(final String sketchPath, final int x, final int y);
}
