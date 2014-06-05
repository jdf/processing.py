"""
Forces (Gravity and Fluid Resistence) with Vectors 
by Daniel Shiffman.    

Demonstration of multiple force acting on bodies (Mover class)
Bodies experience gravity continuously
Bodies experience fluid resistance when in "water"
"""


class Mover(object):

    def __init__(self, m, x, y):
        # Mass is tied to size.
        self.mass = m
        self.location = PVector(x, y)
        self.velocity = PVector(0, 0)
        self.acceleration = PVector(0, 0)

    # Newton's 2nd law: F = M * A
    # or A = F / M
    def applyForce(self, force):
        # Divide by mass.
        f = PVector.div(force, self.mass)
        # Accumulate all forces in acceleration.
        self.acceleration.add(f)

    def update(self):
        # Velocity changes according to acceleration.
        self.velocity.add(self.acceleration)
        # Location changes by velocity.
        self.location.add(self.velocity)
        # We must clear acceleration each frame.
        self.acceleration.mult(0)

    # Draw Mover.
    def display(self):
        stroke(255)
        strokeWeight(2)
        fill(255, 200)
        ellipse(self.location.x, self.location.y,
                self.mass * 16, self.mass * 16)

    # Bounce off bottom of window.
    def checkEdges(self):
        if self.location.y > height:
            # A little dampening when hitting the bottom.
            self.velocity.y *= -0.9
            self.location.y = height

