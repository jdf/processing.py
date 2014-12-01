"""
Koch Curve
by Daniel Shiffman.

Renders a simple fractal, the Koch snowflake. 
Each recursive level is drawn in sequence. 
"""

from koch_fractal import KochFractal
from koch_line import KochLine


def setup():
    size(640, 360)
    frameRate(1)  # Animate slowly
    global k
    k = KochFractal()


def draw():
    background(0)
    # Draws the snowflake!
    k.render()
    # Iterate
    k.nextLevel()
    # Let's not do it more than 5 times. . .
    if k.count > 5:
        k.restart()

