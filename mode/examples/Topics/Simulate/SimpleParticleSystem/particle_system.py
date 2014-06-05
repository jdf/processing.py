# A class to describe a group of Particles.
# A list is used to manage the list of Particles.

from particle import Particle


class ParticleSystem(object):

    def __init__(self, location):
        self.origin = location.get()
        self.particles = []

    def addParticle(self):
        self.particles.append(Particle(self.origin))

    def run(self):
        for i in reversed(range(len(self.particles))):
            p = self.particles[i]
            p.run()
            if p.isDead():
                del self.particles[i]

