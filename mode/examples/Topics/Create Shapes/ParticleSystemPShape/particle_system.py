# The Particle System

from particle import Particle


class ParticleSystem(object):

    def __init__(self, n):
        sprite = loadImage("sprite.png")
        # Make all the Particles.
        # It's just a list of particle objects.
        self.particles = [Particle(sprite) for _ in range(n)]
        # The PShape to group all the particle PShapes.
        self.particleShape = createShape(GROUP)
        # Each particle's PShape gets added to the System PShape.
        for particle in self.particles:
            self.particleShape.addChild(particle.getShape())

    def update(self):
        for particle in self.particles:
            particle.update()

    def setEmitter(self, x, y):
        for particle in self.particles:
            # Each particle gets reborn at the emitter location.
            if particle.isDead():
                particle.rebirth(x, y)

    def display(self):
        shape(self.particleShape)
