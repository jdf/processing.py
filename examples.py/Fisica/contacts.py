"""
/**
 *  Contacts
 *
 *  by Ricard Marxer
 *
 *  This example shows how to use the contact events.
 */
"""
import fisica

world = None
obstacle = None

def setup():
  global world, obstacle
  size(400, 400)
  smooth()

  fisica.Fisica.init(this)

  world = fisica.FWorld()

  obstacle = fisica.FBox(150,150)
  obstacle.setRotation(PI/4)
  obstacle.setPosition(width/2, height/2)
  obstacle.setStatic(True)
  obstacle.setFill(0)
  obstacle.setRestitution(0)
  world.add(obstacle)

def draw():
  background(255)

  if frameCount % 5 == 0:
    b = fisica.FCircle(20)
    b.setPosition(width/2 + random(-50, 50), 50)
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
    line(c.getBody1().getX(), c.getBody1().getY(), c.getBody2().getX(), c.getBody2().getY())

def contactStarted(c):
  ball = None
  if c.getBody1() == obstacle:
    ball = c.getBody2()
  elif c.getBody2() == obstacle:
    ball = c.getBody1()
  if ball:
    ball.setFill(30, 190, 200)

def contactPersisted(c):
  ball = None
  if c.getBody1() == obstacle:
    ball = c.getBody2()
  elif c.getBody2() == obstacle:
    ball = c.getBody1()
  if not ball:
    return

  ball.setFill(30, 120, 200)
  noStroke()
  fill(255, 220, 0)
  ellipse(c.getX(), c.getY(), 10, 10)

def contactEnded(c):
  ball = None
  if c.getBody1() == obstacle:
    ball = c.getBody2()
  elif c.getBody2() == obstacle:
    ball = c.getBody1()
  if ball:
    ball.setFill(200, 30, 90)

def keyPressed():
  saveFrame("screenshot.png")
