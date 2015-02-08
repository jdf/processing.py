"""
Pulses.

Software drawing instruments can follow a rhythm or abide by rules independent
of drawn gestures. This is a form of collaborative drawing in which the draftsperson
controls some aspects of the image and the software controls others.
"""

offset = 0


def setup():
    size(640, 360)
    background(102)
    noStroke()
    fill(0, 102)


def draw():
    global offset
    # Draw only when mouse is pressed
    if mousePressed == True:
        offset += 5
        radius = cos(radians(offset)) * 12.0
        for angle in range(0, 360, 75):
            xOff = cos(radians(angle)) * radius
            yOff = sin(radians(angle)) * radius
            fill(0)
            ellipse(mouseX + xOff, mouseY + yOff, radius, radius)
        fill(255)
        ellipse(mouseX, mouseY, 2, 2)
