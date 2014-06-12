"""
Blending 
by Andres Colubri. 

Images can be blended using one of the 10 blending modes 
(currently available only in P2D and P3).
Click to go to cycle through the modes.    
"""

img1 = None
img2 = None
picAlpha = 255
modes = ((REPLACE, "REPLACE"),
         (BLEND, "BLEND"),
         (ADD, "ADD"),
         (SUBTRACT, "SUBTRACT"),
         (LIGHTEST, "LIGHTEST"),
         (DARKEST, "DARKEST"),
         (DIFFERENCE, "DIFFERENCE"),
         (EXCLUSION, "EXCLUSION"),
         (MULTIPLY, "MULTIPLY"),
         (SCREEN, "SCREEN"),
         (REPLACE, "REPLACE"))
currentMode = 0


def setup():
    size(640, 360, P3D)
    img1 = loadImage("layer1.jpg")
    img2 = loadImage("layer2.jpg")
    noStroke()


def draw():
    selMode, name = modes[currentMode]
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
    currentMode = (currentMode + 1) % len(modes)


def mouseDragged():
    if height - 50 < mouseY:
        picAlpha = int(map(mouseX, 0, width, 0, 255))

