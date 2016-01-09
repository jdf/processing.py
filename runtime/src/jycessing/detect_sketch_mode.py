import ast
import re

from jycessing import MixedModeError
"""
Determines the sketch mode, namely:

"ACTIVE" if the sketch uses draw() and/or setup() functions;
"STATIC" otherise.
"MIXED" if the user seems to have erroneously both declared a draw()
    function and called drawing functions outside draw().
"""

# If you define any of these functions, you're in ACTIVE mode.
activeModeFunc = re.compile(r"""
    ^(
        draw
        |
        setup
        |
        key(Pressed|Released|Typed)
        |
        mouse(Clicked|Dragged|Moved|Pressed|Released|Wheel)
    )$
""", re.X)

# If you're in ACTIVE mode, you can't call any of these functions
# outside a function body.
illegalActiveModeCall = re.compile(r"""
    ^(
        size
        |
        bezier(Detail|Point|Tangent)?
        |
        curve(Detail|Point|Tangent|Tightness)?
        |
        arc|ellipse|line|point|quad|rect|triangle
        |
        box|sphere(Detail)?
        (begin|end)(Countour|Shape)
        |
        (quadratic|bezier|curve)?Vertex | vertex
        |
        (apply|pop|print|push|reset)Matrix
        |
        rotate[XYZ]?
        |
        (ambient|directional|point|spot)Light
        |
        light(Fallof|Specular|s)
        |
        noLights
        |
        normal
        |
        ambient|emissive|shininess|specular
        |
        (load|update)Pixels
        |
        background|clear|(no)?(Fill|Stroke)
    )$
""", re.X)

def detect_mode(code, filename):
    module = ast.parse(code + "\n\n", filename=filename)
    mode = 'STATIC'
    for node in module.body:
        if isinstance(node, ast.FunctionDef):
            if activeModeFunc.match(node.name):
                mode = 'ACTIVE'
                break
    if mode == 'STATIC':
        return mode, None
    for node in module.body:
        if not isinstance(node, ast.Expr):
            continue
        e = node.value
        if not isinstance(e, ast.Call):
            continue
        f = e.func
        if hasattr(f, 'id') and illegalActiveModeCall.match(f.id):
            return 'MIXED', MixedModeError(
                "You can't call %s() outside a function in \"active mode\"." % f.id,
                __file__, node.lineno - 1)
    return mode, None

__mode__, __error__ = detect_mode(__processing_source__, __file__)
