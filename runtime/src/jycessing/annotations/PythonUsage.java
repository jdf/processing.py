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
 * you do, do not change it's name
 * 
 * @author Ralf Biedert <rb@xr.io>
 */
@Retention(RetentionPolicy.RUNTIME)
@Target(value = { ElementType.METHOD, ElementType.FIELD })
public @interface PythonUsage {
  /**
   * The original method name. Must match with the actual method name. 
   * 
   * @return
   */
  public String methodName();
}
