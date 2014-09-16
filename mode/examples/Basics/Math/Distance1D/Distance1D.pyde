"""
Distance 1D.

Move the mouse left and right to control the
speed and direction of the moving shapes.
"""

xpos = [0, 0, 0, 0]
thin = 8
thick = 36


def setup():
    size(640, 360)
    noStroke()
    for i in range(len(xpos)):
        xpos[i] = width / 2


def draw():
    background(0)

    mx = mouseX * 0.4 - width / 5.0
    fill(102)
    rect(xpos[1], 0, thick, height / 2)
    fill(204)
    rect(xpos[0], 0, thin, height / 2)
    fill(102)
    rect(xpos[3], height / 2, thick, height / 2)
    fill(204)
    rect(xpos[2], height / 2, thin, height / 2)

    xpos[0] += mx / 16
    xpos[1] += mx / 64
    xpos[2] -= mx / 16
    xpos[3] -= mx / 64
    
    for i in (0, 2):
        if xpos[i] < -thin:
            xpos[i] = width
        if xpos[i] > width:
            xpos[i] = -thin

    for i in (1, 3):
        if xpos[i] < -thick:
            xpos[i] = width
        if xpos[i] > width:
            xpos[i] = -thick

