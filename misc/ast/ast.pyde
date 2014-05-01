import ast
import astpp
from java.lang import String as JString
expr = """
x = 0
y = []
z = set()
a, b = 4, 5
j, (k, m) = 2, (3, 4)
def foo(a):
    notglob = 12
    x += 1
    print x
    if 23 < 21:
        a = x
    else:
        b -= x
        
def bar(x = 2):
    global y, e
    pass

print b
foo(12)
print b

def setup():
    size(400, 400)
    smooth()
    
def draw():
    x = (x + 10) % width
    background(0)
    noStroke()
    ellipse(x, 100, 20, 20)
"""

p = ast.parse(expr)
print 'BEFORE'
print astpp.dump(p)


class NameAccumulator(object):

    def __init__(self, names=None):
        if names is None:
            self.names = set()
        else:
            self.names = names

    def visit(self, tuple_or_name):
        if hasattr(tuple_or_name, 'elts'):
            for elt in tuple_or_name.elts:
                self.visit(elt)
        elif hasattr(tuple_or_name, 'id'):
            self.names.add(tuple_or_name.id)
        else:
            raise tuple_or_name

acc = NameAccumulator()
for node in p.body:
    if isinstance(node, ast.Assign):
        for t in node.targets:
            acc.visit(t)
globals = acc.names


class FindFunctionAssignments(ast.NodeVisitor):

    def __init__(self):
        self.acc = NameAccumulator()

    def visit_Assign(self, node):
        for t in node.targets:
            self.acc.visit(t)

    def visit_AugAssign(self, node):
        self.acc.visit(node.target)

    def find(self, func):
        self.visit(func)
        return self.acc.names

class Func(object):

    def __init__(self, func):
        self.node = func
        self.args = set(name.id for name in func.args.args)
        self.assigned_names = FindFunctionAssignments().find(func)

    def append_globals_statement(self):
        needed = self.assigned_names.difference(
            self.args).intersection(globals)
        glowball = __global__(needed)
        self.node.body.insert(0, glowball)
        print needed

    def __repr__(self):
        return '<function %s with args %s assigning to %s>' % (self.node.name, self.args, self.assigned_names)


funcs = []
for node in p.body:
    if isinstance(node, ast.FunctionDef):
        Func(node).append_globals_statement()


print '\n\n\n\nAFTER'
print astpp.dump(p)

fixed = ast.fix_missing_locations(p)
codeobj = compile(p, __file__, mode='exec')
exec(codeobj)

