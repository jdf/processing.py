# A class to describe a Star shape.
class Star(object):

    def __init__(self):
        self.x = random(100, width - 100)
        self.y = random(100, height - 100)
        self.speed = random(0.5, 3)
        # First create the shape.
        self.shape = createShape()
        self.shape.beginShape()
        # You can set fill and stroke.
        self.shape.fill(255, 204)
        self.shape.noStroke()
        # Here, we are hardcoding a series of vertices.
        self.shape.vertex(0, -50)
        self.shape.vertex(14, -20)
        self.shape.vertex(47, -15)
        self.shape.vertex(23, 7)
        self.shape.vertex(29, 40)
        self.shape.vertex(0, 25)
        self.shape.vertex(-29, 40)
        self.shape.vertex(-23, 7)
        self.shape.vertex(-47, -15)
        self.shape.vertex(-14, -20)
        # The shape is complete.
        self.shape.endShape(CLOSE)

    def move(self):
        # Demonstrating some simple motion.
        self.x += self.speed
        if self.x > width + 100:
            self.x = -100

    def display(self):
        # Locating and drawing the shape.
        with pushMatrix():
            translate(self.x, self.y)
            shape(self.shape)
