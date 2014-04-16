class Vec3f(object):

    def __init__(self):
        self.set(0, 0, 0)

    def __repr__(self):
        return '<Vec3f x:%f y:%f p:%f>' % (self.x, self.y, self.p)

    def set(self, ix, iy, ip):
        self.x = ix
        self.y = iy
        self.p = ip

