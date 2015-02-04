'''
    A wireframe box with colored edges which expands and contracts according
    to time-of-day.
    An original implementation of *hms* from http://www.gysin-vanetti.com/hms
    (C) Ben Alkov, 2014, licensed as APL 2.0 as part of processing.py
    (https://github.com/jdf/processing.py).
'''


def setup():
    global fillCube, edgeCube
    size(500, 500, P3D)
    smooth(4)
    camera(0, 0, 100,
           0, 0, 0,
           0, 1, 0)

    # Creating a **filled** wireframe cube is non-obvious.
    # We need an opaque black cube inside a transparent wireframe cube.
    fillCube = createShape(BOX, 2)
    edgeCube = makeEdgeCube()

    # The fill color here has to match the `background` from `draw` in order
    # for the fill cube to be invisible.
    fillCube.setFill(color(10))


def draw():
    rotateX(sin(frameCount * 0.008))
    rotateY(cos(frameCount * 0.008))

    # The fill color here has to match the `fillCube`'s `setFill` color in
    # order for the fill cube to be invisible.
    background(10)
    drawShape()


def drawShape():
    # `map`; "Re-maps a number from one range to another."
    # Scale time units to 3D coordinates.
    x = map(second(), 0, 59, 1, 12)
    y = map(minute(), 0, 59, 1, 12)
    z = map(hour(), 0, 23, 1, 12)

    scale(x, y, z)
    shape(fillCube, 0, 0)
    shape(edgeCube, 0, 0)


def makeEdgeCube():
    # Draw a 2x2x2 transparent cube with edges colored according to the
    # current time.
    Red = color(255, 137, 95)  # Seconds.
    Green = color(176, 255, 121)  # Minutes.
    Blue = color(56, 76, 204)  # Hours.
    edgeCube = createShape()
    edgeCube.beginShape(LINES)

    # Seconds - lines along `x`.
    edgeCube.stroke(Red)
    edgeCube.vertex(-1, 1, 1)
    edgeCube.vertex(1, 1, 1)
    edgeCube.vertex(-1, -1, 1)
    edgeCube.vertex(1, -1, 1)
    edgeCube.vertex(-1, -1, -1)
    edgeCube.vertex(1, -1, -1)
    edgeCube.vertex(-1, 1, -1)
    edgeCube.vertex(1, 1, -1)

    # Minutes - lines along `y`.
    edgeCube.stroke(Green)
    edgeCube.vertex(-1, 1, 1)
    edgeCube.vertex(-1, -1, 1)
    edgeCube.vertex(1, 1, 1)
    edgeCube.vertex(1, -1, 1)
    edgeCube.vertex(1, 1, -1)
    edgeCube.vertex(1, -1, -1)
    edgeCube.vertex(-1, 1, -1)
    edgeCube.vertex(-1, -1, -1)

    # Hours - lines along `z`.
    edgeCube.stroke(Blue)
    edgeCube.vertex(-1, 1, -1)
    edgeCube.vertex(-1, 1, 1)
    edgeCube.vertex(1, 1, -1)
    edgeCube.vertex(1, 1, 1)
    edgeCube.vertex(1, -1, -1)
    edgeCube.vertex(1, -1, 1)
    edgeCube.vertex(-1, -1, -1)
    edgeCube.vertex(-1, -1, 1)
    edgeCube.endShape()
    return edgeCube
