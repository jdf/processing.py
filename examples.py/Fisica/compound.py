"""
 *    Compound
 *
 *    by Ricard Marxer
 *
 *    This example shows how to create compound bodies
 *    which are bodies made of multiple shapes.
 """
from fisica import Fisica, FWorld, FCompound, FCircle, FBox

world, pop, cage = None, None, None

def setup():
    global world, pop, cage
    size(400, 400)
    smooth()
    Fisica.init(this)
    Fisica.setScale(10)
    world = FWorld()
    world.setEdges()
    world.remove(world.top)
    pop = createPop()
    pop.setPosition(width/2, height/2)
    pop.setBullet(True)
    world.add(pop)
    cage = createCage()
    cage.setPosition(width/2, height/2)
    cage.setRotation(PI/6)
    cage.setBullet(True)
    world.add(cage)

    for _ in range(10):
        c = FCircle(7)
        c.setPosition(width/2-10+random(-5, 5), height/2-10+random(-5, 5))
        c.setBullet(True)
        c.setNoStroke()
        c.setFillColor(color(0xFF, 0x92, 0x03))
        world.add(c)

    rectMode(CENTER)

def draw():
    background(255)
    world.step()
    world.draw()

def createPop():
    b = FBox(6, 60)
    b.setFillColor(color(0x1F, 0x71, 0x6B))
    b.setNoStroke()
    c = FCircle(20)
    c.setPosition(0, -30)
    c.setFillColor(color(0xFF, 0x00, 0x51))
    c.setNoStroke()

    result = FCompound()
    result.addBody(b)
    result.addBody(c)

    return result

def createCage():
    b1 = FBox(10, 110)
    b1.setPosition(50, 0)
    b1.setFill(0)
    b1.setNoStroke()
    b2 = FBox(10, 110)
    b2.setPosition(-50, 0)
    b2.setFill(0)
    b2.setNoStroke()

    b3 = FBox(110, 10)
    b3.setPosition(0, 50)
    b3.setFill(0)
    b3.setNoStroke()

    b4 = FBox(110, 10)
    b4.setPosition(0, -50)
    b4.setFill(0)
    b4.setNoStroke()

    result = FCompound()
    result.addBody(b1)
    result.addBody(b2)
    result.addBody(b3)
    result.addBody(b4)
    return result

def keyPressed():
    saveFrame("screenshot.png")
