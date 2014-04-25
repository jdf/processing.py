from particle import Particle


class ParticleSystem:

    def __init__(self, n, sprite):
        self.particles = []
        self.particleShape = createShape(PShape.GROUP)
        for i in range(n):
            p = Particle(sprite)
            self.particles.append(p)
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

