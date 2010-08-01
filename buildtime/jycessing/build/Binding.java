package jycessing.build;

import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.util.ArrayList;

public class Binding {
	private final String name;
	private final ArrayList<PolymorphicMethod> methods = new ArrayList<PolymorphicMethod>();
	private Global global = null;

	public Binding(final String interpreterName, final String name) {
		this.name = name;
	}

	public String toString() {
		final StringBuilder sb = new StringBuilder();
		sb.append("builtins.__setitem__(\"").append(name).append("\", ");
		sb.append(global == null ? "new PyObject() {" : global.getInitializerPrefix());
		if (methods.size() > 0) {
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
		}
		if (global != null) {
			sb.append(global.getBody());
		}
		sb.append("}");
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

	public void add(final Field f) {
		global = new Global(f);
	}
}
