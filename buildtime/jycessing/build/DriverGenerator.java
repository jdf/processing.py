package jycessing.build;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Reader;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import processing.core.PApplet;

@SuppressWarnings("serial")
public class DriverGenerator {
	final String BAD_METHOD = "^(init|handleDraw|draw|parse[A-Z].*)$";

	private static final Set<String> BAD_FIELDS = new HashSet<String>(Arrays.asList(
			"screen", "args", "recorder"));

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
	final List<Field> nonPrimitives = new ArrayList<Field>();

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
		if (!Modifier.isPublic(mods) || !PolymorphicMethod.shouldAdd(m)
				|| name.matches(BAD_METHOD) || !ALL_APPLET_METHODS.contains(name)) {
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
		if (f.getType() == char.class || !f.getType().isPrimitive()) {
			nonPrimitives.add(f);
		} else {
			findOrCreateBinding(name).add(f);
		}
	}

	public String getBindings() {
		for (final Method m : PApplet.class.getDeclaredMethods()) {
			maybeAdd(m);
		}
		for (final Field f : PApplet.class.getDeclaredFields()) {
			maybeAdd(f);
		}
		final StringBuilder sb = new StringBuilder();
		for (final Binding b : bindings.values()) {
			sb.append(b.toString());
		}
		return sb.toString();
	}

	public static String getText(final Reader r) throws IOException {
		final BufferedReader reader = new BufferedReader(r);
		final StringBuilder sb = new StringBuilder();
		String line;
		try {
			while ((line = reader.readLine()) != null) {
				sb.append(line).append("\n");
			}
			return sb.toString();
		} finally {
			reader.close();
		}
	}

	public static void main(final String[] args) throws Exception {
		final DriverGenerator gen = new DriverGenerator();

		final String template = getText(new FileReader("template/DriverImpl.java"));
		final String bindings = gen.getBindings();
		final String withBindings = template.replace("%BINDINGS%", bindings);

		final FileWriter out = new FileWriter("generated/jycessing/DriverImpl.java");
		out.write(withBindings);
		out.close();
	}
}
