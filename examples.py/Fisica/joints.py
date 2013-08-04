"""
 *    Joints
 *
 *    by Ricard Marxer
 *
 *    This example shows how to access all the joints of a given body.
 """
from fisica import Fisica, FWorld, FCircle, FDistanceJoint, FJoint

bodyColor = color(0x6E, 0x05, 0x95)
hoverColor = color(0xF5, 0xB5, 0x02)
spiderCount = 10
mainSize = 40
legCount = 10
legSize = 100

world = None
mains = []

def setup():
    global world
    size(400, 400)
    smooth()
    Fisica.init(this)
    world = FWorld()
    world.setEdges()
    world.setGravity(0, 0)
    for _ in range(spiderCount):
        createSpider()

def draw():
    background(255)
    world.step()
    world.draw()

def mouseMoved():
    hovered = world.getBody(mouseX, mouseY)
    for other in mains:
        if hovered == other:
            setJointsDrawable(other, True)
            setJointsColor(other, hoverColor)
        else:
            setJointsDrawable(other, False)
            setJointsColor(other, bodyColor)

def keyPressed():
    saveFrame("screenshot.png")

def createSpider():
    posX = random(mainSize/2, width-mainSize/2)
    posY = random(mainSize/2, height-mainSize/2)
    main = FCircle(mainSize)
    main.setPosition(posX, posY)
    main.setVelocity(random(-20,20), random(-20,20))
    main.setFillColor(bodyColor)
    main.setNoStroke()
    main.setGroupIndex(2)
    world.add(main)
    mains.append(main)
    for i in range(legCount):
        x = legSize * cos(i*TWO_PI/3) + posX
        y = legSize * sin(i*TWO_PI/3) + posY
        leg = FCircle(mainSize/2)
        leg.setPosition(posX, posY)
        leg.setVelocity(random(-20,20), random(-20,20))
        leg.setFillColor(bodyColor)
        leg.setNoStroke()
        world.add(leg)
        j = FDistanceJoint(main, leg)
        j.setLength(legSize)
        j.setNoStroke()
        j.setStroke(0)
        j.setFill(0)
        j.setDrawable(False)
        j.setFrequency(0.1)
        world.add(j)

def setJointsColor(b, c):
    for j in b.getJoints():
        j.setStrokeColor(c)
        j.setFillColor(c)
        j.getBody1().setFillColor(c)
        j.getBody2().setFillColor(c)

def setJointsDrawable(b, c):
    for j in b.getJoints():
        j.setDrawable(c)
