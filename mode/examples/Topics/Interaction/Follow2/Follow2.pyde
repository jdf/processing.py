"""
Follow 2    
based on code from Keith Peters. 

A two-segmented arm follows the cursor position. The relative
angle between the segments is calculated with atan2() and the
position calculated with sin() and cos().
"""
x = [0.0] * 2
y = [0.0] * 2
segLength = 50


def setup():
    size(640, 360)
    strokeWeight(20.0)
    stroke(255, 100)


def draw():
    background(0)
    dragSegment(0, mouseX, mouseY)
    dragSegment(1, x[0], y[0])


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

