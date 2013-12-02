import re

import cog

from java.lang.reflect import Modifier
from java.lang import Class, Void
from processing.core import PApplet


"""
A field is bad if it happens to be marked public in the PApplet source,
but is undocumented or implementation-private.
The "key" field is implemented by hand in the PAppletJythonDriver, since
it's a chimera int/Unicode character.
"""
BAD_FIELD = re.compile(r'''
    ^(
        screen|args|recorder|frame|g|selectedFile|keyEvent|mouseEvent
        |sketchPath|screen(Width|Height)|defaultSize|firstMouse|finished
        |requestImageMax|online|key
    )$
    ''', re.X)

"""
A method is "bad" if either there's already a native python implementation
of it (as in max()) or if it's private to the implementation of PApplet, but
is marked public as a subclass of Component or Applet.
"""
BAD_METHOD = re.compile(r'''
    ^(
    init|handleDraw|draw|parse[A-Z].*|arraycopy|openStream|str|.*Pressed
    |.*Released|(un)?register[A-Z].*|print|setup[A-Z].+|thread
    |(get|set|remove)Cache|update|destroy|main|flush|addListeners|dataFile
    |die|setup|mouseE(ntered|xited)|paint|sketch[A-Z].*|stop|save(File|Path)
    |displayable|method|runSketch|start|focus(Lost|Gained)|(data|create)Path
    |round|abs|max|min|open|append|splice|expand|contract|set|exit|link|param
    |status
    )$
    ''', re.X)


# I don't know of any other way to refer to primitive classes in Jython.
def prim(type_name):
    return Class.forName("java.lang.%s" % type_name).getField("TYPE").get(None)

"""
Here we map from mnemonic type names to the actual Java classes that implement
those types.
"""
PRIMITIVES = { 'int': prim("Integer"),
               'char': prim("Character"),
               'byte': prim("Byte"),
               'long': prim("Long"),
               'double': prim("Double"),
               'float': prim("Float"),
               'boolean': prim("Boolean") }

USELESS_TYPES = (PRIMITIVES['char'], Class.forName('[C'), PRIMITIVES['byte'])

"""
We want to create Jython wrappers for all public methods of PApplet except
those in "BAD_METHOD". Also, if we have both foo(int) and foo(char), we throw
away the char variant, and always call the int variant. Same with foo(byte).
Sadly, Java has no unsigned types, so the distinction is weird.
"""
WANTED_METHODS = [m for m in Class.getDeclaredMethods(PApplet)
                      if Modifier.isPublic(m.getModifiers())
                      and not m.getExceptionTypes()
                      and not BAD_METHOD.match(m.getName())
                      and not any(k in USELESS_TYPES for k in m.getParameterTypes())]

"""
We want to create Jython wrappers for all variables visible during the
Processing runtime.
"""
WANTED_FIELDS = [f for f in Class.getDeclaredFields(PApplet)
                    if Modifier.isPublic(f.getModifiers())
                    and not Modifier.isStatic(f.getModifiers())
                    and not BAD_FIELD.match(f.getName())]


class ClassConversionInfo(object):
    """
    A structure to keep in one place all of the templates for generating
    code for going back and forth between Python and Java.
    """
    def __init__(self, to_python_prefix, to_java_format, typecheck_format):
        self.to_python_prefix = to_python_prefix
        self.to_java_format = to_java_format
        self.typecheck_format = typecheck_format

"""
Map from java types to various expressions needed in code
generation around those types.
"""
CONVERSIONS = {
   PRIMITIVES['int']:
        ClassConversionInfo('new PyInteger', 
                            '%s.asInt()',
                            '%(name)s == PyInteger.TYPE'),
   PRIMITIVES['byte']:
        ClassConversionInfo(None,
                            '(byte)%s.asInt()',
                            '%(name)s == PyInteger.TYPE'),
   PRIMITIVES['float']:
        ClassConversionInfo('new PyFloat',
                            '(float)%s.asDouble()',
                            '(%(name)s == PyFloat.TYPE '
                                '|| %(name)s == PyInteger.TYPE '
                                '|| %(name)s == PyLong.TYPE)'),
   PRIMITIVES['double']:
        ClassConversionInfo('new PyFloat',
                            '%s.asDouble()',
                            '%(name)s == PyFloat.TYPE'),
   PRIMITIVES['long']:
        ClassConversionInfo('new PyLong',
                            '%s.asLong()',
                            '%(name)s == PyLong.TYPE'),
   Class.forName("java.lang.String"):
        ClassConversionInfo('new PyUnicode',
                            '%s.asString()',
                            '(%(name)s == PyString.TYPE'
                                '|| %(name)s == PyUnicode.TYPE)'),
   PRIMITIVES['char']:
        ClassConversionInfo('new PyInteger',
                            '%s.asInt()',
                            None),
   PRIMITIVES['boolean']:
        ClassConversionInfo('new PyBoolean',
                            '%s.__nonzero__()',
                            '%(name)s == PyBoolean.TYPE')
}

def emit_python_prefix(klass):
    try:
        cog.out(CONVERSIONS[klass].to_python_prefix)
    except (KeyError, AttributeError):
        if klass.isPrimitive():
            raise Exception("You need a converter for %s" % klass.getName())
        cog.out('Py.java2py')
    cog.out('(')

