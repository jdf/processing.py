""" 
Penrose Snowflake L-System 
by Geraldine Sarmiento. 

This code was based on Patrick Dwyer's L-System class. 
"""

from l_system import LSystem
from penrose_snowflake_l_system import PenroseSnowflakeLSystem

def setup():
    size(640, 360)
    stroke(255)
    noFill()
    global ps
    ps = PenroseSnowflakeLSystem()
    ps.simulate(4)


def draw():
    background(0)
    ps.render()

