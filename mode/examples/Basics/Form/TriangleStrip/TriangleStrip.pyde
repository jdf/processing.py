"""
Triangle Strip 
by Ira Greenberg. 

Generate a closed ring using the vertex() function and 
beginShape(TRIANGLE_STRIP) mode. The outsideRadius and insideRadius 
variables control ring's radii respectively.
"""
outsideRadius = 150
insideRadius = 100


def setup():
    size(640, 360)
    background(204)
    global x, y
    x = width / 2
    y = height / 2


def draw():
    background(204)

    numPoints = int(map(mouseX, 0, width, 6, 60))
    angle = 0
    angleStep = 180.0 / numPoints

    beginShape(TRIANGLE_STRIP)
    for i in range(numPoints + 1):
        px = x + cos(radians(angle)) * outsideRadius
        py = y + sin(radians(angle)) * outsideRadius
        angle += angleStep
        vertex(px, py)
        px = x + cos(radians(angle)) * insideRadius
        py = y + sin(radians(angle)) * insideRadius
        vertex(px, py)
        angle += angleStep
    endShape()
