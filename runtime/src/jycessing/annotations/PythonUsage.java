/**
 * 
 */
package jycessing.annotations;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * Reminds you that this method is used from Python. Unless you know what 
 * you're doing, do not change its name.
 * 
 * @author Ralf Biedert <rb@xr.io>
 */
@Retention(RetentionPolicy.RUNTIME)
@Target(value = { ElementType.METHOD, ElementType.FIELD, ElementType.TYPE })
public @interface PythonUsage {
  /**
   * The original method name. Must match with the actual method name. 
   * 
   * @return The original method name.
   */
  public String methodName();
}
