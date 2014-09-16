"""
Inheritance

A class can be defined using another class as a foundation. In object-oriented
programming terminology, one class can inherit fields and methods from another. 
An object that inherits from another is called a subclass, and the object it 
inherits from is called a superclass. A subclass extends the superclass.
"""

def setup():
    size(640, 360)
    global arm, spots
    arm = SpinArm(width / 2, height / 2, 0.01)
    spots = SpinSpots(width / 2, height / 2, -0.02, 90.0)


def draw():
    background(204)
    arm.update()
    arm.display()
    spots.update()
    spots.display()


class Spin(object):
    def __init__(self, xpos, ypos, s):
        self.angle = 0.0
        self.x = xpos
        self.y = ypos
        self.speed = s

    def update(self):
        self.angle += self.speed


class SpinArm(Spin):
    def __init__(self, x, y, s):
        super(SpinArm, self).__init__(x, y, s)

    def display(self):
        strokeWeight(1)
        stroke(0)
        with pushMatrix():
            translate(self.x, self.y)
            self.angle += self.speed
            rotate(self.angle)
            line(0, 0, 165, 0)


class SpinSpots(Spin):
    def __init__(self, x, y, s, d):
        super(SpinSpots, self).__init__(x, y, s)
        self.dim = d

    def display(self):
        noStroke()
        with pushMatrix():
            translate(self.x, self.y)
            self.angle += self.speed
            rotate(self.angle)
            ellipse(-self.dim / 2, 0, self.dim, self.dim)
            ellipse(self.dim / 2, 0, self.dim, self.dim)

