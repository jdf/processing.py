"""
Pulses. 

Software drawing instruments can follow a rhythm or abide by rules independent
of drawn gestures. This is a form of collaborative drawing in which the draftsperson
controls some aspects of the image and the software controls others.
"""

angle = 0


def setup():
    size(640, 360)
    background(102)
    noStroke()
    fill(0, 102)


def draw():
    # Draw only when mouse is pressed
    if mousePressed == True:
        angle += 5
        val = cos(radians(angle)) * 12.0
        for a in range(0, 360, 75):
            xoff = cos(radians(a)) * val
            yoff = sin(radians(a)) * val
            fill(0)
            ellipse(mouseX + xoff, mouseY + yoff, val, val)

        fill(255)
        ellipse(mouseX, mouseY, 2, 2)

