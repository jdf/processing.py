package jycessing.build;

import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.util.ArrayList;

public class Binding {
	private final String name;
	private final ArrayList<PolymorphicMethod> methods = new ArrayList<PolymorphicMethod>();
	private Field global = null;

	public Binding(final String interpreterName, final String name) {
		this.name = name;
	}

	public boolean hasGlobal() {
		return global != null;
	}

	public String toString() {
		final boolean hasMethods = methods.size() > 0;

		final StringBuilder sb = new StringBuilder();
		sb.append(String.format("builtins.__setitem__(\"%s\", ", name));
		if (hasGlobal()) {
			sb.append(TypeUtil.pyConversionPrefix(global.getType()));
			sb.append(global.getName());
			sb.append(")");
		} else {
			sb.append("new PyObject()");
		}
		if (hasMethods) {
			sb.append("{");
			sb
					.append("\tpublic PyObject __call__(final PyObject[] args, final String[] kws) {\n");
			sb.append("\t\tswitch(args.length) {\n");
			sb.append("\t\t\tdefault: throw new RuntimeException(\"");
			sb.append(String.format(
					"Can't call \\\"%s\\\" with \" + args.length + \" parameters.", name));
			sb.append("\");\n");
			for (final PolymorphicMethod m : methods) {
				if (m == null) {
					continue;
				}
				sb.append(m.toString());
			}
			sb.append("\t\t}\n\t}\n");
			sb.append("}");
		}
		sb.append(");\n");

		return sb.toString();
	}

	public void add(final Method m) {
		final int arity = m.getParameterTypes().length;
		if (methods.size() < arity + 1) {
			for (int i = methods.size(); i < arity + 1; i++) {
				methods.add(null);
			}
		}
		if (methods.get(arity) == null) {
			methods.set(arity, new PolymorphicMethod(name, arity));
		}
		methods.get(arity).add(m);
	}

	public void setField(final Field f) {
		if (global != null) {
			throw new IllegalStateException("Binding " + name + "'s global was already set!");
		}
		global = f;
	}
}
