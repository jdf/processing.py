from shape3d import Shape3D


class Icosahedron(Shape3D):

    def __init__(self, radius=150):
        Shape3D.__init__(self)
        self.radius = radius
        self.topPent = [PVector() for _ in range(5)]
        self.bottomPent = [PVector() for _ in range(5)]
        self.angle = 0
        c = dist(cos(0) * self.radius,
                 sin(0) * self.radius,
                 cos(radians(72)) * self.radius,
                 sin(radians(72)) * self.radius)
        b = self.radius
        a = sqrt((c**2) - (b**2))
        self.triHeight = sqrt((c**2) - (c / 2)**2)

        for i in range(5):
            self.topPent[i] = PVector(cos(self.angle) * self.radius,
                                      sin(self.angle) * self.radius,
                                      self.triHeight / 2.0)
            self.angle += radians(72)
        self.topPoint = PVector(0, 0, self.triHeight / 2.0 + a)
        self.angle = 72.0 / 2.0
        for i in range(5):
            self.bottomPent[i] = PVector(cos(self.angle) * self.radius,
                                         sin(self.angle) * self.radius,
                                         -self.triHeight / 2.0)
            self.angle += radians(72)
        self.bottomPoint = PVector(0, 0, -(self.triHeight / 2.0 + a))

    # Draw icosahedron.
    def create(self):
        for i in range(5):
            if i < 4:
                # Icosahedron top.
                self.makeTriangle(self.topPent[i],
                                  self.topPoint,
                                  self.topPent[i + 1])
                # Icosahedron bottom.
                self.makeTriangle(self.bottomPent[i],
                                  self.bottomPoint,
                                  self.bottomPent[i + 1])
            else:
                self.makeTriangle(self.topPent[i],
                                  self.topPoint,
                                  self.topPent[0])
                self.makeTriangle(self.bottomPent[i],
                                  self.bottomPoint,
                                  self.bottomPent[0])

        # Icosahedron body.
        for i in range(5):
            if i < 3:
                self.makeTriangle(self.topPent[i],
                                  self.bottomPent[i + 1],
                                  self.bottomPent[i + 2])
                self.makeTriangle(self.bottomPent[i + 2],
                                  self.topPent[i],
                                  self.topPent[i + 1])
            elif i == 3:
                self.makeTriangle(self.topPent[i],
                                  self.bottomPent[i + 1],
                                  self.bottomPent[0])
                self.makeTriangle(self.bottomPent[0],
                                  self.topPent[i],
                                  self.topPent[i + 1])
            elif i == 4:
                self.makeTriangle(self.topPent[i],
                                  self.bottomPent[0],
                                  self.bottomPent[1])
                self.makeTriangle(self.bottomPent[1],
                                  self.topPent[i],
                                  self.topPent[0])

    def makeTriangle(self, a, b, c):
        beginShape()
        vertex(a.x, a.y, a.z)
        vertex(b.x, b.y, b.z)
        vertex(c.x, c.y, c.z)
        endShape(CLOSE)

    # Overridden methods fom Shape3D.
    def rotZ(self, theta):
        tx = 0
        ty = 0
        tz = 0

        # Top point.
        tx = cos(theta) * self.topPoint.x + sin(theta) * self.topPoint.y
        ty = sin(theta) * self.topPoint.x - cos(theta) * self.topPoint.y
        self.topPoint.x = tx
        self.topPoint.y = ty

        # Bottom point.
        tx = cos(theta) * self.bottomPoint.x + sin(theta) * self.bottomPoint.y
        ty = sin(theta) * self.bottomPoint.x - cos(theta) * self.bottomPoint.y
        self.bottomPoint.x = tx
        self.bottomPoint.y = ty

        # Top and bottom pentagons.
        for i in range(5):
            tx = cos(theta) * self.topPent[i].x + sin(theta) * self.topPent[i].y
            ty = sin(theta) * self.topPent[i].x - cos(theta) * self.topPent[i].y
            self.topPent[i].x = tx
            self.topPent[i].y = ty

            tx = cos(theta) * self.bottomPent[i].x + sin(theta) * self.bottomPent[i].y
            ty = sin(theta) * self.bottomPent[i].x - cos(theta) * self.bottomPent[i].y
            self.bottomPent[i].x = tx
            self.bottomPent[i].y = ty

    def rotX(theta):
        pass

    def rotY(theta):
        pass
