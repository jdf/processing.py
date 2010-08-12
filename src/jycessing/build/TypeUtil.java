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

public class TypeUtil {
    public static String pyConversionPrefix(final Class<?> k) {
        if (k == float.class) {
            return "new PyFloat(";
        } else if (k == int.class) {
            return "new PyInteger(";
        } else if (k == long.class) {
            return "new PyLong(";
        } else if (k == String.class || k == char.class) {
            return "new PyString(";
        } else if (k == boolean.class) {
            return "new PyBoolean(";
        } else if (k.isPrimitive()) {
            throw new RuntimeException("You need a converter for " + k);
        } else {
            return "Py.java2py(";
        }
    }
}
