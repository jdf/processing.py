package jycessing.build;

public class Binding {
	private final String localsName;
	private final String name;

	public Binding(final String localsName, final String name) {
		this.name = name;
		this.localsName = localsName;
	}

	public String toString() {
		final StringBuilder sb = new StringBuilder();
		sb.append(localsName).append(".__setitem__(\"").append(name).append(
				"\", new PyObject() {\n");

		sb.append("});\n");
		return sb.toString();
	}
}
