# An individual Particle


class Particle(object):

    def __init__(self, sprite):
        # A single force
        self.gravity = PVector(0, 0.1)
        self.partSize = random(10, 60)
        # The particle is a textured quad.
        self.part = createShape()
        self.part.beginShape(QUAD)
        self.part.noStroke()
        self.part.texture(sprite)
        self.part.normal(0, 0, 1)
        self.part.vertex(-self.partSize / 2, -self.partSize / 2, 0, 0)
        self.part.vertex(self.partSize / 2,
                         -self.partSize / 2, sprite.width, 0)
        self.part.vertex(self.partSize / 2,
                         self.partSize / 2, sprite.width, sprite.height)
        self.part.vertex(-self.partSize / 2,
                         self.partSize / 2, 0, sprite.height)
        self.part.endShape()
        # Initialize center vector.
        self.center = PVector()
        # Set the particle starting location.
        self.rebirth(width / 2, height / 2)

    def getShape(self):
        return self.part

    def rebirth(self, x, y):
        a = random(TWO_PI)
        speed = random(0.5, 4)
        # A velocity with random angle and magnitude.
        self.velocity = PVector.fromAngle(a)
        self.velocity.mult(speed)
        # Set lifespan.
        self.lifespan = 255
        # Set location using translate.
        self.part.resetMatrix()
        self.part.translate(x, y)
        # Update center vector.
        self.center.set(x, y, 0)

    # Is it off the screen, or its lifespan is over?
    def isDead(self):
        return (self.center.x > width or self.center.x < 0
                or self.center.y > height or self.center.y < 0 or
                self.lifespan < 0)

    def update(self):
        # Decrease life.
        self.lifespan = self.lifespan - 1
        # Apply gravity.
        self.velocity.add(self.gravity)
        self.part.setTint(color(255, self.lifespan))
        # Move the particle according to its velocity,
        self.part.translate(self.velocity.x, self.velocity.y)
        # and also update the center
        self.center.add(self.velocity)
