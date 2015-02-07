from particle import Particle


class ParticleSystem(object):

    def __init__(self, n, sprite):
        self.particleShape = createShape(PShape.GROUP)
        self.particles = [Particle(sprite) for _ in range(n)]
        for p in self.particles:
            self.particleShape.addChild(p.getShape())

    def update(self):
        for p in self.particles:
            p.update()

    def setEmitter(self, x, y):
        for p in self.particles:
            if p.isDead():
                p.rebirth(x, y)

    def display(self):
        shape(self.particleShape)
