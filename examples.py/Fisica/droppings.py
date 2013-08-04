"""
 *    Droppings Remade
 *
 *    This example shows how to create a simple remake of my favorite
 *    soundtoy:<br/>
 *
 *        <a href=http:#www.balldroppings.com/>BallDroppings</a>
 *             by Josh Nimoy.
 """

from fisica import FWorld, Fisica, FCircle, FBody, FBox

mundo, caja = None, None
x, y = 0, 0

def setup():
    global mundo
    size(400, 400)
    smooth()

    Fisica.init(this)
    mundo = FWorld()
    mundo.setGravity(0, 200)

    frameRate(24)
    background(0)

def draw():
    fill(0, 100)
    noStroke()
    rect(0, 0, width, height)
    if frameCount % 24 == 0:
        bolita = FCircle(8)
        bolita.setNoStroke()
        bolita.setFill(255)
        bolita.setPosition(100, 20)
        bolita.setVelocity(0, 400)
        bolita.setRestitution(0.9)
        bolita.setDamping(0)
        mundo.add(bolita)
    mundo.step()
    mundo.draw(this)

def mousePressed():
    global caja, x, y
    caja = FBox(4, 4)
    caja.setStaticBody(True)
    caja.setStroke(255)
    caja.setFill(255)
    caja.setRestitution(0.9)
    mundo.add(caja)

    x = mouseX
    y = mouseY

def mouseDragged():
    if not caja:
        return
    ang = atan2(y - mouseY, x - mouseX)
    caja.setRotation(ang)
    caja.setPosition(x+(mouseX-x)/2.0, y+(mouseY-y)/2.0)
    caja.setWidth(dist(mouseX, mouseY, x, y))

def contactStarted(contacto):
    cuerpo1 = contacto.getBody1()
    cuerpo1.setFill(255, 0, 0)
    cuerpo1.setStroke(255, 0, 0)

    noFill()
    stroke(255)
    ellipse(contacto.getX(), contacto.getY(), 30, 30)

def contactEnded(contacto):
    cuerpo1 = contacto.getBody1()
    cuerpo1.setFill(255)
    cuerpo1.setStroke(255)

def keyPressed():
    saveFrame("screenshot.png")