def emit_java_expression(klass, name):
    try:
        cog.out(CONVERSIONS[klass].to_java_format % name)
    except KeyError:
        if klass.isPrimitive():
            raise Exception("You need a converter for %s" % klass.getName())
        simpleName = Class.getName(klass)
        if klass.isArray():
            simpleName = Class.getSimpleName(klass)
        if simpleName != 'java.lang.Object':
            cog.out('(%s)' % simpleName)
        cog.out('%s.__tojava__(%s.class)' % (name, simpleName))

def emit_typecheck_expression(klass, name):
    try:
        cog.out(CONVERSIONS[klass].typecheck_format % {'name': name})
    except (TypeError, KeyError):
        if klass.isPrimitive():
            raise Exception("You need a converter for %s" % klass.getName())
        cog.out('%s.getProxyType() != null '
                '&& %s.getProxyType() == %s.class' % (name, 
                                                      name, 
                                                      Class.getSimpleName(klass)))

def is_builtin(name):
    return name in ('map', 'filter', 'set', 'str')


# TODO: replace this insanity with a decent templating system. What was I thinking?

class PolymorphicMethod(object):
    def __init__(self, name, arity):
        self.name = name
        self.arity = arity
        self.methods = []
        
    def add_method(self, m):
        assert len(m.getParameterTypes()) == self.arity
        self.methods.append(m)
    
    def emit_method(self, m):
        if m.getReturnType() is not Void.TYPE:
            cog.out('return ')
            emit_python_prefix(m.getReturnType())
        cog.out('%s(' % self.name)
        for i in range(self.arity):
            if i > 0:
                cog.out(', ')
            emit_java_expression(m.getParameterTypes()[i], 'args[%d]' % i)
        cog.out(')')
        if m.getReturnType() is Void.TYPE:
            cog.outl(';')
            cog.outl('\t\t\t\treturn Py.None;')
        else:
            cog.outl(');')
        
    def emit(self):
        cog.outl('\t\t\tcase %d: {' % self.arity)
        if len(self.methods) == 1 and not is_builtin(self.name):
            cog.out('\t\t\t\t')
            self.emit_method(self.methods[0])
        else:
            for i in range(self.arity):
                cog.outl('\t\t\t\tfinal PyType t%d = args[%d].getType();' % (i, i))
            self.methods.sort(key=lambda p: [m.getSimpleName()
                                             for m in p.getParameterTypes()],
                               reverse=True)
            for i in range(len(self.methods)):
                m = self.methods[i]
                if i > 0:
                    cog.out(' else ')
                else:
                    cog.out('\t\t\t\t')
                if self.arity > 0:
                    cog.out('if (')
                    for j in range(self.arity):
                        if j > 0:
                            cog.out(' && ')
                        emit_typecheck_expression(m.getParameterTypes()[j], 
                                                  't%d' % j)
                    cog.out(') {\n\t\t\t\t\t')
                self.emit_method(m)
                if self.arity > 0:
                    cog.out('\t\t\t\t}') 
            if is_builtin(self.name):
                cog.outl(' else { return %s_builtin.__call__(args, kws); }' % self.name)
            elif self.arity > 0:
                cog.outl(' else { throw new UnexpectedInvocationError'
                         '("%s", args, kws); }' % self.name)  
        cog.outl('\t\t\t}')
                

class Binding(object):
    def __init__(self, name):
        self.name = name
        self.field = None
        self.methods = {}

    def add_method(self, m):
        arity = len(m.getParameterTypes())
        pm = self.methods.setdefault(arity, PolymorphicMethod(self.name, arity))
        pm.add_method(m)
    
    def set_field(self, f):
        if self.field:
            raise Exception("Binding %s's field was already set!" % self.name)
        self.field = f
    
    def emit(self):
        has_methods = len(self.methods.values()) > 0
        n = self.name
        if is_builtin(n):
            cog.outl('final PyObject %s_builtin = builtins.__getitem__("%s");' % (n, n))
        cog.out('builtins.__setitem__("%s",' % n)
        if self.field:
            emit_python_prefix(self.field.getType())
            cog.out('%s)' % n)
        else:
            cog.out('new PyObject()')
        if has_methods:
            cog.outl('{')
        if has_methods:
            cog.outl('\tpublic PyObject __call__(final PyObject[] args, final String[] kws) {')
            cog.outl('\t\tswitch(args.length) {')
            cog.outl('\t\t\tdefault: ');
            cog.out('\t\t\t\t')
            if is_builtin(n):
                cog.outl('return %s_builtin.__call__(args, kws);' % n)
            else:
                cog.outl('throw new RuntimeException("Can\'t call \\"%s\\" with "'
                         ' + args.length + " parameters."); ' % n)
            for k in sorted(self.methods.keys()):
                self.methods[k].emit()
            cog.outl('\t\t}\n\t}')
        if has_methods:
            cog.out('}')
        cog.outl(');')

bindings = {}
for m in WANTED_METHODS:
    bindings.setdefault(m.getName(), Binding(m.getName())).add_method(m)

simple_method_bindings = [b for b in bindings.values() if not b.field]
