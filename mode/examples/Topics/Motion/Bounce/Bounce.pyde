"""
Bounce.
When the shape hits the edge of the window, it reverses its direction.
"""

# Half width of the shape.
Radius = 60

# Speed of the shape.
XSpeed = 2.8
YSpeed = 2.2

# Starting position of shape.
xpos = 0
ypos = 0

# Left to Right.
xdirection = 1

# Top to Bottom.
ydirection = 1


def setup():
    size(640, 360)
    global xpos, ypos
    noStroke()
    frameRate(30)
    ellipseMode(RADIUS)
    # Set the starting position of the shape.
    xpos = width / 2
    ypos = height / 2


def draw():
    global xpos, ypos, xdirection, ydirection
    background(102)

    # Update the position of the shape.
    xpos += XSpeed * xdirection
    ypos += YSpeed * ydirection

    # Test to see if the shape exceeds the boundaries of the screen.
    # If it does, reverse its direction by multiplying by -1.
    if (xpos < Radius) or (width - Radius < xpos):
        xdirection *= -1

    if (ypos < Radius) or (height - Radius < ypos):
        ydirection *= -1

    # Draw the shape
    ellipse(xpos, ypos, Radius, Radius)
