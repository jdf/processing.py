""" 
Pentigree L-System 
by Geraldine Sarmiento. 

This code was based on Patrick Dwyer's L-System class. 
"""

from l_system import LSystem
from pentigree_l_system import PentigreeLSystem

def setup():
    size(640, 360)
    global ps
    ps = PentigreeLSystem()
    ps.simulate(3)


def draw():
    background(0)
    ps.render()

