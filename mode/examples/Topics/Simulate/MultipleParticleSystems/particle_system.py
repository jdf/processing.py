# A list is used to manage the list of Particles.

from particle import Particle
from crazy_particle import CrazyParticle


class ParticleSystem(object):

    def __init__(self, num, v):
        self.particles = []  # Initialize the list.
        self.origin = v.get()  # Store the origin point.
        for i in range(num):
            # Add "num" amount of particles to the list.
            self.particles.append(Particle(self.origin))

    def run(self):
        # Cycle through the list backwards, because we are deleting while
        # iterating.
        for i in reversed(range(len(self.particles))):
            p = self.particles[i]
            p.run()
            if p.isDead():
                del self.particles[i]

    def addParticle(self):
        p = None
        # Add either a Particle or CrazyParticle to the system.
        if int(random(0, 2)) == 0:
            p = Particle(self.origin)
        else:
            p = CrazyParticle(self.origin)
        self.particles.append(p)

    # A method to test if the particle system still has particles.
    def dead(self):
        return self.particles.isEmpty()

