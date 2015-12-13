"""
Reach 1 
based on code from Keith Peters.

The arm follows the position of the mouse by
calculating the angles with atan2(). 
"""

segLength = 80
x = 0
y = 0
x2 = 0
y2 = 0


def setup():
    size(640, 360)
    strokeWeight(20.0)
    stroke(255, 100)
    x = width / 2
    y = height / 2
    x2 = x
    y2 = y


def draw():
    global x, y
    background(0)
    dx = mouseX - x
    dy = mouseY - y
    angle1 = atan2(dy, dx)
    tx = mouseX - cos(angle1) * segLength
    ty = mouseY - sin(angle1) * segLength
    dx = tx - x2
    dy = ty - y2
    angle2 = atan2(dy, dx)
    x = x2 + cos(angle2) * segLength
    y = y2 + sin(angle2) * segLength
    segment(x, y, angle1)
    segment(x2, y2, angle2)


def segment(x, y, a):
    with pushMatrix():
        translate(x, y)
        rotate(a)
        line(0, 0, segLength, 0)
