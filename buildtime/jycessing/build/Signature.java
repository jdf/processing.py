package jycessing.build;

import java.lang.reflect.Method;
import java.util.Arrays;
import java.util.List;

public class Signature {
	private final List<Class<?>> argTypes;
	private final Class<?> returnType;

	public Signature(final Method method) {
		argTypes = Arrays.asList(method.getParameterTypes());
		returnType = method.getReturnType();
	}

	public boolean isVoid() {
		return returnType == Void.TYPE;
	}

	public String getTypecheckExpression(final int i, final String name) {
		final Class<?> k = argTypes.get(i);
		if (k == float.class) {
			return String.format("%s == PyFloat.TYPE", name);
		} else if (k == int.class || k == byte.class) {
			return String.format("%s == PyInteger.TYPE", name);
		} else if (k == boolean.class) {
			return String.format("%s == PyBoolean.TYPE", name);
		} else if (k == String.class) {
			return String.format("%s == PyString.TYPE", name);
		} else if (k.isPrimitive()) {
			throw new RuntimeException("You need a converter for " + k);
		} else {
			return String.format("%s.getProxyType() != null && %s.getProxyType() == %s.class",
					name, name, k.getSimpleName());
		}
	}

	public List<Class<?>> getArgTypes() {
		return argTypes;
	}

	public Class<?> getReturnType() {
		return returnType;
	}

}
