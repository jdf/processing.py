"""
WigglePShape. 

How to move the individual vertices of a PShape.
"""
from wiggler import Wiggler

def setup():
    size(640, 360, P2D)
    smooth()
    global w
    w = Wiggler()


def draw():
    background(255)
    w.display()
    w.wiggle()

