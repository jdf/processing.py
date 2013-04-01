package jycessing.primitives;

import jycessing.annotations.PythonUsage;

/**
 * Primitive float class. Serves as a container for libraries such as Ani.
 * 
 * @author Ralf Biedert <rb@xr.io>
 */
@PythonUsage(methodName = "PrimitiveFloat")
public class PrimitiveFloat {
  public PrimitiveFloat(float value) {
    this.value = value;
  }

  public float value = 0.0f;

  @Override
  public String toString() {
    return "" + value;
  }
}
