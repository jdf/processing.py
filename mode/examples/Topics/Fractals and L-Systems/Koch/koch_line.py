# The Nature of Code
# Daniel Shiffman
# http://natureofcode.com
# Koch Curve
# A class to describe one line segment in the fractal.
# Includes methods to calculate midPVectors along the line according to
# the Koch algorithm.


class KochLine(object):

    def __init__(self, start, end):
        # Two PVectors,
        # a is the "left" PVector and
        # b is the "right PVector
        self.a = start.get()
        self.b = end.get()

    def display(self):
        stroke(255)
        line(self.a.x, self.a.y, self.b.x, self.b.y)

    def start(self):
        return self.a.get()

    def end(self):
        return self.b.get()

    # This is easy, just 1/3 of the way
    def kochleft(self):
        v = PVector.sub(self.b, self.a)
        v.div(3)
        v.add(self.a)
        return v

    # More complicated, have to use a little trig to figure out where this
    # PVector is!
    def kochmiddle(self):
        v = PVector.sub(self.b, self.a)
        v.div(3)
        p = self.a.get()
        p.add(v)
        v.rotate(-radians(60))
        p.add(v)
        return p

    # Easy, just 2/3 of the way
    def kochright(self):
        v = PVector.sub(self.a, self.b)
        v.div(3)
        v.add(self.b)
        return v

