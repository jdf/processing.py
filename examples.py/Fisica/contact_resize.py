"""
 *    ContactRemove
 *
 *    by Ricard Marxer
 *
 *    This example shows how to use the contact events in order to remove bodies.
 """
from fisica import Fisica, FWorld, FCircle, FContact

world = None

def setup():
    global world
    size(400, 400)
    smooth()
    Fisica.init(this)
    world = FWorld()
    world.setGravity(0, 100)
    world.setEdges()

def draw():
    background(255)
    if frameCount % 50 == 0:
        sz = random(30, 60)
        b = FCircle(sz)
        b.setPosition(random(0+30, width-30), 50)
        b.setVelocity(0, 100)
        b.setRestitution(0.7)
        b.setDamping(0.01)
        b.setNoStroke()
        b.setFill(200, 30, 90)
        world.add(b)
    world.draw()
    world.step()

def contactEnded(c):
    for b in (c.getBody1(), c.getBody2()):
        if not b.isStatic() and b.getSize() > 5:
            b.setSize(b.getSize() * 0.9)

def keyPressed():
    saveFrame("screenshot.png")
