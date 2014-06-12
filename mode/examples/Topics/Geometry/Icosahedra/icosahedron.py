from shape3d import Shape3D


class Icosahedron(Shape3D):

    def __init__(self, radius=150):
        Shape3D.__init__(self)
        self.topPent = [PVector() for _ in range(5)]
        self.bottomPent = [PVector() for _ in range(5)]
        c = dist(cos(0) * radius,
                 sin(0) * radius,
                 cos(radians(72)) * radius,
                 sin(radians(72)) * radius)
        b = radius
        a = sqrt((c**2) - (b**2))
        self.triHeight = sqrt((c**2) - (c / 2)**2)
        angle = 0
        for i in range(5):
            self.topPent[i] = PVector(cos(angle) * radius,
                                      sin(angle) * radius,
                                      self.triHeight / 2.0)
            angle += radians(72)
        self.topPoint = PVector(0, 0, self.triHeight / 2.0 + a)
        angle = 72.0 / 2.0
        for i in range(5):
            self.bottomPent[i] = PVector(cos(angle) * radius,
                                         sin(angle) * radius,
                                         -self.triHeight / 2.0)
            angle += radians(72)
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
        with beginShape():
            vertex(a.x, a.y, a.z)
            vertex(b.x, b.y, b.z)
            vertex(c.x, c.y, c.z)
