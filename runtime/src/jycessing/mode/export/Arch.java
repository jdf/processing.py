package jycessing.mode.export;

public enum Arch {
  X86(32),
  AMD64(64);
  
  public final int bits;
  
  Arch(int bits) {
    this.bits = bits;
  }
}
