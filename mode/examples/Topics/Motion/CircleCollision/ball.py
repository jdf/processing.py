class Ball(object):

    def __init__(self, x, y, radius):
        self.position = PVector(x, y)
        self.velocity = PVector.random2D()
        self.velocity.mult(3)
        self.radius = radius
        self.m = self.radius * 0.1

    def update(self):
        self.position.add(self.velocity)

    def checkBoundaryCollision(self):
        if self.position.x > width - self.radius:
            self.position.x = width - self.radius
            self.velocity.x *= -1
        elif self.position.x < self.radius:
            self.position.x = self.radius
            self.velocity.x *= -1
        elif self.position.y > height - self.radius:
            self.position.y = height - self.radius
            self.velocity.y *= -1
        elif self.position.y < self.radius:
            self.position.y = self.radius
            self.velocity.y *= -1

    def checkCollision(self, other):
        # Get distances between the balls components.
        bVect = PVector.sub(other.position, self.position)

        # Calculate magnitude of the vector separating the balls.
        bVectMag = bVect.mag()
        if bVectMag < self.radius + other.radius:
            # Get angle of bVect.
            theta = bVect.heading()

            # Precalculate trig values.
            sine = sin(theta)
            cosine = cos(theta)

            # bTemp will hold rotated ball positions. You just need to worry
            #  about bTemp[1] position.
            bTemp = [PVector(), PVector()]

            # This ball's position is relative to the other so you can use the
            #  vector between them (bVect) as the reference point in the
            #  rotation expressions. bTemp[0].position.x and
            #  bTemp[0].position.y will initialize automatically to 0.0, which
            #  is what you want since b[1] will rotate around b[0].
            bTemp[1].x = cosine * bVect.x + sine * bVect.y
            bTemp[1].y = cosine * bVect.y - sine * bVect.x

            # Rotate Temporary velocities.
            vTemp = [PVector(), PVector()]
            vTemp[0].x = cosine * self.velocity.x + sine * self.velocity.y
            vTemp[0].y = cosine * self.velocity.y - sine * self.velocity.x
            vTemp[1].x = cosine * other.velocity.x + sine * other.velocity.y
            vTemp[1].y = cosine * other.velocity.y - sine * other.velocity.x

            # Now that velocities are rotated, you can use 1D conservation of
            #  momentum equations to calculate the velocity along the x-
            #  axis.
            vFinal = [PVector(), PVector()]

            # Rotated velocity for b[0].
            vFinal[0].x = (((self.m - other.m) *
                            vTemp[0].x + 2 * other.m * vTemp[1].x) /
                          (self.m + other.m))
            vFinal[0].y = vTemp[0].y

            # Rotated velocity for b[0].
            vFinal[1].x = (((other.m - self.m) *
                            vTemp[1].x + 2 * self.m * vTemp[0].x) /
                          (self.m + other.m))
            vFinal[1].y = vTemp[1].y

            # Hack to avoid clumping.
            bTemp[0].x += vFinal[0].x
            bTemp[1].x += vFinal[1].x

            # Rotate ball positions and velocities back Reverse signs in trig
            #  expressions to rotate in the opposite direction.
            # Rotate balls.
            bFinal = [PVector(), PVector()]
            bFinal[0].x = cosine * bTemp[0].x - sine * bTemp[0].y
            bFinal[0].y = cosine * bTemp[0].y + sine * bTemp[0].x
            bFinal[1].x = cosine * bTemp[1].x - sine * bTemp[1].y
            bFinal[1].y = cosine * bTemp[1].y + sine * bTemp[1].x

            # Update balls to screen position.
            other.position.x = self.position.x + bFinal[1].x
            other.position.y = self.position.y + bFinal[1].y
            self.position.add(bFinal[0])

            # Update velocities.
            self.velocity.x = cosine * vFinal[0].x - sine * vFinal[0].y
            self.velocity.y = cosine * vFinal[0].y + sine * vFinal[0].x
            other.velocity.x = cosine * vFinal[1].x - sine * vFinal[1].y
            other.velocity.y = cosine * vFinal[1].y + sine * vFinal[1].x

    def display(self):
        noStroke()
        fill(204)
        ellipse(self.position.x, self.position.y, self.radius * 2, self.radius * 2)
