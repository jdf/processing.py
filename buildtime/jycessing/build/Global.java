package jycessing.build;

import java.lang.reflect.Field;

public class Global {
	private final Field field;

	public Global(final Field field) {
		this.field = field;
	}

	public String getInitializerPrefix() {
		final Class<?> k = field.getType();
		if (k == int.class) {
			return "new PyInteger(0) {";
		} else if (k == char.class) {
			// noop
		} else if (k == long.class) {
			return "new PyLong(0) {";
		} else if (k == float.class || k == double.class) {
			return "new PyFloat(0f) {";
		} else if (k == boolean.class) {
			return "new PyBoolean(false) {";
		} else if (k.isPrimitive()) {
			throw new RuntimeException("You've got to put in a converter for field "
					+ field.getName() + " of type " + k);
		}
		return "new JavaWrapper(" + field.getName() + ") {";
	}

	public String getBody() {
		final Class<?> k = field.getType();
		final String name = field.getName();
		if (k == int.class) {
			return String.format("\tpublic int getValue() { return %s; }\n", name);
		} else if (k == long.class) {
			return String.format(
					"\tpublic BigInteger getValue() { return BigInteger.valueOf(%s); }\n", name);
		} else if (k == float.class || k == double.class) {
			return String.format("\tpublic double getValue() { return %s; }\n", name);
		} else if (k == boolean.class) {
			return String.format("\tpublic int getValue() { return %s ? 1 : 0; }\n", name);
		} else if (k == char.class || k == String.class) {
			// noop
		} else if (k.isPrimitive()) {
			throw new RuntimeException("You've got to put in a converter for field " + name
					+ " of type " + k);
		}
		return "";
	}
}