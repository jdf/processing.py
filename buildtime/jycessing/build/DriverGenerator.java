package jycessing.build;

import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import processing.core.PApplet;

@SuppressWarnings("serial")
public class DriverGenerator {
	private static final String[] APPLET_OWNED_METHODS = new String[] { "loadFont", "size",
			"frameRate", "sin", "cos", "tan", "sqrt", "millis" };

	private static final Set<String> BAD_METHODS = new HashSet<String>(Arrays
			.asList("init"));

	private static final Set<String> BAD_FIELDS = new HashSet<String>(Arrays
			.asList("screen"));

	private static final Set<String> ALL_APPLET_METHODS = Collections
			.unmodifiableSet(new HashSet<String>() {
				{
					for (final Method m : PApplet.class.getDeclaredMethods()) {
						if (!Modifier.isPublic(m.getModifiers())) {
							continue;
						}
						add(m.getName());
					}
				}
			});

	final Map<String, Binding> bindings = new HashMap<String, Binding>();

	public DriverGenerator() {
	}

	private Binding findOrCreateBinding(final String name) {
		if (!bindings.containsKey(name)) {
			bindings.put(name, new Binding("interp", name));
		}
		return bindings.get(name);
	}

	private void maybeAdd(final Method m) {
		final String name = m.getName();
		final int mods = m.getModifiers();
		if (!Modifier.isPublic(mods) || Modifier.isStatic(mods)
				|| !PolymorphicMethod.shouldAdd(m) || BAD_METHODS.contains(name)
				|| !ALL_APPLET_METHODS.contains(name)) {
			return;
		}
		findOrCreateBinding(name).add(m);
	}

	private void maybeAdd(final Field f) {
		final String name = f.getName();
		final int mods = f.getModifiers();
		if (!Modifier.isPublic(mods) || Modifier.isStatic(mods) || BAD_FIELDS.contains(name)) {
			return;
		}
		findOrCreateBinding(name).add(f);
	}

	public void generateDriver() {
		for (final Method m : PApplet.class.getDeclaredMethods()) {
			maybeAdd(m);
		}
		for (final Field f : PApplet.class.getDeclaredFields()) {
			maybeAdd(f);
		}
		for (final Binding b : bindings.values()) {
			System.out.println(b);
		}

	}

	public static void main(final String[] args) {
		new DriverGenerator().generateDriver();
	}
}
