import __builtin__

import re
import cog

from java.lang.reflect import Field, Method, Modifier
from java.lang import Class, String
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
    |(get|set|remove)Cache|max|update|destroy|main|flush|addListeners|dataFile
    |die|setup|mouseE(ntered|xited)|paint|sketch[A-Z].*|stop|save(File|Path)
    |displayable|method|runSketch|start|focus(Lost|Gained)|(data|create)Path
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

CHAR_TYPES = (PRIMITIVES['char'], Class.forName('[C'))
WANTED_METHODS = [m for m in Class.getDeclaredMethods(PApplet)
                      if Modifier.isPublic(m.getModifiers())
                      and not BAD_METHOD.match(m.getName())
                      and not any(k in CHAR_TYPES for k in m.getParameterTypes())]

WANTED_FIELDS = [f for f in Class.getDeclaredFields(PApplet)
                    if Modifier.isPublic(f.getModifiers())
                    and not Modifier.isStatic(f.getModifiers())
                    and not BAD_FIELD.match(f.getName())]

class ClassConversionInfo(object):
    def __init__(self, to_python_prefix, to_java_format, typecheck_format):
        self.to_python_prefix = to_python_prefix
        self.to_java_format = to_java_format
        self.typecheck_format = typecheck_format

CONVERSIONS = {
   PRIMITIVES['int']: ClassConversionInfo('new PyInteger', 
                                          '{0}.asInt()', 
                                          '{0} == PyInteger.TYPE'),
   PRIMITIVES['byte']: ClassConversionInfo('new PyInteger', 
                                           '(byte){0}.asInt()', 
                                           '{0} == PyInteger.TYPE'),
   PRIMITIVES['float']: ClassConversionInfo('new PyFloat', 
                                            '(float){0}.asDouble()', 
                                            '({0} == PyFloat.TYPE || {0} == PyInteger.TYPE || {0} == PyLong.TYPE)'),
   PRIMITIVES['long']: ClassConversionInfo('new PyLong', 
                                           '{0}.asLong()', 
                                           '{0} == PyLong.TYPE'),
   PRIMITIVES['long']: ClassConversionInfo('new PyLong', 
                                           '{0}.asLong()', 
                                           '{0} == PyLong.TYPE'),
   PRIMITIVES['char']:     'new PyString',
   Class.forName("java.lang.String"): 'new PyString',
   PRIMITIVES['boolean']:  'new PyBoolean' }
PY_CONVERSION_PREFIX = {PRIMITIVES['int']:      'new PyInteger',
                        PRIMITIVES['float']:    'new PyFloat',
                        PRIMITIVES['long']:     'new PyLong',
                        PRIMITIVES['char']:     'new PyString',
                        Class.forName("java.lang.String"): 'new PyString',
                        PRIMITIVES['boolean']:  'new PyBoolean' }
def get_conversion_prefix(klass):
    return PY_CONVERSION_PREFIX.get(klass, 'Py.java2py')

def is_builtin(name):
    return hasattr(__builtin__, name)

class PolymorphicMethod(object):
    def __init__(self, name, arity):
        self.name = name
        self.arity = arity
        self.methods = []
        
    def add_method(self, m):
        assert len(m.getParameterTypes()) == self.arity
        self.methods.append(m)
    
    


class Binding(object):
    def __init__(self, name):
        self.name = name
        self.field = None
        self.methods = {}

    def add_method(self, m):
        arity = len(m.getParameterTypes())
        pm = self.methods.get(arity, PolymorphicMethod(self.name, arity))
        pm.add_method(m)
    
    def set_field(self, f):
        if self.field:
            raise Exception("Binding %s's field was already set!" % self.name)
        self.field = f
    
    def emit(self):
        has_methods = len(self.methods) > 0
        is_wrapped_integer = self.field and self.field.getType() == PRIMITIVES['int']
        n = self.name
        if is_builtin(n):
            cog.outl('final PyObject %s_builtin = builtins.__getitem__("%s");' % (n, n))
        cog.out('builtins.__setitem__("%s",' % n)
        if self.field:
            if is_wrapped_integer:
                cog.out('new WrappedInteger()')
            else:
                cog.out('%s(%s)'%(get_conversion_prefix(self.field.getType()), n))
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
                cog.outl('''throw new RuntimeException("Can\'t call \\"%s\\" with "
                            + args.length + " parameters."); '''% n)
            for m in self.methods.values:
                m.emit()
            cog.outl('\t\t}\n\t}')
        if is_wrapped_integer:
            cog.outl('\tpublic int getValue() { return %s; }' % n)
        if has_methods or is_wrapped_integer:
            cog.out('}')
        cog.outl(');')
