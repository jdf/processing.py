"""
Simple Linear Gradient 

The lerpColor() function is useful for interpolating
between two colors.
"""
# Constants
Y_AXIS = 1
X_AXIS = 2

# Define colors
b1 = color(255)
b2 = color(0)
c1 = color(204, 102, 0)
c2 = color(0, 102, 153)


def setup():
    size(640, 360)
    noLoop()


def draw():
    # Background
    setGradient(0, 0, width / 2, height, b1, b2, X_AXIS)
    setGradient(width / 2, 0, width / 2, height, b2, b1, X_AXIS)
    # Foreground
    setGradient(50, 90, 540, 80, c1, c2, Y_AXIS)
    setGradient(50, 190, 540, 80, c2, c1, X_AXIS)


def setGradient(x, y, w, h, c1, c2, axis):
    noFill()
    if axis == Y_AXIS:  # Top to bottom gradient
        for i in range(y, y + h + 1):
            inter = map(i, y, y + h, 0, 1)
            c = lerpColor(c1, c2, inter)
            stroke(c)
            line(x, i, x + w, i)
    elif axis == X_AXIS:  # Left to right gradient
        for i in range(x, x + w + 1):
            inter = map(i, x, x + w, 0, 1)
            c = lerpColor(c1, c2, inter)
            stroke(c)
            line(i, y, i, y + h)

