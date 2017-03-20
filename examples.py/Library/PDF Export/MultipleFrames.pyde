"""
Multiple Frames.

Saves one PDF document of many frames drawn to the screen.
Starts the file when the mouse is pressed and end the file
when the mouse is released.
"""

add_library('pdf')  # import processing.pdf.*

def setup():
    size(600, 600)
    frameRate(24)
    background(255)

def draw():
    stroke(0, 20)
    strokeWeight(20.0)
    line(mouseX, 0, width - mouseY, height)

def mousePressed():
    beginRecord(PDF, "Lines.pdf")
    background(255)

def mouseReleased():
    endRecord()
    background(255)
