"""
Tile Images

Draws an image larger than the screen, and saves the image as six tiles.
The scaleValue variable sets amount of scaling: 1 is 100%, 2 is 200%, etc.
"""

scaleValue = 3  # Multiplication factor
xoffset = 0     # x-axis offset
yoffset = 0     # y-axis offset


def setup():
    size(600, 600)
    stroke(0, 100)


def draw():
    background(204)
    scale(scaleValue)
    translate(xoffset * (-width / scaleValue),
              yoffset * (-height / scaleValue))
    line(10, 150, 500, 50)
    line(0, 600, 600, 0)
    save("lines-" + str(yoffset) + "-" + str(xoffset) + ".png")
    setOffset()


def setOffset():
    global xoffset
    global yoffset

    xoffset += 1
    if xoffset == scaleValue:
        xoffset = 0
        yoffset += 1
        if yoffset == scaleValue:
            print "Tiles saved."
            exit()
