"""
 *    Restitutions
 *
 *    by Ricard Marxer
 *
 *    This example shows how the restitution coefficients works.
 """
from fisica import Fisica, FWorld, FCircle

world = None

ballCount = 10

def setup():
    global world
    size(400, 400)
    smooth()
    Fisica.init(this)
    world = FWorld()
    world.setEdges()
    world.remove(world.left)
    world.remove(world.right)
    world.remove(world.top)
    world.setEdgesRestitution(0.0)
    for i in range(ballCount):
        b = FCircle(25)
        b.setPosition(map(i, 0, ballCount-1, 40, width-40), height/6)
        b.setRestitution(map(i, 0, ballCount-1, 0.0, 1.0))
        b.setNoStroke()
        b.setFill(map(i, 0, ballCount-1, 60, 255), 80, 120)
        world.add(b)

def draw():
    background(255)
    world.step()
    world.draw()

def keyPressed():
    saveFrame("screenshot.png")
