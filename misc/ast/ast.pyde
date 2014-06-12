import ast


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
    Finds assignments in a function body, and accumulates the
    names of the assigned-to entities.
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


def insert_global_statements(module):
    """
    Finds all of the function definitions in a module, and inserts global
    statements in those that assign to names that are the same as existing
    module globals.

    For example, insert_global_statements will transform the AST for

      x = 0
      def draw():
          x = (x + 1) % width

    into the AST for

      x = 0
      def draw():
          global x
          x = (x + 1) % width
    """
    for node in module.body:
        if isinstance(node, ast.FunctionDef):
            args = set(name.id for name in node.args.args)
            assigned_names = FindFunctionAssignments().find(node)
            globals = get_module_globals(module)
            needed = assigned_names.difference(args).intersection(globals)
            node.body.insert(0, __global__(needed))

source = """
x = 0

def setup():
    size(400, 400)
    smooth()
    
def draw():
    x = (x + 5) % width
    background(0)
    noStroke()
    ellipse(x, 100, 20, 20)
"""
module = ast.parse(source)
insert_global_statements(module)
# Is this desirable?
# fixed = ast.fix_missing_locations(p)
codeobj = compile(module, __file__, mode='exec')
exec(codeobj)

