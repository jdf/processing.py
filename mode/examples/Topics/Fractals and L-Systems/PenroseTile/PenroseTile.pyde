""" 
Penrose Tile L-System 
by Geraldine Sarmiento.

This code was based on Patrick Dwyer's L-System class. 
"""

from l_system import LSystem
from penrose_l_system import PenroseLSystem

ds = None


def setup():
    size(640, 360)
    ds = PenroseLSystem()
    ds.simulate(4)


def draw():
    background(0)
    ds.render()

