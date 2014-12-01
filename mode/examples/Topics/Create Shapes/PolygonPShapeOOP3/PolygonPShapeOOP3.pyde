"""
PolygonPShapeOOP.

Wrapping a PShape inside a custom class
and demonstrating how we can have a multiple objects each
using the same PShape.
"""

import random
from polygon import Polygon

# A list of objects
polygons = []
# Three possible shapes
shapes = [None] * 3


def setup():
    size(640, 360, P2D)
    smooth()
    shapes[0] = createShape(ELLIPSE, 0, 0, 100, 100)
    shapes[0].setFill(color(255, 127))
    shapes[0].setStroke(False)
    shapes[1] = createShape(RECT, 0, 0, 100, 100)
    shapes[1].setFill(color(255, 127))
    shapes[1].setStroke(False)
    shapes[2] = createShape()
    shapes[2].beginShape()
    shapes[2].fill(0, 127)
    shapes[2].noStroke()
    shapes[2].vertex(0, -50)
    shapes[2].vertex(14, -20)
    shapes[2].vertex(47, -15)
    shapes[2].vertex(23, 7)
    shapes[2].vertex(29, 40)
    shapes[2].vertex(0, 25)
    shapes[2].vertex(-29, 40)
    shapes[2].vertex(-23, 7)
    shapes[2].vertex(-47, -15)
    shapes[2].vertex(-14, -20)
    shapes[2].endShape(CLOSE)

    for i in range(25):
        polygons.append(Polygon(random.choice(shapes)))


def draw():
    background(102)
    # Display and move them all.
    for poly in polygons:
        poly.display()
        poly.move()

