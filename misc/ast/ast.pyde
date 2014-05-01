import ast
import astpp
from java.lang import String as JString
expr = """
x = 0
j, (k, m) = 2, (3, 4)

def setup():
    size(400, 400)
    smooth()
    
def draw():
    x = (x + 10) % width
    background(0)
    noStroke()
    ellipse(x, 100, 20, 20)
"""

class NameAccumulator(ast.NodeVisitor):
    """
    NameAccumulator walks an AST "target" node, recursively gathering the 'id'
    properties of all of the Names it finds.
    """
    def __init__(self):
        self.names = set()

    def visit_Name(self, name):
        self.names.add(name.id)

def get_module_globals(module):
    """
    Examine all of the top-level nodes in the module, and remember the names
    of all variables assigned to.
    """
    acc = NameAccumulator()
    for node in module.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                acc.visit(t)
    return acc.names
    

class FindFunctionAssignments(ast.NodeVisitor):
    """
    """
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

def insert_globals_statement(func):
    args = set(name.id for name in func.args.args)
    assigned_names = FindFunctionAssignments().find(func)
    globals = get_module_globals(module)
    needed = assigned_names.difference(args).intersection(globals)
    func.body.insert(0, __global__(needed))

def insert_global_statements(module):
    for node in module.body:
        if isinstance(node, ast.FunctionDef):
            insert_globals_statement(node)
    
module = ast.parse(expr)
insert_global_statements(module)

#print astpp.dump(p)

#fixed = ast.fix_missing_locations(p)
codeobj = compile(module, __file__, mode='exec')
exec(codeobj)

