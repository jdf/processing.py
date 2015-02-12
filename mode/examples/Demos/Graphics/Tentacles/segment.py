class Segment(object):
    '''A Segment, which encapsulates its own position and color, and can draw
    itself'''

    def __init__(self, id, tickOffset, alti, color):
        self.id = id
        #  Effectively, the distance between segments.
        self.alti = alti
        self.tickOffset = tickOffset
        self.color = color
        self.loc = PVector(0.0, 0.0, 0.0)
        # A magic number. 12 just seems to look good.
        self.tickOffset *= 12

    def calc(self, time, sRadius):
        # Spherical coords.
        # New formula from http://acko.net/blog/js1k-demo-the-making-of
        lon = (cos(time + sin(time * 0.31)) * 2
               + sin(time * 0.83)
               * 3 + time * 0.02)
        lat = (sin(time * 0.7)
               - cos(3 + time * 0.23) * 3)
        # Convert to cartesian 3D.
        # http://acko.net/blog/js1k-demo-the-making-of
        self.loc.set(cos(lon) * cos(lat) * (sRadius + self.alti),
                     sin(lon) * cos(lat) * (sRadius + self.alti),
                     sin(lat) * (sRadius + self.alti))

    def drawSelf(self, other):
        stroke(self.color)
        line(self.loc.x, self.loc.y, self.loc.z,
             other.loc.x, other.loc.y, other.loc.z)
