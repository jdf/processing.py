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
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;

public class Signature implements Comparable<Signature> {
    private static final Comparator<Class<?>> CLASS_COMP = new Comparator<Class<?>>() {
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

    public int compareTo(final Signature o) {
        if (argTypes.size() != o.argTypes.size()) {
            throw new IllegalArgumentException("Can't compare Signatures of unlike size");
        }
        for (int i = 0; i < argTypes.size(); i++) {
            final int c = CLASS_COMP.compare(argTypes.get(i), o.argTypes.get(i));
            if (c != 0) {
                return c;
            }
        }
        return 0;
    }

    private final List<Class<?>> argTypes;
    private final Class<?> returnType;

    public Signature(final Method method) {
        argTypes = Arrays.asList(method.getParameterTypes());
        returnType = method.getReturnType();
    }

    public boolean isVoid() {
        return returnType == Void.TYPE;
    }

    public String getTypecheckExpression(final int i, final String name) {
        final Class<?> k = argTypes.get(i);
        if (k == float.class) {
            return String.format(
                    "(%s == PyFloat.TYPE || %s == PyInteger.TYPE)", name, name);
        } else if (k == int.class || k == byte.class) {
            return String.format("%s == PyInteger.TYPE", name);
        } else if (k == boolean.class) {
            return String.format("%s == PyBoolean.TYPE", name);
        } else if (k == String.class) {
            return String.format("%s == PyString.TYPE", name);
        } else if (k.isPrimitive()) {
            throw new RuntimeException("You need a converter for " + k);
        } else {
            return String.format(
                    "%s.getProxyType() != null && %s.getProxyType() == %s.class", name,
                    name, k.getSimpleName());
        }
    }

    public List<Class<?>> getArgTypes() {
        return argTypes;
    }

    public Class<?> getReturnType() {
        return returnType;
    }

}
