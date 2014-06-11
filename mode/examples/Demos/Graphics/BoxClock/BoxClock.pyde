'''
    A wireframe box with colored edges which expands and contracts according
    to time-of-day.
    An original implementation of *hms* from http://www.gysin-vanetti.com/hms
    (C) Ben Alkov, 2014, licensed as APL 2.0 as part of processing.py
    (https://github.com/jdf/processing.py).
'''
add_library('peasycam')

# Creating a **filled** wireframe cube is non-obvious.
# We need am opaque black cube...
fillCube = PShape()
# ...and a transparent colored wireframe.
edgeCube = PShape()
cam = None


def setup():
    size(500, 500, P3D)
    # rotateX(radians(180))
    # frameRate(60)
    smooth(4)
    cam = PeasyCam(this, 70)
    cam.setMinimumDistance(70)
    cam.setMaximumDistance(200)
    # Draw a 2x2x2 opaque box.
    fillCube = createShape(BOX, 2)
    # The fill color here has to match the `background` from `draw` in order
    # for the fill cube to be invisible.
    fillCube.setFill(color(10))
    makeEdgeCube()


def draw():
    # Note that we're rotating the *shape*, not the matrix or camera.
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
    # Note that we're scaling the *shape*, not the matrix or camera.
    scale(x, y, z)
    shape(fillCube, 0, 0)
    shape(edgeCube, 0, 0)


def makeEdgeCube():
    # Draw a 2x2x2 transparent box with different-colored edges.
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
