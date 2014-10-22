# An object that wraps the PShape.
class Wiggler(object):

    def __init__(self):
        # For 2D Perlin noise
        self.yoff = 0
        # Its location
        self.x = width / 2
        self.y = height / 2
        # The "original" locations of the vertices make up a circle.
        # We are using a list to keep a duplicate copy
        # of vertices original locations.
        self.original = []
        for a in range(0, TWO_PI * 10, 2):
            ascaled = a * .1
            vec = PVector.fromAngle(ascaled)
            vec.mult(100)
            self.original.append(vec)
        # The PShape to be "wiggled".
        # Make the PShape with those vertices.
        self.shape = createShape()
        self.shape.beginShape()
        self.shape.fill(127)
        self.shape.stroke(0)
        self.shape.strokeWeight(2)
        for vert in self.original:
            self.shape.vertex(vert.x, vert.y)
        self.shape.endShape(CLOSE)

    def wiggle(self):
        xoff = 0
        # Apply an offset to each vertex.
        for i in range(self.shape.getVertexCount()):
            # Calculate a vertex location based on noise around "original"
            # location.
            pos = self.original[i]
            a = TWO_PI * noise(xoff, self.yoff)
            radius = PVector.fromAngle(a)
            radius.mult(4)
            radius.add(pos)
            # Set the location of each vertex to the one.
            self.shape.setVertex(i, radius)
            # Increment perlin noise x value.
            xoff += 0.5
        # Increment perlin noise y value.
        self.yoff += 0.02

    def display(self):
        with pushMatrix():
            translate(self.x, self.y)
            shape(self.shape)
