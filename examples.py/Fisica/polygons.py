"""
 *    Polygons
 *
 *    by Ricard Marxer
 *
 *    This example shows how to create polygon bodies.
 """
from fisica import Fisica, FWorld, FPoly, FBody

world, poly = None, None

def setup():
    global world
    size(400, 400)
    smooth()
    Fisica.init(this)
    world = FWorld()
    world.setGravity(0, 800)
    world.setEdges()
    world.remove(world.left)
    world.remove(world.right)
    world.remove(world.top)

    world.setEdgesRestitution(0.5)

def draw():
    background(255)
    world.step()
    world.draw(this)
    # Draw the polygon while
    # while it is being created
    # and hasn't been added to the
    # world yet
    if poly:
        poly.draw(this)

def mousePressed():
    if world.getBody(mouseX, mouseY):
        return
    global poly
    poly = FPoly()
    poly.setStrokeWeight(3)
    poly.setFill(120, 30, 90)
    poly.setDensity(10)
    poly.setRestitution(0.5)
    poly.vertex(mouseX, mouseY)

def mouseDragged():
    if poly:
        poly.vertex(mouseX, mouseY)

def mouseReleased():
    global poly
    if poly:
        world.add(poly)
        poly = None

def keyPressed():
    if key == BACKSPACE:
        hovered = world.getBody(mouseX, mouseY)
        if hovered and not hovered.isStatic():
            world.remove(hovered)
    else:
        saveFrame("screenshot.png")
