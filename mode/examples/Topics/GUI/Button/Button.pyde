"""
Button. 

Click on one of the colored squares in the 
center of the image to change the color of 
the background. 
"""

rectX = 0  # Position of square button
rectY = 0
circleX = 0  # Position of circle button
circleY = 0
rectSize = 90  # Diameter of rect
circleSize = 93  # Diameter of circle
rectColor = color(0)
rectHighlight = color(51)
circleColor = color(255)
circleHighlight = color(204)
baseColor = color(102)
currentColor = baseColor
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
    background(currentColor)
    if rectOver:
        fill(rectHighlight)
    else:
        fill(rectColor)
    stroke(255)
    rect(rectX, rectY, rectSize, rectSize)
    if circleOver:
        fill(circleHighlight)
    else:
        fill(circleColor)
    stroke(0)
    ellipse(circleX, circleY, circleSize, circleSize)


def update(x, y):
    circleOver = overCircle(circleX, circleY, circleSize)
    rectOver = overRect(rectX, rectY, rectSize, rectSize)


def mousePressed():
    if circleOver:
        currentColor = circleColor
    if rectOver:
        currentColor = rectColor


def overRect(x, y, width, height):
    return x <= mouseX <= x + width and y <= mouseY <= y + height


def overCircle(x, y, diameter):
    distance = dist(x,y,mouseX,mouseY)
    return distance < diameter / 2
