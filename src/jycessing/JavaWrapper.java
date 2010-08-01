package jycessing;

import org.python.core.PyObjectDerived;
import org.python.core.PyType;

public class JavaWrapper extends PyObjectDerived {

	public JavaWrapper(final Object k) {
		super(PyType.fromClass(k.getClass(), false));
		javaProxy = k;
	}

}
