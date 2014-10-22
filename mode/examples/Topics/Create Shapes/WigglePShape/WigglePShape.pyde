"""
WigglePShape.

How to move the individual vertices of a PShape.
"""
from wiggler import Wiggler

# A "Wiggler" object
wiggler = None


def setup():
    global wiggler
    size(640, 360, P2D)
    smooth()
    wiggler = Wiggler()


def draw():
    background(255)
    wiggler.display()
    wiggler.wiggle()
