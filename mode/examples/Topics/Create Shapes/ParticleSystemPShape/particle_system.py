# The Particle System

from particle import Particle


class ParticleSystem(object):
    particles = None
    particleShape = None

    def __init__(self, n):
        # It's just an ArrayList of particle objects.
        self.particles = []
        # The PShape to group all the particle PShapes.
        self.particleShape = createShape(GROUP)
        # Make all the Particles.
        for i in range(n):
            p = Particle()
            self.particles.append(p)
            # Each particle's PShape gets added to the System PShape.
            self.particleShape.addChild(p.getShape())

    def update(self):
        for p in self.particles:
            p.update()

    def setEmitter(self, x, y):
        for p in self.particles:
            # Each particle gets reborn at the emitter location.
            if p.isDead():
                p.rebirth(x, y)

    def display(self):
        shape(self.particleShape)

