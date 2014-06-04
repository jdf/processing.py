"""
Bounce.
When the shape hits the edge of the window, it reverses its direction.
"""

rad = 60  # Width of the shape.
# Starting position of shape.
xpos = 0
ypos = 0

# Speed of the shape.
xspeed = 2.8
yspeed = 2.2

xdirection = 1  # Left or Right.
ydirection = 1  # Top to Bottom.


def setup():
    size(640, 360)
    noStroke()
    frameRate(30)
    ellipseMode(RADIUS)
    # Set the starting position of the shape.
    xpos = width / 2
    ypos = height / 2


def draw():
    background(102)

    # Update the position of the shape.
    xpos = xpos + (xspeed * xdirection)
    ypos = ypos + (yspeed * ydirection)

    # Test to see if the shape exceeds the boundaries of the screen.
    # If it does, reverse its direction by multiplying by -1.
    if xpos > width - rad or xpos < rad:
        xdirection *= -1

    if ypos > height - rad or ypos < rad:
        ydirection *= -1

    # Draw the shape
    ellipse(xpos, ypos, rad, rad)
