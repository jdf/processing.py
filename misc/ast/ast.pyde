import ast
import astpp

expr = """
x = 0
y = []
z = set()
a, b = 4, 5
j, (k, m) = 2, (3, 4)
def foo():
    global x, y
    notglob = 12
    x += 1
    print x
    if 23 > 21:
        a = x
    else:
        b -= x
        
def bar(x = 2):
    pass
"""

p = ast.parse(expr)
print 'BEFORE'
print astpp.dump(p)


class NameAccumulator(object):

    def __init__(self, names = None):
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

globals = set()
acc = NameAccumulator(globals)
for node in p.body:
    if isinstance(node, ast.Assign):
        for t in node.targets:
            acc.visit(t)
print globals


class FindFunctionAssignments(ast.NodeVisitor):

    def __init__(self):
        self.assigned_names = set()
        self.acc = NameAccumulator(self.assigned_names)

    def visit_Assign(self, node):
        for t in node.targets:
            acc.visit(t)

    def visit_AugAssign(self, node):
        acc.visit(node.target)

    def find(self, func):
        self.visit(func)
        return self.assigned_names

class Func(object):

    def __init__(self, func):
        self.node = func
        self.args = set(name.id for name in func.args.args)
        self.global_refs = FindFunctionAssignments().find(func)
        
    def __repr__(self):
        return '<function %s with args %s referring to globals %s>' % (self.node.name, self.args, self.global_refs)


class FindFuncs(ast.NodeVisitor):

    def __init__(self):
        self.funcs = []

    def visit_FunctionDef(self, func):
        self.funcs.append(Func(func))

    def get_funcs(self, module):
        self.visit(module)
        return self.funcs

funcs = FindFuncs().get_funcs(p)
print funcs
exit()

