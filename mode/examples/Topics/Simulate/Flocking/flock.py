# The Flock (a list of Boid objects)
class Flock(object):

    def __init__(self):
        self.boids = []  # Initialize a list for all the boids.

    def run(self):
        for b in self.boids:
            # Pass the entire list of boids to each boid individually.
            b.run(self.boids)

    def addBoid(self, b):
        self.boids.append(b)

