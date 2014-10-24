"""
BeginEndContour

This example shows how to cut a shape out of another using beginContour() and endContour().
"""


def setup():
    global shp
    size(640, 360, P2D)
    smooth()
    # Make a shape
    shp = createShape()
    shp.beginShape()
    shp.fill(0)
    shp.stroke(255)
    shp.strokeWeight(2)
    # Exterior part of shape
    shp.vertex(-100, -100)
    shp.vertex(100, -100)
    shp.vertex(100, 100)
    shp.vertex(-100, 100)
    # Interior part of shape
    shp.beginContour()
    shp.vertex(-10, -10)
    shp.vertex(10, -10)
    shp.vertex(10, 10)
    shp.vertex(-10, 10)
    shp.endContour()
    # Finishing off shape
    shp.endShape(CLOSE)


def draw():
    background(52)
    # Display shape
    translate(width / 2, height / 2)
    # Shapes can be rotated
    shp.rotate(0.01)
    shape(shp)
