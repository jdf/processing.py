class Ground(object):

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x = (self.x1 + self.x2) / 2
        self.y = (self.y1 + self.y2) / 2
        self.length = dist(self.x1, self.y1, self.x2, self.y2)
        self.rot = atan2((self.y2 - self.y1), (self.x2 - self.x1))
