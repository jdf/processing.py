
# A simple Particle class, renders the particle as an image.


class Particle(object):

    def __init__(self, l, img):
        self.acc = PVector(0, 0)
        self.vx = randomGaussian() * 0.3
        self.vy = randomGaussian() * 0.3 - 1.0
        self.vel = PVector(self.vx, self.vy)
        self.loc = l.get()
        self.lifespan = 100.0
        self.img = img

    def run(self):
        self.update()
        self.render()

    # Method to apply a force vector to the Particle object
    # Note we are ignoring "mass" here.
    def applyForce(self, f):
        self.acc.add(f)

    # Method to update location
    def update(self):
        self.vel.add(self.acc)
        self.loc.add(self.vel)
        self.lifespan -= 2.5
        self.acc.mult(0)  # clear Acceleration.

    # Method to display
    def render(self):
        imageMode(CENTER)
        tint(255, self.lifespan)
        image(self.img, self.loc.x, self.loc.y)
        # Drawing a circle instead.
        # fill(255,lifespan)
        # noStroke()
        # ellipse(self.loc.x,self.loc.y,self.img.width,self.img.height)

    # Is the particle still useful?
    def isDead(self):
        return self.lifespan <= 0.0

