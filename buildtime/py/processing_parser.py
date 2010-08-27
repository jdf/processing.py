import re

import cog

from java.lang.reflect import Modifier
from java.lang import Class, Void
from processing.core import PApplet


BAD_FIELD = re.compile(r'''
    ^(
        screen|args|recorder|frame|g|selectedFile|keyEvent|mouseEvent
        |sketchPath|screen(Width|Height)|defaultSize|firstMouse|finished
        |requestImageMax
    )$
    ''', re.X)


BAD_METHOD = re.compile(r'''
    ^(
    init|handleDraw|draw|parse[A-Z].*|arraycopy|openStream|str|.*Pressed
    |.*Released|(un)?register[A-Z].*|print(ln)?|setup[A-Z].+|thread
    |(get|set|remove)Cache|update|destroy|main|flush|addListeners|dataFile
    |die|setup|mouseE(ntered|xited)|paint|sketch[A-Z].*|stop|save(File|Path)
    |displayable|method|runSketch|start|focus(Lost|Gained)|(data|create)Path
    |round|abs|max|min|open|append|splice|expand|contract
    )$
    ''', re.X)


# I don't know of any other way to refer to primitive classes in Jython.
prim = lambda(type_name): Class.forName(type_name).getField("TYPE").get(None)
PRIMITIVES = { 'int': prim("java.lang.Integer"),
               'char': prim("java.lang.Character"),
               'byte': prim("java.lang.Byte"),
               'long': prim("java.lang.Long"),
               'double': prim("java.lang.Double"),
               'float': prim("java.lang.Float"),
               'boolean': prim("java.lang.Boolean") }

USELESS_TYPES = (PRIMITIVES['char'], Class.forName('[C'), PRIMITIVES['byte'])
WANTED_METHODS = [m for m in Class.getDeclaredMethods(PApplet)
                      if Modifier.isPublic(m.getModifiers())
                      and not BAD_METHOD.match(m.getName())
                      and not any(k in USELESS_TYPES for k in m.getParameterTypes())]

WANTED_FIELDS = [f for f in Class.getDeclaredFields(PApplet)
                    if Modifier.isPublic(f.getModifiers())
                    and not Modifier.isStatic(f.getModifiers())
                    and not BAD_FIELD.match(f.getName())]

class ClassConversionInfo(object):
    def __init__(self, to_python_prefix, to_java_format, typecheck_format):
        self.to_python_prefix = to_python_prefix
        self.to_java_format = to_java_format
        self.typecheck_format = typecheck_format

"""
    Mapping from java type to various expressions needed in code
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
   PRIMITIVES['long']:
        ClassConversionInfo('new PyLong',
                            '%s.asLong()',
                            None),
   Class.forName("java.lang.String"):
        ClassConversionInfo('new PyString',
                            '%s.asString()',
                            '%(name)s == PyString.TYPE'),
   PRIMITIVES['char']:
        ClassConversionInfo('new PyString',
                            '%s.asString().charAt(0)',
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
        is_wrapped_integer = self.field and self.field.getType() == PRIMITIVES['int']
        n = self.name
        if is_builtin(n):
            cog.outl('final PyObject %s_builtin = builtins.__getitem__("%s");' % (n, n))
        cog.out('builtins.__setitem__("%s",' % n)
        if self.field:
            if is_wrapped_integer:
                cog.out('new WrappedInteger()')
            else:
                emit_python_prefix(self.field.getType())
                cog.out('%s)' % n)
        else:
            cog.out('new PyObject()')
        if has_methods or is_wrapped_integer:
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
        if is_wrapped_integer:
            cog.outl('\tpublic int getValue() { return %s; }' % n)
        if has_methods or is_wrapped_integer:
            cog.out('}')
        cog.outl(');')

bindings = {}
for m in WANTED_METHODS:
    bindings.setdefault(m.getName(), Binding(m.getName())).add_method(m)
for f in WANTED_FIELDS:
    bindings.setdefault(f.getName(), Binding(f.getName())).set_field(f)

simple_method_bindings = [b for b in bindings.values() if not b.field]
integer_field_bindings = [b for b in bindings.values() 
                          if b.field 
                          and b.field.getType() is PRIMITIVES['int']]
field_bindings = [b for b in bindings.values()
                  if b.field
                  and b.field.getType() is not PRIMITIVES['int']]
