"""
 *    Buttons and bodies
 *
 *    by Ricard Marxer
 *
 *    This example shows how to create bodies.
 *    It also demonstrates the use of bodies as buttons.
 """
from fisica import Fisica, FWorld, FBox, FCircle, FPoly

boxButton = None
circleButton = None
polyButton = None
world = None
buttonColor = color(0x15, 0x5A, 0xAD)
hoverColor = color(0x55, 0xAA, 0x11)
bodyColor = color(0x6E, 0x05, 0x95)

def setup():
    global boxButton, circleButton, polyButton, world

    size(400, 400)
    smooth()
    Fisica.init(this)
    world = FWorld()
    world.setEdges()
    world.remove(world.left)
    world.remove(world.right)
    world.remove(world.top)
    boxButton = FBox(40, 40)
    boxButton.setPosition(width/4, 100)
    boxButton.setStatic(True)
    boxButton.setFillColor(buttonColor)
    boxButton.setNoStroke()
    world.add(boxButton)
    circleButton = FCircle(40)
    circleButton.setPosition(2*width/4, 100)
    circleButton.setStatic(True)
    circleButton.setFillColor(buttonColor)
    circleButton.setNoStroke()
    world.add(circleButton)
    polyButton = FPoly()
    polyButton.vertex(20, 20)
    polyButton.vertex(-20, 20)
    polyButton.vertex(0, -20)
    polyButton.setPosition(3*width/4, 100)
    polyButton.setStatic(True)
    polyButton.setFillColor(buttonColor)
    polyButton.setNoStroke()
    world.add(polyButton)

def draw():
    background(255)
    world.step()
    world.draw()

def mousePressed():
    pressed = world.getBody(mouseX, mouseY)
    if pressed == boxButton:
        myBox = FBox(40, 40)
        myBox.setPosition(width/4, 200)
        myBox.setRotation(random(TWO_PI))
        myBox.setVelocity(0, 200)
        myBox.setFillColor(bodyColor)
        myBox.setNoStroke()
        world.add(myBox)
    elif pressed == circleButton:
        myCircle = FCircle(40)
        myCircle.setPosition(2*width/4, 200)
        myCircle.setRotation(random(TWO_PI))
        myCircle.setVelocity(0, 200)
        myCircle.setFillColor(bodyColor)
        myCircle.setNoStroke()
        world.add(myCircle)
    elif pressed == polyButton:
        myPoly = FPoly()
        myPoly.vertex(20, 20)
        myPoly.vertex(-20, 20)
        myPoly.vertex(0, -20)
        myPoly.setPosition(3*width/4, 200)
        myPoly.setRotation(random(TWO_PI))
        myPoly.setVelocity(0, 200)
        myPoly.setFillColor(bodyColor)
        myPoly.setNoStroke()
        world.add(myPoly)

def mouseMoved():
    hovered = world.getBody(mouseX, mouseY)
    if hovered in (boxButton, circleButton, polyButton):
        hovered.setFillColor(hoverColor)
    else:
        boxButton.setFillColor(buttonColor)
        circleButton.setFillColor(buttonColor)
        polyButton.setFillColor(buttonColor)

def keyPressed():
    saveFrame("screenshot.png")
