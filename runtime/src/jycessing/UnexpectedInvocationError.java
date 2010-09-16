package jycessing;

import org.python.core.PyObject;

public class UnexpectedInvocationError extends RuntimeException {
    private static String buildMessage(final String name, final PyObject[] args,
                                       final String[] kws) {
        final StringBuilder sb = new StringBuilder();
        sb.append("I don't know how to handle a call to ");
        sb.append(name).append('(');
        for (int i = 0; i < args.length; i++) {
            if (i > 0) {
                sb.append(", ");
            }
            sb.append(args[i].getType());
        }
        sb.append("\n");
        sb.append("If ").append('"').append(name).append('"');
        sb.append(" is a Python builtin, please report this to ");
        sb.append("the processing.py project as a bug!");
        return sb.toString();
    }

    public UnexpectedInvocationError(final String name, final PyObject[] args,
                                     final String[] kws) {
        super(buildMessage(name, args, kws));
    }
}
