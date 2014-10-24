# A class to describe a Star shape.
class Star(object):

    def __init__(self):
        self.x = random(100, width - 100)
        self.y = random(100, height - 100)
        self.speed = random(0.5, 3)
        # First create the shape.
        self.shp = createShape()
        self.shp.beginShape()
        # You can set fill and stroke.
        self.shp.fill(255, 204)
        self.shp.noStroke()
        # Here, we are hardcoding a series of vertices.
        self.shp.vertex(0, -50)
        self.shp.vertex(14, -20)
        self.shp.vertex(47, -15)
        self.shp.vertex(23, 7)
        self.shp.vertex(29, 40)
        self.shp.vertex(0, 25)
        self.shp.vertex(-29, 40)
        self.shp.vertex(-23, 7)
        self.shp.vertex(-47, -15)
        self.shp.vertex(-14, -20)
        # The shape is complete.
        self.shp.endShape(CLOSE)

    def move(self):
        # Demonstrating some simple motion.
        self.x += self.speed
        if self.x > width + 100:
            self.x = -100

    def display(self):
        # Locating and drawing the shape.
        with pushMatrix():
            translate(self.x, self.y)
            shape(self.shp)
