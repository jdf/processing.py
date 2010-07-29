package jycessing.build;

import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.util.HashMap;
import java.util.Map;

import processing.core.PGraphics;

public class GenerateDriver {
	public static void main(final String[] args) {
		final Map<String, Binding> bindings = new HashMap<String, Binding>();

		for (final Method m : PGraphics.class.getDeclaredMethods()) {
			if (!Modifier.isPublic(m.getModifiers())) {
				continue;
			}
			final String name = m.getName();
			if (!bindings.containsKey(name)) {
				bindings.put(name, new Binding("locals", name));
			}
			bindings.get(name).add(m);
		}
		for (final Binding b : bindings.values()) {
			System.out.println(b);
		}
	}
}
