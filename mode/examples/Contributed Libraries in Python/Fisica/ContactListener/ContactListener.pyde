"""
Contacts
by Ricard Marxer
(Adapted for Python by Jonathan Feinberg.)
 
This example shows how to use contact events.
"""
add_library('fisica')


class ContactListener(FContactAdapter):

    """Demonstration of implementing FContactListener by subclassing
       FContactAdapter."""

    def __init__(self, obstacle):
        self.obstacle = obstacle

    def getContactedBall(self, c):
        if c.getBody1() == self.obstacle:
            return c.getBody2()
        if c.getBody2() == self.obstacle:
            return c.getBody1()
        return None

    def contactStarted(self, c):
        ball = self.getContactedBall(c)
        if ball:
            ball.setFill(30, 190, 200)

    def contactPersisted(self, c):
        ball = self.getContactedBall(c)
        if ball:
            ball.setFill(30, 120, 200)
            noStroke()
            fill(255, 220, 0)
            ellipse(c.getX(), c.getY(), 10, 10)

    def contactEnded(self, c):
        ball = self.getContactedBall(c)
        if ball:
            ball.setFill(200, 30, 90)


def setup():
    size(400, 400)
    smooth()
    Fisica.init(this)
    global world
    world = FWorld()
    global obstacle
    obstacle = FBox(150, 150)
    obstacle.setRotation(PI / 4)
    obstacle.setPosition(width / 2, height / 2)
    obstacle.setStatic(True)
    obstacle.setFill(0)
    obstacle.setRestitution(0)
    world.add(obstacle)
    world.setContactListener(ContactListener(obstacle))


def draw():
    background(255)
    if frameCount % 5 == 0:
        b = FCircle(20)
        b.setPosition(width / 2 + random(-50, 50), 50)
        b.setVelocity(0, 200)
        b.setRestitution(0)
        b.setNoStroke()
        b.setFill(200, 30, 90)
        world.add(b)
    world.draw()
    world.step()
    strokeWeight(1)
    stroke(255)
    for c in obstacle.getContacts():
        line(c.getBody1().getX(), c.getBody1().getY(),
             c.getBody2().getX(), c.getBody2().getY())

