def setup():
    size(400, 400, P3D)
    noLoop()


def draw():
    background(255, 0, 0)
    ellipse(mouseX, mouseY, 100, 50)
    print "draw"


def keyPressed():
    redraw()
