"""
 *    Anchors and the bridge
 *
 *    by Ricard Marxer
 *
 *    This example shows the use of anchors and distance joints in order
 *    to create a bridge.
 """
from fisica import Fisica, FBody, FBox, FWorld, FCircle, FDistanceJoint

frequency = 5
damping = 1
puenteY = None
stepCount = 20
steps = []
world = []
boxWidth = 400/stepCount - 2

def setup():
    global puenteY, world

    size(400, 400)
    smooth()
    puenteY = height/3
    Fisica.init(this)
    world = FWorld()
    bola = FCircle(40)
    bola.setPosition(width/3, puenteY-10)
    bola.setDensity(0.2)
    bola.setFill(120, 120, 190)
    bola.setNoStroke()
    world.add(bola)
    for i in range(stepCount):
        box = FBox(boxWidth, 10)
        box.setPosition(map(i, 0, stepCount - 1, boxWidth, width-boxWidth), puenteY)
        box.setNoStroke()
        box.setFill(120, 200, 190)
        world.add(box)
        steps.append(box)
    for i in range(1, stepCount):
        junta = FDistanceJoint(steps[i-1], steps[i])
        junta.setAnchor1(boxWidth/2, 0)
        junta.setAnchor2(-boxWidth/2, 0)
        junta.setFrequency(frequency)
        junta.setDamping(damping)
        junta.setFill(0)
        junta.calculateLength()
        world.add(junta)
    left = FCircle(10)
    left.setStatic(True)
    left.setPosition(0, puenteY)
    left.setDrawable(False)
    world.add(left)
    right = FCircle(10)
    right.setStatic(True)
    right.setPosition(width, puenteY)
    right.setDrawable(False)
    world.add(right)
    juntaPrincipio = FDistanceJoint(steps[0], left)
    juntaPrincipio.setAnchor1(-boxWidth/2, 0)
    juntaPrincipio.setAnchor2(0, 0)
    juntaPrincipio.setFrequency(frequency)
    juntaPrincipio.setDamping(damping)
    juntaPrincipio.calculateLength()
    juntaPrincipio.setFill(0)
    world.add(juntaPrincipio)
    juntaFinal = FDistanceJoint(steps[stepCount-1], right)
    juntaFinal.setAnchor1(boxWidth/2, 0)
    juntaFinal.setAnchor2(0, 0)
    juntaFinal.setFrequency(frequency)
    juntaFinal.setDamping(damping)
    juntaFinal.calculateLength()
    juntaFinal.setFill(0)
    world.add(juntaFinal)

def draw():
    background(255)
    world.step()
    world.draw()

def mousePressed():
    radius = random(10, 40)
    bola = FCircle(radius)
    bola.setPosition(mouseX, mouseY)
    bola.setDensity(0.2)
    bola.setFill(120, 120, 190)
    bola.setNoStroke()
    world.add(bola)

def keyPressed():
    saveFrame("screenshot.png")
