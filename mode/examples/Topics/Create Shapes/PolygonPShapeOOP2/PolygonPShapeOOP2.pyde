"""
PolygonPShapeOOP.

Wrapping a PShape inside a custom class
and demonstrating how we can have a multiple objects each
using the same PShape.
"""
from polygon import Polygon

polygons = None


def setup():
    global polygons
    size(640, 360, P2D)
    smooth()
    # Make a PShape.
    star = createShape()
    star.beginShape()
    star.noStroke()
    star.fill(0, 127)
    star.vertex(0, -50)
    star.vertex(14, -20)
    star.vertex(47, -15)
    star.vertex(23, 7)
    star.vertex(29, 40)
    star.vertex(0, 25)
    star.vertex(-29, 40)
    star.vertex(-23, 7)
    star.vertex(-47, -15)
    star.vertex(-14, -20)
    star.endShape(CLOSE)
    # Add a bunch of objects to the ArrayList.
    # Pass in reference to the PShape.
    # We could make polygons with different PShapes.
    polygons = [Polygon(star) for _ in range(25)]


def draw():
    background(255)
    # Display and move them all.
    for poly in polygons:
        poly.display()
        poly.move()
