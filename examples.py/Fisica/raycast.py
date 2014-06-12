"""
 *    Raycast
 *
 *    by Ricard Marxer
 *
 *    This example shows how to use the raycasts.
 """
from fisica import Fisica, FWorld, FBody, FBox, FRaycastResult

#import org.jbox2d.common.*

world, obstacle = None, None

def setup():
    global world, obstacle
    size(400, 400)
    smooth()
    Fisica.init(this)
    world = FWorld()
    obstacle = FBox(150,150)
    obstacle.setRotation(PI/4)
    obstacle.setPosition(width/2, height/2)
    obstacle.setStatic(True)
    obstacle.setFill(0)
    obstacle.setRestitution(0)
    world.add(obstacle)

def draw():
    background(255)
    world.draw()
    world.step()

    castRay()

def castRay():
    result = FRaycastResult()
    b = world.raycastOne(width/2, height, mouseX, mouseY, result, True)
    stroke(0)
    line(width/2, height, mouseX, mouseY)
    if b:
        b.setFill(120, 90, 120)
        fill(180, 20, 60)
        noStroke()

        x = result.getX()
        y = result.getY()
        ellipse(x, y, 10, 10)
    else:
        obstacle.setFill(0)

def keyPressed():
    saveFrame("screenshot.png")
