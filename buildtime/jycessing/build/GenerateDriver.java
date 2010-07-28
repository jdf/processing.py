package jycessing.build;

import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;

import processing.core.PGraphics;

public class GenerateDriver {
	public static void main(final String[] args) {
		Map<String, ArrayList<PolymorphicMethod>> methods = new HashMap<String, ArrayList<PolymorphicMethod>>();

		for (final Method m : PGraphics.class.getDeclaredMethods()) {
			if (!Modifier.isPublic(m.getModifiers())) {
				continue;
			}
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
