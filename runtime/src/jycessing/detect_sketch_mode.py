import ast
import re

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
        bezier(Detail|Point|Tangent)?
        |
        curve(Detail|Point|Tangent|Tightness)?
        |
        arc|ellipse|line|point|quad|rect|triangle
        |
        box|sphere(Detail)?
        (begin|end)(Countour|Shape)
        |
        (quadratic|bezier|curve)?Vertex
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

module = ast.parse(__processing_source__ + "\n\n", filename=__file__)
mode = 'STATIC'
for node in module.body:
    if isinstance(node, ast.FunctionDef):
        if activeModeFunc.match(name):
            mode = 'ACTIVE'
            break

if mode == 'STATIC':
    return mode

for node in module.body:
    if not isinstance(node, ast.Expr):
        continue
    e = node.value
    if not isinstance(e, ast.Call):
        continue
    f = e.func
    if illegalActiveModeCall.match(f.id):
        return 'MIXED'
    
return mode
