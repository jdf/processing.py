# An object that wraps the PShape.
class Wiggler(object):

    # The PShape to be "wiggled".
    s = None
    # Its location
    x = None
    y = None
    # For 2D Perlin noise
    yoff = 0
    # We are using an ArrayList to keep a duplicate copy
    # of vertices original locations.
    original = []

    def __init__(self):
        self.x = width / 2
        self.y = height / 2
        # The "original" locations of the vertices make up a circle.
        self.original = []
        for a in range(0, TWO_PI * 10, 2):
            ascaled = a * .1
            v = PVector.fromAngle(ascaled)
            v.mult(100)
            self.original.append(v)
        # Now make the PShape with those vertices.
        self.s = createShape()
        self.s.beginShape()
        self.s.fill(127)
        self.s.stroke(0)
        self.s.strokeWeight(2)
        for v in self.original:
            self.s.vertex(v.x, v.y)
        self.s.endShape(CLOSE)

    def wiggle(self):
        xoff = 0
        # Apply an offset to each vertex.
        for i in range(self.s.getVertexCount()):
            # Calculate a vertex location based on noise around "original"
            # location.
            pos = self.original[i]
            a = TWO_PI * noise(xoff, self.yoff)
            r = PVector.fromAngle(a)
            r.mult(4)
            r.add(pos)
            # Set the location of each vertex to the one.
            self.s.setVertex(i, r.x, r.y)
            # Increment perlin noise x value.
            xoff += 0.5

        # Increment perlin noise y value.
        self.yoff += 0.02

    def display(self):
        pushMatrix()
        translate(self.x, self.y)
        shape(self.s)
        popMatrix()

