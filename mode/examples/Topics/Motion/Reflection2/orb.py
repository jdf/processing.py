class Orb(object):
    # A damping of 80% slows it down when it hits the ground.
    Damping = 0.8
    Gravity = PVector(0, 0.05)

    def __init__(self, x, y, radius):
        # Orb has position and velocity.
        self.position = PVector(x, y)
        self.velocity = PVector(0.5, 0)
        self.radius = radius

    def move(self):
        # Move orb.
        self.velocity.add(Orb.Gravity)
        self.position.add(self.velocity)

    def display(self):
        # Draw orb.
        noStroke()
        fill(200)
        ellipse(self.position.x, self.position.y, self.radius * 2, self.radius * 2)

    # Check boundaries of window.
    def checkWallCollision(self):
        if self.position.x > width - self.radius:
            self.position.x = width - self.radius
            self.velocity.x *= -Orb.Damping

        elif self.position.x < self.radius:
            self.position.x = self.radius
            self.velocity.x *= -Orb.Damping

    def checkGroundCollision(self, ground):

        # Get difference between orb and ground.
        deltaX = self.position.x - ground.x
        deltaY = self.position.y - ground.y

        # Precalculate trig values.
        cosine = cos(ground.rot)
        sine = sin(ground.rot)

        # Rotate ground and velocity to allow orthogonal collision.
        #  calculations
        groundXTemp = cosine * deltaX + sine * deltaY
        groundYTemp = cosine * deltaY - sine * deltaX
        velocityXTemp = cosine * self.velocity.x + sine * self.velocity.y
        velocityYTemp = cosine * self.velocity.y - sine * self.velocity.x

        # Ground collision - check for surface collision and also that orb is
        #  within left / right bounds of ground segment.
        if (groundYTemp > -self.radius and
            self.position.x > ground.x1 and
            self.position.x < ground.x2):
            # keep orb from going into ground.
            groundYTemp = -self.radius
            # bounce and slow down orb.
            velocityYTemp *= -1.0
            velocityYTemp *= Orb.Damping

        # Reset ground, velocity and orb.
        deltaX = cosine * groundXTemp - sine * groundYTemp
        deltaY = cosine * groundYTemp + sine * groundXTemp
        self.velocity.x = cosine * velocityXTemp - sine * velocityYTemp
        self.velocity.y = cosine * velocityYTemp + sine * velocityXTemp
        self.position.x = ground.x + deltaX
        self.position.y = ground.y + deltaY
