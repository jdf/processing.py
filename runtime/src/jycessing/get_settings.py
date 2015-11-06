import ast

__width__ = 100
__height__ = 100
__renderer__ = "JAVA2D"
__fullScreen__ = False
__smooth__ = False
__noSmooth__ = False

def extract_settings(module):
    global __width__, __height__, __renderer__, __fullScreen__, __smooth__, __noSmooth__
    for node in module.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            func = node.value.func
            if not hasattr(func, 'id'): continue
            if func.id in ('size', 'smooth', 'noSmooth', 'fullScreen'):
                module.body.remove(node)
            if func.id == 'size':
                args = node.value.args
                if len(args) > 0 and isinstance(args[0], ast.Num):
                    __width__ = args[0].n
                if len(args) > 1 and isinstance(args[1], ast.Num):
                    __height__ = args[0].n
                if len(args) > 2:
                    if isinstance(args[2], ast.Str):
                        __renderer__ = args[2].s
                    elif isinstance(args[2], ast.Name):
                        __renderer__ = args[2].id
            elif func.id == 'fullScreen':
                __fullScreen__ = True
            elif func.id == 'smooth':
                __smooth__ = True
            elif func.id == 'noSmooth':
                __noSmooth__ = True 

module = ast.parse(__processing_source__ + "\n\n", filename=__file__)
extract_settings(module)

__cleaned_sketch__ = compile(module, __file__, mode='exec') 
