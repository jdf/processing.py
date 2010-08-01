package jycessing;

import org.python.util.PythonInterpreter;
import org.python.core.*;
import processing.core.*;
import java.io.*;

@SuppressWarnings("serial")
public class DriverImpl extends PAppletJythonDriver {

	public DriverImpl(final PythonInterpreter interp) {
		super(interp);
	}

	@Override
	protected void populateBuiltins() {
		%BINDINGS%
	}

	@Override
	protected void setNonPrimitives() {
		interp.set("key", key);
		interp.set("keyEvent", keyEvent);
	}

}
