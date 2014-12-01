"""
BeginEndContour

This example shows how to cut a shape out of another using beginContour() and endContour().
"""

def setup():
    size(640, 360, P2D)
    smooth()
    # Make a shape
    global s
    s = createShape()
    s.beginShape()
    s.fill(0)
    s.stroke(255)
    s.strokeWeight(2)
    # Exterior part of shape
    s.vertex(-100, -100)
    s.vertex(100, -100)
    s.vertex(100, 100)
    s.vertex(-100, 100)
    # Interior part of shape
    s.beginContour()
    s.vertex(-10, -10)
    s.vertex(10, -10)
    s.vertex(10, 10)
    s.vertex(-10, 10)
    s.endContour()
    # Finishing off shape
    s.endShape(CLOSE)


def draw():
    background(52)
    # Display shape
    translate(width / 2, height / 2)
    # Shapes can be rotated
    s.rotate(0.01)
    shape(s)

