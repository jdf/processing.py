package jycessing.mode.export;

import processing.core.PConstants;

public class Linux extends ExportPlatform {
  public Linux(int bits) {
    this.id = PConstants.LINUX;
    this.bits = bits;
    this.name = PConstants.platformNames[id] + bits;
  }
}
