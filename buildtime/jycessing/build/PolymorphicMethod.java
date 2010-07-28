package jycessing.build;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

import processing.core.PApplet;

public class PolymorphicMethod {
	private final String name;
	private final int arity;
	private final List<Signature> signatures = new ArrayList<Signature>();

	public PolymorphicMethod(final String name, final int arity) {
		this.name = name;
		this.arity = arity;
	}

	public void add(final Method method) {
		if (method.getParameterTypes().length != arity) {
			throw new IllegalArgumentException("I expect methods with " + arity
					+ " args, but got " + method);
		}
		signatures.add(new Signature(method));
	}

	public String toString() {
		final StringBuilder sb = new StringBuilder();
		sb.append("public PyObject __call__(");
		for (int i = 0; i < arity; i++) {
			if (i > 0) {
				sb.append(", ");
			}
			sb.append("final PyObject arg").append(i);
		}
		sb.append(") {\n");
		if (signatures.size() == 1) {
			sb.append("\t");
			append(signatures.get(0), sb);
		} else {
			for (int i = 0; i < arity; i++) {
				sb.append(String.format("\tfinal PyType t%d = arg%d.getType();\n", i, i));
			}
			for (int i = 0; i < signatures.size(); i++) {
				final Signature sig = signatures.get(i);
				if (i > 0) {
					sb.append(" else ");
				} else {
					sb.append('\t');
				}
				sb.append("if (");
				for (int j = 0; j < arity; j++) {
					if (j > 0) {
						sb.append(" && ");
					}
					sb.append(sig.getTypecheckExpression(j, "t" + j));
				}
				sb.append(") {\n\t\t");
				append(sig, sb);
				sb.append("\n\t}");
			}
			sb
					.append(" else { throw new IllegalArgumentException(\"Couldn't figure out which \\\"");
			sb.append(name);
			sb.append("\\\" to call.\"); }");
		}
		sb.append("\n};\n");
		return sb.toString();
	}

	private void append(final Signature signature, final StringBuilder sb) {
		if (!signature.isVoid()) {
			sb.append("return ").append(TypeUtil.pyConversionPrefix(signature.getReturnType()));
		}
		sb.append(name).append('(');
		for (int i = 0; i < arity; i++) {
			if (i > 0) {
				sb.append(", ");
			}
			sb.append(TypeUtil.asJavaExpression("arg" + i, signature.getArgTypes().get(i)));
		}
		sb.append(')');
		if (signature.isVoid()) {
			sb.append(";\n");
			sb.append("\t\treturn Py.None;");
		} else {
			sb.append(");");
		}
	}

	public static void main(final String[] args) {
		Map<String, ArrayList<PolymorphicMethod>> methods = new HashMap<String, ArrayList<PolymorphicMethod>>();

		for (final Method m : PApplet.class.getDeclaredMethods()) {
			final String name = m.getName();
			if (!methods.containsKey(name)) {
				methods.put(name, new ArrayList<PolymorphicMethod>());
			}
			final ArrayList<PolymorphicMethod> pms = methods.get(name);
			final int arity = m.getParameterTypes().length;
			if (pms.size() < arity + 1) {
				for (int i = pms.size(); i < arity + 1; i++) {
					pms.add(null);
				}
			}
			if (pms.get(arity) == null) {
				pms.set(arity, new PolymorphicMethod(name, arity));
			}
			final PolymorphicMethod pm = pms.get(arity);
			pm.add(m);
		}
		for (final Entry<String, ArrayList<PolymorphicMethod>> e : methods.entrySet()) {
			System.out.println("---------------" + e.getKey());
			for (final PolymorphicMethod m : e.getValue()) {
				if (m != null) {
					System.out.println(m);
				}
			}
		}
	}
}
