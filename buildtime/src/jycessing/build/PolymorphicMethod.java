/*
 * Copyright 2010 Jonathan Feinberg
 * 
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License. You may obtain a copy of
 * the License at
 * 
 * http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations under
 * the License.
 */
package jycessing.build;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

public class PolymorphicMethod {
    private final String name;
    private final int arity;
    private final List<Method> methods = new ArrayList<Method>();
    private final boolean isPythonBuiltin;

    public PolymorphicMethod(final String name, final int arity,
            final boolean isPythonBuiltin) {
        this.name = name;
        this.arity = arity;
        this.isPythonBuiltin = isPythonBuiltin;
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
        methods.add(method);
    }

    public String toString() {
        final StringBuilder sb = new StringBuilder();
        sb.append(String.format("\t\t\tcase %d: {\n", arity));
        if (!isPythonBuiltin && methods.size() == 1) {
            sb.append("\t\t\t\t");
            append(methods.get(0), sb);
        } else {
            for (int i = 0; i < arity; i++) {
                final String typeTemp = "\t\t\t\tfinal PyType t%d = args[%d].getType();\n";
                sb.append(String.format(typeTemp, i, i));
            }
            Collections.sort(methods, METHOD_COMPARATOR);
            for (int i = 0; i < methods.size(); i++) {
                final Method m = methods.get(i);
                if (i > 0) {
                    sb.append(" else ");
                } else {
                    sb.append("\t\t\t\t");
                }
                if (arity > 0) {
                    sb.append("if (");
                    for (int j = 0; j < arity; j++) {
                        if (j > 0) {
                            sb.append(" && ");
                        }
                        final String typeExpr = String.format("t%d", j);
                        sb.append(getTypecheckExpression(
                                m.getParameterTypes()[j], typeExpr));
                    }
                    sb.append(") {\n\t\t\t\t\t");
                }
                append(m, sb);
                if (arity > 0) {
                    sb.append("\t\t\t\t}");
                }
            }
            if (isPythonBuiltin) {
                sb.append(" else { return ").append(name)
                        .append("_builtin.__call__(args, kws); }\n");
            } else if (arity > 0) {
                sb.append(" else { throw new UnexpectedInvocationError(\"");
                sb.append(name);
                sb.append("\", args, kws); }\n");
            }
        }
        sb.append("\t\t\t}\n");
        return sb.toString();
    }

    private void append(final Method m, final StringBuilder sb) {
        if (m.getReturnType() != Void.TYPE) {
            final String prefix = TypeUtil.pyConversionPrefix(m
                    .getReturnType());
            sb.append("return ").append(prefix);
        }
        sb.append(name).append('(');
        for (int i = 0; i < arity; i++) {
            if (i > 0) {
                sb.append(", ");
            }
            sb.append(asJavaExpression(m, i));
        }
        sb.append(')');
        if (m.getReturnType() == Void.TYPE) {
            sb.append(";\n");
            sb.append("\t\t\t\treturn Py.None;");
        } else {
            sb.append(");");
        }
        sb.append('\n');
    }

    public static String asJavaExpression(final Method signature, final int i) {
        final String name = "args[" + i + "]";
        final Class<?> javaType = signature.getParameterTypes()[i];
        final StringBuilder sb = new StringBuilder();
        if (javaType == float.class) {
            sb.append("(float)").append(name).append(".asDouble()");
        } else if (javaType == int.class) {
            sb.append(name).append(".asInt()");
        } else if (javaType == String.class) {
            sb.append(name).append(".asString()");
        } else if (javaType == char.class) {
            sb.append(name).append(".asString().charAt(0)");
        } else if (javaType == long.class) {
            sb.append(name).append(".asLong()");
        } else if (javaType == byte.class) {
            sb.append("(byte)").append(name).append(".asInt()");
        } else if (javaType == boolean.class) {
            sb.append(name).append(".__nonzero__()");
        } else if (javaType.isPrimitive()) {
            throw new RuntimeException("You need a converter for " + javaType);
        } else {
            final String simpleName = javaType.isArray() ? javaType
                    .getSimpleName() : javaType.getName();
            // no need to cast Object to Object
            if (!simpleName.equals("java.lang.Object")) {
                sb.append('(').append(simpleName).append(')');
            }
            sb.append(name).append(".__tojava__(").append(simpleName)
                    .append(".class)");
        }
        return sb.toString();
    }

    public String getTypecheckExpression(final Class<?> k, final String name) {
        if (k == float.class) {
            return String
                    .format("(%s == PyFloat.TYPE || %s == PyInteger.TYPE || %s == PyLong.TYPE)",
                            name, name, name);
        } else if (k == int.class || k == byte.class) {
            return String.format("%s == PyInteger.TYPE", name);
        } else if (k == boolean.class) {
            return String.format("%s == PyBoolean.TYPE", name);
        } else if (k == String.class) {
            return String.format("%s == PyString.TYPE", name);
        } else if (k.isPrimitive()) {
            throw new RuntimeException("You need a converter for " + k);
        } else {
            return String
                    .format("%s.getProxyType() != null && %s.getProxyType() == %s.class",
                            name, name, k.getSimpleName());
        }
    }

    private static final Comparator<Method> METHOD_COMPARATOR = new Comparator<Method>() {
        private final Comparator<Class<?>> CLASS_COMP = new Comparator<Class<?>>() {
            public int compare(final Class<?> a, final Class<?> b) {
                if (a == int.class && b == float.class) {
                    return -1;
                }
                if (a == float.class && b == int.class) {
                    return 1;
                }
                return a.getSimpleName().compareTo(b.getSimpleName());
            }
        };
        public int compare(Method a, Method b) {
            final Class<?>[] atypes = a.getParameterTypes();
            final Class<?>[] btypes = b.getParameterTypes();
            if (atypes.length != btypes.length) {
                throw new IllegalArgumentException(
                        "Can't compare Methods of unlike arity");
            }
            for (int i = 0; i < atypes.length; i++) {
                final int c = CLASS_COMP.compare(atypes[i], btypes[i]);
                if (c != 0) {
                    return c;
                }
            }
            return 0;
        }
    };
}
