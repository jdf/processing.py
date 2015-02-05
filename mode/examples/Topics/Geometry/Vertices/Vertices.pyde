"""
Vertices
by Simon Greenwold.

Draw a cylinder centered on the y - axis, going down from y = 0 to y = height.
The radius at the top can be different from the radius at the bottom, and the
number of sides drawn is variable.
"""

def setup():
    global halfWidth, halfHeight
    size(640, 360, P3D)
    halfWidth = width / 2
    halfHeight = height / 2


def draw():
    background(0)
    lights()
    translate(halfWidth, halfHeight)
    rotateY(map(mouseX, 0, width, 0, PI))
    rotateZ(map(mouseY, 0, height, 0, -PI))
    noStroke()
    fill(255, 255, 255)
    translate(0, -40, 0)
    # Draw a mix between a cylinder and a cone.
    drawCylinder(10, 180, 200, 16)
    # Draw a cylinder.
    # drawCylinder(70, 70, 120, 64)
    # Draw a pyramid.
    # drawCylinder(0, 180, 200, 4)


def drawCylinder(topRadius, bottomRadius, tall, sides):
    angle = 0
    angleIncrement = TAU / sides

    with beginShape(QUAD_STRIP):
        for _ in range(sides + 1):
            vertex(topRadius * cos(angle), 0, topRadius * sin(angle))
            vertex(bottomRadius * cos(angle), tall, bottomRadius * sin(angle))
            angle += angleIncrement

    # If it is not a cone, draw the circular top cap.
    if topRadius != 0:
        angle = 0
        with beginShape(TRIANGLE_FAN):
            # Center point.
            vertex(0, 0, 0)
            for _ in range(sides + 1):
                vertex(topRadius * cos(angle), 0, topRadius * sin(angle))
                angle += angleIncrement

    # If it is not a cone, draw the circular bottom cap.
    if bottomRadius != 0:
        angle = 0
        with beginShape(TRIANGLE_FAN):
            # Center point.
            vertex(0, tall, 0)
            for _ in range(sides + 1):
                vertex(bottomRadius * cos(angle), tall, bottomRadius * sin(angle))
                angle += angleIncrement
