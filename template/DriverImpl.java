package jycessing;

import org.python.util.InteractiveConsole;
import org.python.util.PythonInterpreter;
import org.python.core.*;
import processing.core.*;
import java.io.*;

@SuppressWarnings("serial")
public class DriverImpl extends PAppletJythonDriver {

	public DriverImpl(final InteractiveConsole interp, final String programText) {
		super(interp, programText);
	}
	@Override
	protected void populateBuiltins() {
		%METHOD_BINDINGS%
	}

	@Override
	protected void setFields() {
		%FIELD_BINDINGS%
	}

}
