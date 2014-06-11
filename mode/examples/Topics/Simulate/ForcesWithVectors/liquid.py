"""
Forces (Gravity and Fluid Resistence) with Vectors 
by Daniel Shiffman.    

Demonstration of multiple force acting on bodies (Mover class)
Bodies experience gravity continuously
Bodies experience fluid resistance when in "water"
"""

# Liquid class
class Liquid(object):

    # Liquid is a rectangle.

    def __init__(self, x_, y_, w_, h_, c_):
        self.x = x_
        self.y = y_
        self.w = w_
        self.h = h_
        # Coefficient of drag.
        self.c = c_

    # Is the Mover in the Liquid?
    def contains(self, m):
        loc = m.location
        return self.x < loc.x < self.x + self.w and self.y < loc.y < self.y + self.h

    # Calculate drag force.
    def drag(self, m):
        # Magnitude is coefficient * speed squared.
        speed = m.velocity.mag()
        dragMagnitude = self.c * speed * speed
        # Direction is inverse of velocity.
        drag = m.velocity.get()
        drag.mult(-1)
        # Scale according to magnitude.
        drag.setMag(dragMagnitude)
        return drag

    def display(self):
        noStroke()
        fill(127)
        rect(self.x, self.y, self.w, self.h)

