# An individual Particle


class Particle(object):
    # A single force
    Gravity = PVector(0, 0.1)

    def __init__(self, sprite):
        # `lifespan`, `velocity`, and `center` are only **declared** here.
        self.lifespan = 0
        self.velocity = PVector()
        self.center = PVector()
        self.partSize = random(10, 60)
        # The particle is a textured quad.
        self.shp = self.makeShape(sprite)
        # Set the particle starting location.
        self.rebirth(width / 2, height / 2)

    def makeShape(self, sprite):
        shp = createShape()
        shp.beginShape(QUAD)
        shp.noStroke()
        shp.texture(sprite)
        shp.normal(0, 0, 1)
        shp.vertex(-self.partSize / 2, -self.partSize / 2,
                   0, 0)
        shp.vertex(self.partSize / 2, -self.partSize / 2,
                   sprite.width, 0)
        shp.vertex(self.partSize / 2, self.partSize / 2,
                   sprite.width, sprite.height)
        shp.vertex(-self.partSize / 2, self.partSize / 2,
                   0, sprite.height)
        shp.endShape()
        return shp

    def getShape(self):
        return self.shp

    def rebirth(self, x, y):
        # Set lifespan.
        self.lifespan = 255
        # Set velocity.
        self.velocity = PVector.fromAngle(random(TAU))
        # Set speed.
        self.velocity.mult(random(0.5, 4))
        # Reset location using translate.
        self.shp.resetMatrix()
        self.shp.translate(x, y)
        # Set center vector.
        self.center.set(x, y, 0)

    # Is it off the screen, or its lifespan is over?
    def isDead(self):
        return (self.center.x > width or self.center.x < 0
                or self.center.y > height or self.center.y < 0
                or self.lifespan < 0)

    def update(self):
        # Decrease life.
        self.lifespan = self.lifespan - 1
        # Apply gravity.
        self.velocity.add(Particle.Gravity)
        self.shp.setTint(color(255, self.lifespan))
        # Move the particle according to its velocity,
        self.shp.translate(self.velocity.x, self.velocity.y)
        # and also update the center
        self.center.add(self.velocity)
