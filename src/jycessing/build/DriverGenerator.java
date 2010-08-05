package jycessing.build;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Reader;
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
	final String BAD_METHOD = "^(init|handleDraw|draw|parse[A-Z].*|arraycopy|openStream)$";

	private static final Set<String> BAD_FIELDS = new HashSet<String>(Arrays.asList(
			"screen", "args", "recorder", "frame", "g", "selectedFile", "keyEvent",
			"mouseEvent", "sketchPath", "screenWidth", "screenHeight", "defaultSize",
			"firstMouse", "finished", "requestImageMax"));

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
		for (final Method m : PApplet.class.getDeclaredMethods()) {
			maybeAdd(m);
		}
		for (final Field f : PApplet.class.getDeclaredFields()) {
			maybeAdd(f);
		}
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
		findOrCreateBinding(name).setField(f);
	}

	public String getMethodBindings() {
		final StringBuilder sb = new StringBuilder();
		for (final Binding b : bindings.values()) {
			if (!b.hasGlobal()) {
				sb.append(b.toString());
			}
		}
		return sb.toString();
	}

	public String getFieldBindings() {
		final StringBuilder sb = new StringBuilder();
		for (final Binding b : bindings.values()) {
			if (b.hasGlobal()) {
				sb.append(b.toString());
			}
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
		final String withMethodBindings = template.replace("%METHOD_BINDINGS%", gen
				.getMethodBindings());
		final String withFieldBindings = withMethodBindings.replace("%FIELD_BINDINGS%", gen
				.getFieldBindings());

		final FileWriter out = new FileWriter("generated/jycessing/DriverImpl.java");
		out.write(withFieldBindings);
		out.close();
	}
}
