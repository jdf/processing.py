package jycessing.mode.export;

/**
 * The architecture of the platform we're exporting to. (The "bits" field is necessary because the
 * processing Library API uses magic integers for architecture.)
 */
public enum Arch {
  X86(32),
  AMD64(64);

  public final int bits;

  Arch(final int bits) {
    this.bits = bits;
  }
}
