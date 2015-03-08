"""
Moving On Curves.

In this example, the circles moves along the curve y = x^4.
Click the mouse to have it move to a position.
"""

beginX = 20.0  # Initial x-coordinate.
beginY = 10.0  # Initial y-coordinate.
endX = 570.0  # Final x-coordinate.
endY = 320.0  # Final y-coordinate.
distX = None  # X-axis distance to move.
distY = None  # Y-axis distance to move.
exponent = 4  # Determines the curve.
x = 0.0  # Current x-coordinate.
y = 0.0  # Current y-coordinate.
step = 0.01  # Size of each step along the path.
pct = 0.0  # Percentage traveled (0.0 to 1.0).


def setup():
    size(640, 360)
    global distX, distY
    noStroke()
    distX = endX - beginX
    distY = endY - beginY


def draw():
    global pct, x, y
    fill(0, 2)
    rect(0, 0, width, height)
    pct += step
    if pct < 1.0:
        x = beginX + (pct * distX)
        y = beginY + (pow(pct, exponent) * distY)
    fill(255)
    ellipse(x, y, 20, 20)


def mousePressed():
    global pct, beginX, beginY, endX, endY, distX, distY
    pct = 0.0
    beginX = x
    beginY = y
    endX = mouseX
    endY = mouseY
    distX = endX - beginX
    distY = endY - beginY
