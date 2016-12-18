"""
Soft Body 
by Ira Greenberg.    

Softbody dynamics simulation using curveVertex() and curveTightness().
"""

# center point
centerX = 0
centerY = 0
radius = 45
rotAngle = -90
accelX = 0
accelY = 0
springing = .0009
damping = .98
# Corner nodes
nodes = 5
nodeStartX = [0.0] * nodes
nodeStartY = [0.0] * nodes
nodeX = [0.0] * nodes
nodeY = [0.0] * nodes
angle = [0.0] * nodes
frequency = [0.0] * nodes
# Soft-body dynamics
organicConstant = 1


def setup():
    size(640, 360)
    # Center shape in window.
    centerX = width / 2
    centerY = height / 2
    # Initialize frequencies for corner nodes.
    for i in range(nodes):
        frequency[i] = random(5, 12)
    noStroke()
    frameRate(30)


def draw():
    # fade background
    fill(0, 100)
    rect(0, 0, width, height)
    drawShape()
    moveShape()


def drawShape():
    global rotAngle
    # Calculate node starting locations.
    for i in range(nodes):
        nodeStartX[i] = centerX + cos(radians(rotAngle)) * radius
        nodeStartY[i] = centerY + sin(radians(rotAngle)) * radius
        rotAngle += 360.0 / nodes
    # Draw polygon.
    curveTightness(organicConstant)
    fill(255)
    with beginClosedShape():
        for i in range(nodes):
            curveVertex(nodeX[i], nodeY[i])
        for i in range(nodes - 1):
            curveVertex(nodeX[i], nodeY[i])


def moveShape():
    global centerX, centerY, deltaX, deltaY, accelX, accelY
    # Move center point.
    deltaX = mouseX - centerX
    deltaY = mouseY - centerY
    # Create springing effect.
    deltaX *= springing
    deltaY *= springing
    accelX += deltaX
    accelY += deltaY
    # Move predator's center.
    centerX += accelX
    centerY += accelY
    # Slow down springing.
    accelX *= damping
    accelY *= damping
    # Change curve tightness.
    organicConstant = 1 - ((abs(accelX) + abs(accelY)) * .1)
    # Move nodes.
    for i in range(nodes):
        nodeX[i] = nodeStartX[i] + sin(radians(angle[i])) * (accelX * 2)
        nodeY[i] = nodeStartY[i] + sin(radians(angle[i])) * (accelY * 2)
        angle[i] += frequency[i]
