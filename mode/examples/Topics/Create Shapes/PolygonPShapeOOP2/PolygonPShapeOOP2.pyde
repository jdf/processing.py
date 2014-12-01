"""
PolygonPShapeOOP. 

Wrapping a PShape inside a custom class 
and demonstrating how we can have a multiple objects each
using the same PShape.
"""
from polygon import Polygon

# A list of objects
polygons = []

def setup():
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

    # Pass in reference to the PShape.
    # We coud make polygons with different PShapes.
    for i in range(25):
        polygons.append(Polygon(star))


def draw():
    background(255)
    # Display and move them all.
    for poly in polygons:
        poly.display()
        poly.move()

