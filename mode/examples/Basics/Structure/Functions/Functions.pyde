"""
 * Functions. 
 * 
 * The drawTarget() function makes it easy to draw many distinct targets. 
 * Each call to drawTarget() specifies the position, size, and number of 
 * rings for each target. 
"""


def setup():
    size(640, 360)
    background(51)
    noStroke()
    noLoop()


def draw():
    drawTarget(width * 0.25, height * 0.4, 200, 4)
    drawTarget(width * 0.5, height * 0.5, 300, 10)
    drawTarget(width * 0.75, height * 0.3, 120, 6)


def drawTarget(xloc, yloc, size, num):
    grayvalues = 255 / num
    steps = size / num
    for i in range(num):
        fill(i * grayvalues)
        ellipse(xloc, yloc, size - i * steps, size - i * steps)

