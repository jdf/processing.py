"""
Loading URLs. 

Click on the button to open a URL in a browser    
"""
overButton = False

def setup():
    size(640, 360)


def draw():
    background(204)

    if overButton:
        fill(255)
    else:
        noFill()

    rect(105, 60, 75, 75)
    line(135, 105, 155, 85)
    line(140, 85, 155, 85)
    line(155, 85, 155, 100)


def mousePressed():
    if overButton:
        link("http://www.processing.org")


def mouseMoved():
    checkButtons()


def mouseDragged():
    checkButtons()


def checkButtons():
    global overButton
    overButton = 105 < mouseX < 180 and 60 < mouseY < 135;
