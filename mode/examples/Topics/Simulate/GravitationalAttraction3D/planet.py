# Gravitational Attraction (3D)
# Daniel Shiffman <http://www.shiffman.net>
# A class for(object): an orbiting Planet


class Planet(object):

    # Basic physics model (location, velocity, acceleration, mass)
    def __init__(self, m, x, y, z):
        self.mass = m
        self.location = PVector(x, y, z)
        self.velocity = PVector(1, 0)  # Arbitrary starting velocity
        self.acceleration = PVector(0, 0)

    # Newton's 2nd Law (F = M*A) applied
    def applyForce(self, force):
        f = PVector.div(force, self.mass)
        self.acceleration.add(f)

    # Our motion algorithm (aka Euler Integration)
    def update(self):
        # Velocity changes according to acceleration.
        self.velocity.add(self.acceleration)
        self.location.add(self.velocity)  # Location changes according to velocity.
        self.acceleration.mult(0)

    # Draw the Planet.
    def display(self):
        noStroke()
        fill(255)
        with pushMatrix():
            translate(self.location.x, self.location.y, self.location.z)
            sphere(self.mass * 8)

