"""
Mouse Signals. 
  
Move and click the mouse to generate signals. 
The top row is the signal from "mouseX", 
the middle row is the signal from "mouseY",
and the bottom row is the signal from "mousePressed". 
"""


def setup():
    size(640, 360)
    noSmooth()
    global xvals, yvals, bvals
    xvals = [0 for i in range(width)]
    yvals = [0 for i in range(width)]
    bvals = [0 for i in range(width)]


def draw():
    background(102)
    global xvals, yvals, bvals

    for i in range(1, width, 1):
        xvals[i - 1] = xvals[i]
        yvals[i - 1] = yvals[i]
        bvals[i - 1] = bvals[i]

    xvals[width - 1] = mouseX
    yvals[width - 1] = mouseY

    if(mousePressed):
        bvals[width - 1] = 0
    else:
        bvals[width - 1] = 255

    fill(255)
    noStroke()
    rect(0, height / 3, width, height / 3 + 1)

    for i in range(1, width, 1):
        stroke(255)
        point(i, xvals[i] / 3)
        stroke(0)
        point(i, height / 3 + yvals[i] / 3)
        stroke(255)
        line(i, 2 * height / 3 + bvals[i] / 3,
             i, (2 * height / 3 + bvals[i - 1] / 3))

