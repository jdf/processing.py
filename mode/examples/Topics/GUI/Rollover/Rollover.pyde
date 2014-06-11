"""
Rollover.

Roll over the colored squares in the center of the image
to change the color of the outside rectangle.
"""

# Position of square button
rectX = 0
rectY = 0
# Position of circle button
circleX = 0
circleY = 0
rectSize = 90  # Diameter of rect
circleSize = 93  # Diameter of circle
rectColor = color(0)
circleColor = color(255)
baseColor = color(102)
rectOver = False
circleOver = False


def setup():
    size(640, 360)
    circleX = width / 2 + circleSize / 2 + 10
    circleY = height / 2
    rectX = width / 2 - rectSize - 10
    rectY = height / 2 - rectSize / 2
    ellipseMode(CENTER)


def draw():
    update(mouseX, mouseY)
    noStroke()
    if rectOver:
        background(rectColor)
    elif circleOver:
        background(circleColor)
    else:
        background(baseColor)
    stroke(255)
    fill(rectColor)
    rect(rectX, rectY, rectSize, rectSize)
    stroke(0)
    fill(circleColor)
    ellipse(circleX, circleY, circleSize, circleSize)


def update(x, y):
    circleOver = overCircle(circleX, circleY, circleSize)
    rectOver = overRect(rectX, rectY, rectSize, rectSize)


def overRect(x, y, width, height):
    return x <= mouseX <= x + width and y <= mouseY <= y + height


def overCircle(x, y, diameter):
    distance = dist(x, y, mouseX, mouseY)
    return distance < diameter / 2

