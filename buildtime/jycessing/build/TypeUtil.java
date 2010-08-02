package jycessing.build;

public class TypeUtil {
	public static String asJavaExpression(final String name, final Class<?> javaType) {
		final StringBuilder sb = new StringBuilder();
		if (javaType == float.class) {
			sb.append("(float)").append(name).append(".asDouble()");
		} else if (javaType == int.class) {
			sb.append(name).append(".asInt()");
		} else if (javaType == String.class) {
			sb.append(name).append(".asString()");
		} else if (javaType == char.class) {
			sb.append(name).append(".asString().charAt(0)");
		} else if (javaType == long.class) {
			sb.append(name).append(".asLong()");
		} else if (javaType == byte.class) {
			sb.append("(byte)").append(name).append(".asInt()");
		} else if (javaType == boolean.class) {
			sb.append(name).append(".__nonzero__()");
		} else if (javaType.isPrimitive()) {
			throw new RuntimeException("You need a converter for " + javaType);
		} else {
			final String simpleName = javaType.isArray() ? javaType.getSimpleName() : javaType
					.getName();
			sb.append('(').append(simpleName).append(')').append(name).append(".__tojava__(")
					.append(simpleName).append(".class)");
		}
		return sb.toString();
	}

	public static String pyConversionPrefix(final Class<?> k) {
		if (k == float.class) {
			return "new PyFloat(";
		} else if (k == int.class) {
			return "new PyInteger(";
		} else if (k == long.class) {
			return "new PyLong(";
		} else if (k == String.class || k == char.class) {
			return "new PyString(";
		} else if (k == boolean.class) {
			return "new PyBoolean(";
		} else if (k.isPrimitive()) {
			throw new RuntimeException("You need a converter for " + k);
		} else {
			return "Py.java2py(";
		}
	}
}
