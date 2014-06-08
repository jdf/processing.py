# A class to describe a Star shape.
class Star(object):

    def __init__(self):
        self.x = random(100, width - 100)
        self.y = random(100, height - 100)
        self.speed = random(0.5, 3)
        # First create the shape.
        self.s = createShape()
        self.s.beginShape()
        # You can set fill and stroke.
        self.s.fill(255, 204)
        self.s.noStroke()
        # Here, we are hardcoding a series of vertices.
        self.s.vertex(0, -50)
        self.s.vertex(14, -20)
        self.s.vertex(47, -15)
        self.s.vertex(23, 7)
        self.s.vertex(29, 40)
        self.s.vertex(0, 25)
        self.s.vertex(-29, 40)
        self.s.vertex(-23, 7)
        self.s.vertex(-47, -15)
        self.s.vertex(-14, -20)
        # The shape is complete.
        self.s.endShape(CLOSE)

    def move(self):
        # Demonstrating some simple motion.
        self.x += self.speed
        if self.x > width + 100:
            self.x = -100

    def display(self):
        # Locating and drawing the shape.
        with pushMatrix():
            translate(self.x, self.y)
            shape(self.s)

