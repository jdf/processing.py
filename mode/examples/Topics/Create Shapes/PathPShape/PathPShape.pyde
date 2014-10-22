"""
PathPShape

A simple path using PShape
"""
# A PShape object
path = None


def setup():
    global path
    size(640, 360, P2D)
    smooth()
    # Create the shape.
    path = createShape()
    path.beginShape()
    # Set fill and stroke.
    path.noFill()
    path.stroke(255)
    path.strokeWeight(2)
    x = 0
    # Calculate the path as a sine wave.
    for i in range(0, TWO_PI * 10, 1):
        itemp = i * .1
        path.vertex(x, sin(itemp) * 100)
        x += 5
    # The path is complete.
    path.endShape()


def draw():
    background(51)
    # Draw the path at the mouse location.
    translate(mouseX, mouseY)
    shape(path)

