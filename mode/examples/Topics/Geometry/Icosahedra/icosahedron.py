from shape3d import Shape3D


class Icosahedron(Shape3D):

    def __init__(self, radius=150):
        Shape3D.__init__(self)
        self.radius = radius
        self.topPent = [PVector for p in range(5)]
        self.bottomPent = [PVector for p in range(5)]
        self.angle = 0

        c = dist(cos(0) * self.radius,
                 sin(0) * self.radius,
                 cos(radians(72)) * self.radius,
                 sin(radians(72)) * self.radius)
        b = self.radius
        a = sqrt((c * c) - (b * b))

        self.triHt = sqrt((c * c) - (c / 2)**2)

        for i in range(len(self.topPent)):
            self.topPent[i] = PVector(cos(self.angle) * self.radius,
                                      sin(self.angle) * self.radius,
                                      self.triHt / 2.0)
            self.angle += radians(72)

        self.topPoint = PVector(0, 0, self.triHt / 2.0 + a)
        self.angle = 72.0 / 2.0
        for i in range(len(self.topPent)):
            self.bottomPent[i] = PVector(cos(self.angle) * self.radius,
                                         sin(self.angle) * self.radius,
                                         -self.triHt / 2.0)
            self.angle += radians(72)

        self.bottomPoint = PVector(0, 0, -(self.triHt / 2.0 + a))

    # Draw icosahedron.
    def create(self):
        for i in range(len(self.topPent)):
            # Icosahedron top.
            beginShape()
            if i < len(self.topPent) - 1:
                vertex(self.locationX + self.topPent[i].x,
                       self.locationY + self.topPent[i].y,
                       self.locationZ + self.topPent[i].z)
                vertex(self.locationX + self.topPoint.x,
                       self.locationY + self.topPoint.y,
                       self.locationZ + self.topPoint.z)
                vertex(self.locationX + self.topPent[i + 1].x,
                       self.locationY + self.topPent[i + 1].y,
                       self.locationZ + self.topPent[i + 1].z)
            else:
                vertex(self.locationX + self.topPent[i].x,
                       self.locationY + self.topPent[i].y,
                       self.locationZ + self.topPent[i].z)
                vertex(self.locationX + self.topPoint.x,
                       self.locationY + self.topPoint.y,
                       self.locationZ + self.topPoint.z)
                vertex(self.locationX + self.topPent[0].x,
                       self.locationY + self.topPent[0].y,
                       self.locationZ + self.topPent[0].z)
            endShape(CLOSE)

            # Icosahedron bottom.
            beginShape()
            if i < len(self.bottomPent) - 1:
                vertex(self.locationX + self.bottomPent[i].x,
                       self.locationY + self.bottomPent[i].y,
                       self.locationZ + self.bottomPent[i].z)
                vertex(self.locationX + self.bottomPoint.x,
                       self.locationY + self.bottomPoint.y,
                       self.locationZ + self.bottomPoint.z)
                vertex(self.locationX + self.bottomPent[i + 1].x,
                       self.locationY + self.bottomPent[i + 1].y,
                       self.locationZ + self.bottomPent[i + 1].z)
            else:
                vertex(self.locationX + self.bottomPent[i].x,
                       self.locationY + self.bottomPent[i].y,
                       self.locationZ + self.bottomPent[i].z)
                vertex(self.locationX + self.bottomPoint.x,
                       self.locationY + self.bottomPoint.y,
                       self.locationZ + self.bottomPoint.z)
                vertex(self.locationX + self.bottomPent[0].x,
                       self.locationY + self.bottomPent[0].y,
                       self.locationZ + self.bottomPent[0].z)
            endShape(CLOSE)

        # Icosahedron body.
        for i in range(len(self.topPent)):
            if i < len(self.topPent) - 2:
                beginShape()
                vertex(self.locationX + self.topPent[i].x,
                       self.locationY + self.topPent[i].y,
                       self.locationZ + self.topPent[i].z)
                vertex(self.locationX + self.bottomPent[i + 1].x,
                       self.locationY + self.bottomPent[i + 1].y,
                       self.locationZ + self.bottomPent[i + 1].z)
                vertex(self.locationX + self.bottomPent[i + 2].x,
                       self.locationY + self.bottomPent[i + 2].y,
                       self.locationZ + self.bottomPent[i + 2].z)
                endShape(CLOSE)

                beginShape()
                vertex(self.locationX + self.bottomPent[i + 2].x,
                       self.locationY + self.bottomPent[i + 2].y,
                       self.locationZ + self.bottomPent[i + 2].z)
                vertex(self.locationX + self.topPent[i].x,
                       self.locationY + self.topPent[i].y,
                       self.locationZ + self.topPent[i].z)
                vertex(self.locationX + self.topPent[i + 1].x,
                       self.locationY + self.topPent[i + 1].y,
                       self.locationZ + self.topPent[i + 1].z)
                endShape(CLOSE)

            elif i == len(self.topPent) - 2:
                beginShape()
                vertex(self.locationX + self.topPent[i].x,
                       self.locationY + self.topPent[i].y,
                       self.locationZ + self.topPent[i].z)
                vertex(self.locationX + self.bottomPent[i + 1].x,
                       self.locationY + self.bottomPent[i + 1].y,
                       self.locationZ + self.bottomPent[i + 1].z)
                vertex(self.locationX + self.bottomPent[0].x,
                       self.locationY + self.bottomPent[0].y,
                       self.locationZ + self.bottomPent[0].z)
                endShape(CLOSE)

                beginShape()
                vertex(self.locationX + self.bottomPent[0].x,
                       self.locationY + self.bottomPent[0].y,
                       self.locationZ + self.bottomPent[0].z)
                vertex(self.locationX + self.topPent[i].x,
                       self.locationY + self.topPent[i].y,
                       self.locationZ + self.topPent[i].z)
                vertex(self.locationX + self.topPent[i + 1].x,
                       self.locationY + self.topPent[i + 1].y,
                       self.locationZ + self.topPent[i + 1].z)
                endShape(CLOSE)

            elif i == len(self.topPent) - 1:
                beginShape()
                vertex(self.locationX + self.topPent[i].x,
                       self.locationY + self.topPent[i].y,
                       self.locationZ + self.topPent[i].z)
                vertex(self.locationX + self.bottomPent[0].x,
                       self.locationY + self.bottomPent[0].y,
                       self.locationZ + self.bottomPent[0].z)
                vertex(self.locationX + self.bottomPent[1].x,
                       self.locationY + self.bottomPent[1].y,
                       self.locationZ + self.bottomPent[1].z)
                endShape(CLOSE)

                beginShape()
                vertex(self.locationX + self.bottomPent[1].x,
                       self.locationY + self.bottomPent[1].y,
                       self.locationZ + self.bottomPent[1].z)
                vertex(self.locationX + self.topPent[i].x,
                       self.locationY + self.topPent[i].y,
                       self.locationZ + self.topPent[i].z)
                vertex(self.locationX + self.topPent[0].x,
                       self.locationY + self.topPent[0].y,
                       self.locationZ + self.topPent[0].z)
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
        for i in range(len(self.topPent)):
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
