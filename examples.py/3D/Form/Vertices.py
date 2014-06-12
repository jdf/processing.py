"""
  Vertices
  by Simon Greenwold.
  (Rewritten in Python by Jonathan Feinberg.)

  Draw a cylinder centered on the y-axis, going down
  from y=0 to y=height. The radius at the top can be
  different from the radius at the bottom, and the
  number of sides drawn is variable.
 """
def setup():
    size(640, 360, P3D)

def draw():
    background(0)
    lights()
    translate(width / 2, height / 2)
    rotateY(map(mouseX, 0, width, 0, PI))
    rotateZ(map(mouseY, 0, height, 0, -PI))
    noStroke()
    fill(255, 255, 255)
    translate(0, -40, 0)
    drawCylinder(10, 180, 200, 16) # Draw a mix between a cylinder and a cone
    #drawCylinder(70, 70, 120, 64) # Draw a cylinder
    #drawCylinder(0, 180, 200, 4) # Draw a pyramid

def drawCylinder(topRadius, bottomRadius, tall, sides):
    angle = 0
    angleIncrement = TWO_PI / sides
    beginShape(QUAD_STRIP)
    for i in range(sides + 1):
        vertex(topRadius * cos(angle), 0, topRadius * sin(angle))
        vertex(bottomRadius * cos(angle), tall, bottomRadius * sin(angle))
        angle += angleIncrement
    endShape()

    # If it is not a cone, draw the circular top cap
    if topRadius:
        angle = 0
        beginShape(TRIANGLE_FAN)
        # Center point
        vertex(0, 0, 0)
        for i in range(sides + 1):
            vertex(topRadius * cos(angle), 0, topRadius * sin(angle))
            angle += angleIncrement
        endShape()

    # If it is not a cone, draw the circular bottom cap
    if bottomRadius:
        angle = 0
        beginShape(TRIANGLE_FAN)
        # Center point
        vertex(0, tall, 0)
        for i in range(sides + 1):
            vertex(bottomRadius * cos(angle), tall, bottomRadius * sin(angle))
            angle += angleIncrement
        endShape()
