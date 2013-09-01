"""
 *    Buttons and bodies
 *
 *    by Ricard Marxer
 *
 *    This example shows how to create a blob.
 """
from fisica import Fisica, FWorld, FPoly, FBlob

world = None
xPos = 0

circleCount = 20
hole = 50
topMargin = 50
bottomMargin = 300
sideMargin = 100

def setup():
    global world

    size(400, 400)
    smooth()
    Fisica.init(this)
    world = FWorld()
    world.setGravity(0, -300)
    l = FPoly()
    l.vertex(width/2-hole/2, 0)
    l.vertex(0, 0)
    l.vertex(0, height)
    l.vertex(0+sideMargin, height)
    l.vertex(0+sideMargin, height-bottomMargin)
    l.vertex(width/2-hole/2, topMargin)
    l.setStatic(True)
    l.setFill(0)
    l.setFriction(0)
    world.add(l)
    r = FPoly()
    r.vertex(width/2+hole/2, 0)
    r.vertex(width, 0)
    r.vertex(width, height)
    r.vertex(width-sideMargin, height)
    r.vertex(width-sideMargin, height-bottomMargin)
    r.vertex(width/2+hole/2, topMargin)
    r.setStatic(True)
    r.setFill(0)
    r.setFriction(0)
    world.add(r)

def draw():
    global xPos
    background(80, 120, 200)
    if (frameCount % 40) == 1:
        b = FBlob()
        s = random(30, 40)
        space = (width-sideMargin*2-s)
        xPos = (xPos + random(s, space/2)) % space
        b.setAsCircle(sideMargin + xPos+s/2, height-random(100), s, 20)
        b.setStroke(0)
        b.setStrokeWeight(2)
        b.setFill(255)
        b.setFriction(0)
        world.add(b)
    world.step()
    world.draw()
