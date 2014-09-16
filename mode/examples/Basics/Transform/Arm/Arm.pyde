"""
Arm. 

The angle of each segment is controlled with the mouseX and
mouseY position. The transformations applied to the first segment
are also applied to the second segment because they are inside
the same pushMatrix() and popMatrix() group.
"""

segLength = 100


def setup():
    size(600, 600)
    strokeWeight(30)
    stroke(255, 160)
    global x, y
    x = width * 0.3
    y = height * 0.5


def draw():
    background(0)

    angle1 = (mouseX / float(width) - 0.5) * -PI
    angle2 = (mouseY / float(height) - 0.5) * PI

    with pushMatrix():
        segment(x, y, angle1)
        segment(segLength, 0, angle2)


def segment(s, y, a):
    translate(x, y)
    rotate(a)
    line(0, 0, segLength, 0)

