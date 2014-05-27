"""
Loading Images. 

Processing applications can only load images from the network
while running in the Processing environment. 

This example will not run in a web broswer and will only work when 
the computer is connected to the Internet. 
"""

img = None


def setup():
    size(640, 360)
    img = loadImage("http://processing.org/img/processing-web.png")
    noLoop()


def draw():
    background(0)
    if img != None:
        for i in range(5):
            image(img, 0, img.height * i)

