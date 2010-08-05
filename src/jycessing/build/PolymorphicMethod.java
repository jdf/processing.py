package jycessing.build;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class PolymorphicMethod {
	private final String name;
	private final int arity;
	private final List<Signature> signatures = new ArrayList<Signature>();

	public PolymorphicMethod(final String name, final int arity) {
		this.name = name;
		this.arity = arity;
	}

	public static boolean shouldAdd(final Method method) {
		final Class<?>[] types = method.getParameterTypes();
		for (final Class<?> k : types) {
			if (k == char.class || k == char[].class) {
				return false;
			}
		}
		return true;
	}

	public void add(final Method method) {
		final Class<?>[] types = method.getParameterTypes();
		if (types.length != arity) {
			throw new IllegalArgumentException("I expect methods with " + arity
					+ " args, but got " + method);
		}
		if (!shouldAdd(method)) {
			throw new IllegalArgumentException("I can't cope with " + method
					+ " because it's evil.");
		}
		signatures.add(new Signature(method));
	}

	public String toString() {
		final StringBuilder sb = new StringBuilder();
		sb.append(String.format("\t\t\tcase %d: {\n", arity));
		if (signatures.size() == 1) {
			sb.append("\t\t\t\t");
			append(signatures.get(0), sb);
		} else {
			for (int i = 0; i < arity; i++) {
				final String typeTemp = "\t\t\t\tfinal PyType t%d = args[%d].getType();\n";
				sb.append(String.format(typeTemp, i, i));
			}
			Collections.sort(signatures);
			for (int i = 0; i < signatures.size(); i++) {
				final Signature sig = signatures.get(i);
				if (i > 0) {
					sb.append(" else ");
				} else {
					sb.append("\t\t\t\t");
				}
				sb.append("if (");
				for (int j = 0; j < arity; j++) {
					if (j > 0) {
						sb.append(" && ");
					}
					final String typeExpr = String.format("t%d", j);
					sb.append(sig.getTypecheckExpression(j, typeExpr));
				}
				sb.append(") {\n\t\t\t\t\t");
				append(sig, sb);
				sb.append("\t\t\t\t}");
			}
			sb
					.append(" else { throw new IllegalArgumentException(\"Couldn't figure out which \\\"");
			sb.append(name);
			sb.append("\\\" to call.\"); }\n");
		}
		sb.append("\t\t\t}\n");
		return sb.toString();
	}

	private void append(final Signature signature, final StringBuilder sb) {
		if (!signature.isVoid()) {
			final String prefix = TypeUtil.pyConversionPrefix(signature.getReturnType());
			sb.append("return ").append(prefix);
		}
		sb.append(name).append('(');
		for (int i = 0; i < arity; i++) {
			if (i > 0) {
				sb.append(", ");
			}
			sb.append(TypeUtil.asJavaExpression("args[" + i + "]", signature.getArgTypes().get(
					i)));
		}
		sb.append(')');
		if (signature.isVoid()) {
			sb.append(";\n");
			sb.append("\t\t\t\treturn Py.None;");
		} else {
			sb.append(");");
		}
		sb.append('\n');
	}

}
