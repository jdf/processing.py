"""
Reach 3
based on code from Keith Peters.

The arm follows the position of the ball by
calculating the angles with atan2().
"""
numSegments = 8
x = [0.0] * numSegments
y = [0.0] * numSegments
angle = [0.0] * numSegments
segLength = 26
targetX = 0
targetY = 0
ballX = 50
ballY = 50
ballXDirection = 2.5
ballYDirection = -2


def setup():
    size(640, 360)
    strokeWeight(20.0)
    stroke(255, 100)
    noFill()
    x[-1] = width / 2  # Set base x-coordinate
    y[-1] = height  # Set base y-coordinate


def draw():
    global ballX, ballY
    global ballXDirection, ballYDirection
    background(0)
    strokeWeight(20)
    ballX = ballX + 1.0 * ballXDirection
    ballY = ballY + 0.8 * ballYDirection
    if ballX > width - 25 or ballX < 25:
        ballXDirection *= -1
    if ballY > height - 25 or ballY < 25:
        ballYDirection *= -1
    ellipse(ballX, ballY, 30, 30)
    reachSegment(0, ballX, ballY)
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
    global targetX, targetY
    dx = xin - x[i]
    dy = yin - y[i]
    angle[i] = atan2(dy, dx)
    targetX = xin - cos(angle[i]) * segLength
    targetY = yin - sin(angle[i]) * segLength


def segment(x, y, a, sw):
    strokeWeight(sw)
    with pushMatrix():
        translate(x, y)
        rotate(a)
        line(0, 0, segLength, 0)
