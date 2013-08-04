"""
 *    ContactRemove
 *
 *    by Ricard Marxer
 *
 *    This example shows how to use the contact events in order to remove bodies.
 """
from fisica import Fisica, FWorld, FBox, FCircle, FBody, FContact

world, pala = None, None

def setup():
    global world, pala
    size(400, 400)
    smooth()
    Fisica.init(this)
    world = FWorld()
    pala = FBox(50, 20)
    pala.setPosition(width/2, height - 40)
    pala.setStatic(True)
    pala.setFill(0)
    pala.setRestitution(0)
    world.add(pala)

def draw():
    background(255)
    if frameCount % 8 == 0:
        b = FCircle(random(5, 20))
        b.setPosition(random(0+10, width-10), 50)
        b.setVelocity(0, 200)
        b.setRestitution(0)
        b.setNoStroke()
        b.setFill(200, 30, 90)
        world.add(b)
    pala.setPosition(mouseX, height - 40)
    world.draw()
    world.step()

def contactStarted(c):
    ball = None
    if c.getBody1() == pala:
        ball = c.getBody2()
    elif c.getBody2() == pala:
        ball = c.getBody1()
    if not ball:
        return
    ball.setFill(30, 190, 200)
    world.remove(ball)

def keyPressed():
    saveFrame("screenshot.png")
