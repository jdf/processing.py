package jycessing.build;

import java.lang.reflect.Field;

public class Global {
	private final Field field;

	public Global(final Field field) {
		this.field = field;
	}

	public String toString() {
		final StringBuilder sb = new StringBuilder();
		final Class<?> k = field.getType();
		if (k == int.class || k == long.class || k == float.class || k == double.class) {
			sb.append("\tpublic PyFloat __float__() {\n");
			sb.append(String.format("\t\treturn new PyFloat(%s);\n", field.getName()));
			sb.append("\t}\n\n");
			sb.append("\tpublic PyObject __int__() {\n");
			sb.append(String.format("\t\treturn new PyInteger((int)%s);\n", field.getName()));
			sb.append("\t}\n\n");
			sb.append("\tpublic PyObject __long__() {\n");
			sb.append(String.format("\t\treturn new PyLong((long)%s);\n", field.getName()));
			sb.append("\t}\n\n");
		} else if (k == boolean.class) {
			sb.append("\tpublic boolean __nonzero__() {\n");
			sb.append(String.format("\t\treturn %s;\n", field.getName()));
			sb.append("\t}\n\n");
		} else if (k == char.class) {
			// noop
		} else if (k.isPrimitive()) {
			throw new RuntimeException("You've got to put in a converter for field "
					+ field.getName() + " of type " + k);
		} else {
			sb.append("\tpublic Object __tojava__(Class<?> c) {\n");
			sb.append(String.format("\t\treturn %s;\n", field.getName()));
			sb.append("\t}\n\n");
		}
		sb.append("\tpublic PyString __repr__() {\n");
		sb.append(String.format("\t\treturn new PyString(String.valueOf(%s));\n", field
				.getName()));
		sb.append("\t}\n\n");
		return sb.toString();
	}
}