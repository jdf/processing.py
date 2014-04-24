"""
Arctangent. 

Move the mouse to change the direction of the eyes. 
The atan2() function computes the angle from each eye 
to the cursor. 
"""


def setup():
    size(640, 360)
    noStroke()
    global e1, e2, e3
    e1 = Eye(250, 16, 120)
    e2 = Eye(164, 185, 80)
    e3 = Eye(420, 230, 220)


def draw():
    background(102)

    e1.update(mouseX, mouseY)
    e2.update(mouseX, mouseY)
    e3.update(mouseX, mouseY)
    e1.display()
    e2.display()
    e3.display()


class Eye:

    def __init__(self, tx, ty, ts):
        self.x = tx
        self.y = ty
        self.size = ts
        self.angle = 0.0

    def update(self, mx,  my):
        self.angle = atan2(my - self.y, mx - self.x)

    def display(self):
        pushMatrix()
        translate(self.x, self.y)
        fill(255)
        ellipse(0, 0, self.size, self.size)
        rotate(self.angle)
        fill(153, 204, 0)
        ellipse(self.size / 4, 0, self.size / 2, self.size / 2)
        popMatrix()

