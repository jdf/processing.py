"""
Scrollbar.

Move the scrollbars left and right to change the positions of the images.
"""
from hscrollbar import HScrollbar

def setup():
    global hs1, hs2, img1, img2
    size(640, 360)
    noStroke()
    # Two scrollbars
    hs1 = HScrollbar(0, height / 2 - 8, width, 16, 16)
    hs2 = HScrollbar(0, height / 2 + 8, width, 16, 16)
    # Load images
    img1 = loadImage("seedTop.jpg")
    img2 = loadImage("seedBottom.jpg")


def draw():
    background(255)
    # Get the position of the img1 scrollbar
    # and convert to a value to display the img1 image.
    img1Pos = hs1.getPos() - width / 2
    fill(255)
    image(img1, width / 2 - img1.width / 2 + img1Pos * 1.5, 0)
    # Get the position of the img2 scrollbar
    # and convert to a value to display the img2 image.
    img2Pos = hs2.getPos() - width / 2
    fill(255)
    image(img2, width / 2 - img2.width / 2 + img2Pos * 1.5, height / 2)
    hs1.update()
    hs2.update()
    hs1.display()
    hs2.display()
    stroke(0)
    line(0, height / 2, width, height / 2)
