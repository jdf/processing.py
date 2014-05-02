"""
 * Pointillism
 * by Daniel Shiffman. 
 * 
 * Mouse horizontal location controls size of dots. 
 * Creates a simple pointillist effect using ellipses colored
 * according to pixels in an image. 
 """

smallPoint = 4
largePoint = 40

def setup():
    size(640, 360)
    global img
    img = loadImage("moonwalk.jpg")
    imageMode(CENTER)
    noStroke()
    background(255)


def draw():
    pointillize = map(mouseX, 0, width, smallPoint, largePoint)
    x = int(random(img.width))
    y = int(random(img.height))
    pix = img.get(x, y)
    fill(pix, 128)
    ellipse(x, y, pointillize, pointillize)

