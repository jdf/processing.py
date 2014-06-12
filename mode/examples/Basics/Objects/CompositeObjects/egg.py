class Egg(object):

    def __init__(self, xpos, ypos, t, s):
        self.x = xpos  # x-coordinate
        self.y = ypos  # y-coordinate
        self.tilt = t  # Left and right angle offset
        self.angle = 0  # Used to define the tilt
        self.scalar = s / 100.0  # Height of the egg

    def wobble(self):
        self.tilt = cos(self.angle) / 8
        self.angle += 0.1

    def display(self):
        noStroke()
        fill(255)
        with pushMatrix():
            translate(self.x, self.y)
            rotate(self.tilt)
            scale(self.scalar)
            with beginShape():
                vertex(0, -100)
                bezierVertex(25, -100, 40, -65, 40, -40)
                bezierVertex(40, -15, 25, 0, 0, 0)
                bezierVertex(-25, 0, -40, -15, -40, -40)
                bezierVertex(-40, -65, -25, -100, 0, -100)

