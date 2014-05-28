"""
PolygonPShapeOOP. 

Wrapping a PShape inside a custom class 
"""

from star import Star

# A Star object
s1 = None
s2 = None


def setup():
    size(640, 360, P2D)
    smooth()
    # Make a Star.
    s1 = Star()
    s2 = Star()


def draw():
    background(51)
    s1.display()  # Display the first star.
    s1.move()  # Move the first star.
    s2.display()  # Display the second star.
    s2.move()  # Move the second star.

