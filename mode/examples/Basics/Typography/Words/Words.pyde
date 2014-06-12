"""
 * Words. 
 * 
 * The text() function is used for writing words to the screen.
 * The letters can be aligned left, center, or right with the 
 * textAlign() function. 
 """


def setup():
    size(640, 360)

    # Create the font
    printArray(PFont.list())
    f = createFont("Georgia", 24)
    textFont(f)


def draw():
    background(102)
    textAlign(RIGHT)
    drawType(width * 0.25)
    textAlign(CENTER)
    drawType(width * 0.5)
    textAlign(LEFT)
    drawType(width * 0.75)


def drawType(x):
    line(x, 0, x, 65)
    line(x, 220, x, height)
    fill(0)
    text("ichi", x, 95)
    fill(51)
    text("ni", x, 130)
    fill(204)
    text("san", x, 165)
    fill(255)
    text("shi", x, 210)

