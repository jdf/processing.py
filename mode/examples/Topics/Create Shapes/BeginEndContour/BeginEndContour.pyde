"""
BeginEndContour

This example shows how to cut a shape out of another using beginContour() and endContour().
"""

shape = None

def setup():
    global shape
    size(640, 360, P2D)
    smooth()
    # Make a shape
    shape = createShape()
    shape.beginShape()
    shape.fill(0)
    shape.stroke(255)
    shape.strokeWeight(2)
    # Exterior part of shape
    shape.vertex(-100, -100)
    shape.vertex(100, -100)
    shape.vertex(100, 100)
    shape.vertex(-100, 100)
    # Interior part of shape
    shape.beginContour()
    shape.vertex(-10, -10)
    shape.vertex(10, -10)
    shape.vertex(10, 10)
    shape.vertex(-10, 10)
    shape.endContour()
    # Finishing off shape
    shape.endShape(CLOSE)


def draw():
    background(52)
    # Display shape
    translate(width / 2, height / 2)
    # Shapes can be rotated
    shape.rotate(0.01)
    shape(shape)

