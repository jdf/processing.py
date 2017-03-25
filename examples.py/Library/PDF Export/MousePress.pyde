"""
Mouse Press. 

Saves one PDF of the contents of the display window 
each time the mouse is pressed.
"""


add_library('pdf')

saveOneFrame = False


def setup():
    size(600, 600)
    frameRate(24)


def draw():
    global saveOneFrame
    if saveOneFrame:
        beginRecord(PDF, "Line.pdf")

    background(255)
    stroke(0, 20)
    strokeWeight(20.0)
    line(mouseX, 0, width - mouseY, height)

    if saveOneFrame:
        endRecord()
        saveOneFrame = False


def mousePressed():
    global saveOneFrame
    saveOneFrame = True
