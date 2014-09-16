"""
Mouse functions.

Click on the box and drag it across the screen.
"""

boxSize = 75
overBox = False
locked = False
xOffset = 0.0
yOffset = 0.0


def setup():
    size(640, 360)
    global bx, by
    bx = width / 2.0
    by = height / 2.0
    rectMode(RADIUS)


def draw():
    global overBox

    background(0)
    if bx - boxSize < mouseX < bx + boxSize and \
       by - boxSize < mouseY < by + boxSize:
        overBox = True
        if not locked:
            stroke(255)
            fill(153)
    else:
        stroke(153)
        fill(153)
        overBox = False
    rect(bx, by, boxSize, boxSize)


def mousePressed():
    global locked, xOffset, yOffset
    if overBox:
        locked = True
        fill(255, 255, 255)
    else:
        locked = False
    xOffset = mouseX - bx
    yOffset = mouseY - by


def mouseDragged():
    global bx, by

    if locked:
        bx = mouseX - xOffset
        by = mouseY - yOffset


def mouseReleased():
    global locked
    locked = False

