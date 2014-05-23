"""
Continuous Lines. 

Click and drag the mouse to draw a line. 
"""


def setup():
    size(640, 360)
    background(102)


def draw():
    stroke(255)
    if mousePressed == True:
        line(mouseX, mouseY, pmouseX, pmouseY)

