"""
Zoom. 

Move the cursor over the image to alter its position. Click and press
the mouse to zoom. This program displays a series of lines with their 
heights corresponding to a color value read from an image. 
"""
img = None
imgPixels = None
sval = 1.0
nmx = 0
nmy = 0
res = 5


def setup():
    size(640, 360, P3D)
    noFill()
    stroke(255)
    img = loadImage("ystone08.jpg")
    imgPixels = [[0]*img.width for i in range(img.height)]
    for i in range(img.height):
        for j in range(img.width):
            imgPixels[j][i] = img.get(j, i)


def draw():
    background(0)
    nmx += (mouseX - nmx) / 20
    nmy += (mouseY - nmy) / 20
    if mousePressed:
        sval += 0.005
    else:
        sval -= 0.01
    sval = constrain(sval, 1.0, 2.0)
    translate(width / 2 + nmx * sval - 100, height / 2 + nmy * sval - 100, -50)
    scale(sval)
    rotateZ(PI / 9 - sval + 1.0)
    rotateX(PI / sval / 8 - 0.125)
    rotateY(sval / 8 - 0.125)
    translate(-width / 2, -height / 2, 0)
    for i in range(0, img.height, res):
        for j in range(0, img.width, res):
            rr = red(imgPixels[j][i])
            gg = green(imgPixels[j][i])
            bb = blue(imgPixels[j][i])
            tt = rr + gg + bb
            stroke(rr, gg, gg)
            line(i, j, tt / 10 - 20, i, j, tt / 10)

