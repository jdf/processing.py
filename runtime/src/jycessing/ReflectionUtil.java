package jycessing;

import java.lang.reflect.Field;

public class ReflectionUtil {
  public static Field accessibleField(final Class<?> c, final String fieldName) {
    try {
      final Field field = c.getDeclaredField(fieldName);
      field.setAccessible(true);
      return field;
    } catch (final Exception e) {
      throw new RuntimeException(e);
    }
  }

  public static <T> void setObjectStatic(final Class<T> klass, final String fieldName,
      final Object value) {
    try {
      accessibleField(klass, fieldName).set(null, value);
    } catch (final Exception e) {
      throw new RuntimeException(e);
    }
  }

  public static <T> void setBooleanStatic(final Class<T> klass, final String fieldName,
      final boolean value) {
    try {
      accessibleField(klass, fieldName).set(null, value);
    } catch (final Exception e) {
      throw new RuntimeException(e);
    }
  }

  public static <T> void setObject(final T instance, final String fieldName, final Object value) {
    try {
      accessibleField(instance.getClass(), fieldName).set(instance, value);
    } catch (final Exception e) {
      throw new RuntimeException(e);
    }
  }

}
