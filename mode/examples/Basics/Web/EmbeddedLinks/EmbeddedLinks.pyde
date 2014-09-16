"""
Loading URLs. 

Click on the left button to open a different URL in the same window (Only
works online). Click on the right button to open a URL in a browser window.    
"""
overLeftButton = False
overRightButton = False


def setup():
    size(640, 360)


def draw():
    background(204)

    # Left button
    if overLeftButton:
        fill(255)
    else:
        noFill()

    rect(20, 60, 75, 75)
    rect(50, 90, 15, 15)

    # Right button
    if overRightButton:
        fill(255)
    else:
        noFill()

    rect(105, 60, 75, 75)
    line(135, 105, 155, 85)
    line(140, 85, 155, 85)
    line(155, 85, 155, 100)


def mousePressed():
    if overLeftButton:
        link("http://www.processing.org")
    elif overRightButton:
        link("http://www.processing.org", "_new")


def mouseMoved():
    checkButtons()


def mouseDragged():
    checkButtons()


def checkButtons():
    global overLeftButton, overRightButton
    overLeftButton = 20 < mouseX < 95 and 60 < mouseY < 135;
    overRightButton = 105 < mouseX < 180 and 60 < mouseY < 135;

