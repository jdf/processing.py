from particle import Particle


class ParticleSystem(object):

    def __init__(self, n, sprite):
        self.particleShape = createShape(PShape.GROUP)
        self.particles = [Particle(sprite) for _ in range(n)]
        for particle in self.particles:
            self.particleShape.addChild(particle.getShape())

    def update(self):
        for particle in self.particles:
            particle.update()

    def setEmitter(self, x, y):
        for particle in self.particles:
            if particle.isDead():
                particle.rebirth(x, y)

    def display(self):
        shape(self.particleShape)

