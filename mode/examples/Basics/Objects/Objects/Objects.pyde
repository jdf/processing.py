"""
Objects
by hbarragan. 

Move the cursor across the image to change the speed and positions
of the geometry. The class MRect defines a group of lines.
"""

r1 = None
r2 = None
r3 = None
r4 = None


def setup():
    size(640, 360)
    fill(255, 204)
    noStroke()
    r1 = MRect(1, 134.0, 0.532, 0.1 * height, 10.0, 60.0)
    r2 = MRect(2, 44.0, 0.166, 0.3 * height, 5.0, 50.0)
    r3 = MRect(2, 58.0, 0.332, 0.4 * height, 10.0, 35.0)
    r4 = MRect(1, 120.0, 0.0498, 0.9 * height, 15.0, 60.0)


def draw():
    background(0)

    r1.display()
    r2.display()
    r3.display()
    r4.display()

    r1.move(mouseX - (width / 2), mouseY + (height * 0.1), 30)
    r2.move((mouseX + (width * 0.05)) % width, mouseY + (height * 0.025), 20)
    r3.move(mouseX / 4, mouseY - (height * 0.025), 40)
    r4.move(mouseX - (width / 2), (height - mouseY), 50)


class MRect(object):

    def __init__(self, iw, ixp, ih, iyp, id, it):
        self.w = iw  # single bar width
        self.xpos = ixp  # rect xposition
        self.h = ih  # rect height
        self.ypos = iyp  # rect yposition
        self.d = id  # single bar distance
        self.t = it  # number of bars

    def move(self, posX, posY, damping):
        self.dif = self.ypos - posY
        if abs(self.dif) > 1:
            self.ypos -= self.dif / damping

        self.dif = self.xpos - posX
        if abs(self.dif) > 1:
            self.xpos -= self.dif / damping

    def display(self):
        for i in range(self.t):
            rect(self.xpos + (i * (self.d + self.w)),
                 self.ypos, self.w, height * self.h)

