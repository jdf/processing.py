class Particle(object):

    def __init__(self, sprite):
        self.gravity = PVector(0, 0.1)
        self.lifespan = 255
        self.velocity = PVector()
        partSize = random(10, 60)
        self.part = createShape()
        self.part.beginShape(QUAD)
        self.part.noStroke()
        self.part.texture(sprite)
        self.part.normal(0, 0, 1)
        self.part.vertex(-partSize / 2, -partSize / 2, 0, 0)
        self.part.vertex(+partSize / 2, -partSize / 2, sprite.width, 0)
        self.part.vertex(+partSize / 2, +partSize / 2,
                         sprite.width, sprite.height)
        self.part.vertex(-partSize / 2, +partSize / 2, 0, sprite.height)
        self.part.endShape()
        self.rebirth(width / 2, height / 2)
        self.lifespan = random(255)

    def getShape(self):
        return self.part

    def rebirth(self, x, y):
        a = random(TWO_PI)
        speed = random(0.5, 4)
        self.velocity = PVector(cos(a), sin(a))
        self.velocity.mult(speed)
        self.lifespan = 255
        self.part.resetMatrix()
        self.part.translate(x, y)

    def isDead(self):
        return self.lifespan < 0

    def update(self):
        self.lifespan -= 1
        self.velocity.add(self.gravity)
        self.part.setTint(color(255, self.lifespan))
        self.part.translate(self.velocity.x, self.velocity.y)

