"""
Follow 3    
based on code from Keith Peters. 

A segmented line follows the mouse. The relative angle from
each segment to the next is calculated with atan2() and the
position of the next is calculated with sin() and cos().
"""

x = [0.0] * 20
y = [0.0] * 20
segLength = 18


def setup():
    size(640, 360)
    strokeWeight(9)
    stroke(255, 100)


def draw():
    background(0)
    dragSegment(0, mouseX, mouseY)
    for i in range(len(x) - 1):
        dragSegment(i + 1, x[i], y[i])


def dragSegment(i, xin, yin):
    dx = xin - x[i]
    dy = yin - y[i]
    angle = atan2(dy, dx)
    x[i] = xin - cos(angle) * segLength
    y[i] = yin - sin(angle) * segLength
    segment(x[i], y[i], angle)


def segment(x, y, a):
    with pushMatrix():
        translate(x, y)
        rotate(a)
        line(0, 0, segLength, 0)

