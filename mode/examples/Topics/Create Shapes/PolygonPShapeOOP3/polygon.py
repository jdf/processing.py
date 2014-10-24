# A class to describe a Polygon (with a PShape).
class Polygon(object):

    def __init__(self, shp):
        self.x = random(width)
        self.y = random(-500, -100)
        self.shp = shp
        self.speed = random(2, 6)

    # Simple motion
    def move(self):
        self.y += self.speed
        if self.y > height + 100:
            self.y = -100

    # Draw the object.
    def display(self):
        with pushMatrix():
            translate(self.x, self.y)
            shape(self.shp)
