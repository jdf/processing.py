"""
Loading Images. 
"""

def setup():
    size(640, 360)
    global img
    img = loadImage("http://processing.org/img/processing-web.png")
    noLoop()


def draw():
    background(0)
    for i in range(5):
        image(img, 0, img.height * i)

