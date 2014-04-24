"""
Distance 1D. 

Move the mouse left and right to control the 
speed and direction of the moving shapes. 
"""

thin = 8
thick = 36


def setup():
    size(640, 360)
    noStroke()
    global xpos1, xpos2, xpos3, xpos4
    xpos1 = width / 2
    xpos2 = width / 2
    xpos3 = width / 2
    xpos4 = width / 2


def draw():
    background(0)

    mx = mouseX * 0.4 - width / 5.0

    global xpos1, xpos2, xpos3, xpos4
    fill(102)
    rect(xpos2, 0, thick, height / 2)
    fill(204)
    rect(xpos1, 0, thin, height / 2)
    fill(102)
    rect(xpos4, height / 2, thick, height / 2)
    fill(204)
    rect(xpos3, height / 2, thin, height / 2)

    xpos1 += mx / 16
    xpos2 += mx / 64
    xpos3 -= mx / 16
    xpos4 -= mx / 64

    if(xpos1 < -thin):
        xpos1 = width
    if(xpos1 > width):
        xpos1 = -thin
    if(xpos2 < -thick):
        xpos2 = width
    if(xpos2 > width):
        xpos2 = -thick
    if(xpos3 < -thin):
        xpos3 = width
    if(xpos3 > width):
        xpos3 = -thin
    if(xpos4 < -thick):
        xpos4 = width
    if(xpos4 > width):
        xpos4 = -thick

