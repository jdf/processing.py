"""
Arctangent. 

Move the mouse to change the direction of the eyes. 
The atan2() function computes the angle from each eye 
to the cursor. 
"""

from eye import Eye

e1 = Eye(250, 16, 120)
e2 = Eye(164, 185, 80)
e3 = Eye(420, 230, 220)


def setup():
    size(640, 360)
    noStroke()


def draw():
    background(102)

    e1.update(mouseX, mouseY)
    e2.update(mouseX, mouseY)
    e3.update(mouseX, mouseY)
    e1.display()
    e2.display()
    e3.display()

