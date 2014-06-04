"""
Forces (Gravity and Fluid Resistence) with Vectors 
by Daniel Shiffman.    

Demonstration of multiple force acting on bodies (Mover class)
Bodies experience gravity continuously
Bodies experience fluid resistance when in "water"

For the basics of working with PVector, see
http://processing.org/learning/pvector/
as well as examples in Topics/Vectors/
"""

from liquid import Liquid
from mover import Mover

# Five moving bodies
movers = [None] * 10
# Liquid
liquid = None


def setup():
    size(640, 360)
    reset()
    # Create liquid object.
    liquid = Liquid(0, height / 2, width, height / 2, 0.1)


def draw():
    background(0)
    # Draw water.
    liquid.display()
    for i in range(len(movers)):
        # Is the Mover in the liquid?
        if liquid.contains(movers[i]):
            # Calculate drag force.
            drag = liquid.drag(movers[i])
            # Apply drag force to Mover.
            movers[i].applyForce(drag)
        # Gravity is scaled by mass here!
        gravity = PVector(0, 0.1 * movers[i].mass)
        # Apply gravity.
        movers[i].applyForce(gravity)
        # Update and display.
        movers[i].update()
        movers[i].display()
        movers[i].checkEdges()
    fill(255)
    text("click mouse to reset", 10, 30)


def mousePressed():
    reset()


# Restart all the Mover objects randomly.
def reset():
    for i in range(len(movers)):
        movers[i] = Mover(random(0.5, 3), 40 + i * 70, 0)
