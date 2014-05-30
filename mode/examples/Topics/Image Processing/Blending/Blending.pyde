"""
Blending 
by Andres Colubri. 

Images can be blended using one of the 10 blending modes 
(currently available only in P2D and P3).
Click to go to cycle through the modes.    
"""

img1 = None
img2 = None
selMode = REPLACE
name = "REPLACE"
picAlpha = 255


def setup():
    size(640, 360, P3D)
    img1 = loadImage("layer1.jpg")
    img2 = loadImage("layer2.jpg")
    noStroke()


def draw():
    picAlpha = int(map(mouseX, 0, width, 0, 255))
    background(0)
    tint(255, 255)
    image(img1, 0, 0)
    blendMode(selMode)
    tint(255, picAlpha)
    image(img2, 0, 0)
    blendMode(REPLACE)
    fill(255)
    rect(0, 0, 94, 22)
    fill(0)
    text(name, 10, 15)


def mousePressed():
    if selMode == REPLACE:
        selMode = BLEND
        name = "BLEND"
    elif selMode == BLEND:
        selMode = ADD
        name = "ADD"
    elif selMode == ADD:
        selMode = SUBTRACT
        name = "SUBTRACT"
    elif selMode == SUBTRACT:
        selMode = LIGHTEST
        name = "LIGHTEST"
    elif selMode == LIGHTEST:
        selMode = DARKEST
        name = "DARKEST"
    elif selMode == DARKEST:
        selMode = DIFFERENCE
        name = "DIFFERENCE"
    elif selMode == DIFFERENCE:
        selMode = EXCLUSION
        name = "EXCLUSION"
    elif selMode == EXCLUSION:
        selMode = MULTIPLY
        name = "MULTIPLY"
    elif selMode == MULTIPLY:
        selMode = SCREEN
        name = "SCREEN"
    elif selMode == SCREEN:
        selMode = REPLACE
        name = "REPLACE"


def mouseDragged():
    if height - 50 < mouseY:
        picAlpha = int(map(mouseX, 0, width, 0, 255))

