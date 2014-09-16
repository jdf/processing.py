"""
Increment Decrement.

Writing "a += 1" is equivalent to "a = a + 1".
Writing "a -= 1" is equivalent to "a = a - 1".
"""

a = 0
b = 0
direction = True

def setup():
    size(640, 360)
    colorMode(RGB, width)
    b = width
    frameRate(30)


def draw():
    global direction, a, b
    a += 1
    if a > width:
        a = 0
        direction = not direction
    if direction:
        stroke(a)
    else:
        stroke(width - a)
    line(a, 0, a, height / 2)
    b -= 1
    if b < 0:
        b = width

    if direction:
        stroke(width - b)
    else:
        stroke(b)

    line(b, height / 2 + 1, b, height)

