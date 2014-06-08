class Hair(object):
    def __init__(self, radius):
        self.radius = radius
        self.phi = random(TAU)
        self.slow = random(1.15, 1.2)
        self.theta = asin(random(-self.radius, self.radius) / self.radius)
        self.z = self.radius * sin(self.theta)

    def render(self):
        oFF = (noise(millis() * 0.0005, sin(self.phi)) - 0.5) * 0.3
        oFFb = (noise(millis() * 0.0007, sin(self.z) * 0.01) - 0.5) * 0.3

        self.thetaFF = self.theta + oFF
        phiFF = self.phi + oFFb
        x = self.radius * cos(self.theta) * cos(self.phi)
        y = self.radius * cos(self.theta) * sin(self.phi)
        self.z = self.radius * sin(self.theta)

        xo = self.radius * cos(self.thetaFF) * cos(phiFF)
        yo = self.radius * cos(self.thetaFF) * sin(phiFF)
        zo = self.radius * sin(self.thetaFF)

        xb = xo * self.slow
        yb = yo * self.slow
        zb = zo * self.slow

        with beginShape(LINES):
            stroke(0)
            vertex(x, y, self.z)
            stroke(200, 150)
            vertex(xb, yb, zb)
