"""
Reach 2    
based on code from Keith Peters.

The arm follows the position of the mouse by
calculating the angles with atan2(). 
"""
numSegments = 10
x = [0.0] * numSegments
y = [0.0] * numSegments
angle = [0.0] * numSegments
segLength = 26
targetX = 0
targetY = 0

def setup():
    size(640, 360)
    strokeWeight(20.0)
    stroke(255, 100)
    x[len(x) - 1] = width / 2  # Set base x-coordinate
    y[len(x) - 1] = height  # Set base y-coordinate


def draw():
    background(0)
    reachSegment(0, mouseX, mouseY)
    for i in range(1, numSegments):
        reachSegment(i, targetX, targetY)
    for i in range(len(x) - 1, 0, -1):
        positionSegment(i, i - 1)
    for i in range(len(x)):
        segment(x[i], y[i], angle[i], (i + 1) * 2)


def positionSegment(a, b):
    x[b] = x[a] + cos(angle[a]) * segLength
    y[b] = y[a] + sin(angle[a]) * segLength


def reachSegment(i, xin, yin):
    dx = xin - x[i]
    dy = yin - y[i]
    angle[i] = atan2(dy, dx)
    global targetX, targetY
    targetX = xin - cos(angle[i]) * segLength
    targetY = yin - sin(angle[i]) * segLength


def segment(x, y, a, sw):
    strokeWeight(sw)
    with pushMatrix():
        translate(x, y)
        rotate(a)
        line(0, 0, segLength, 0)
