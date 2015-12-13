"""
Tickle. 

The word "tickle" jitters when the cursor hovers over.
Sometimes, it can be tickled off the screen.
"""

message = "tickle"
# X and Y coordinates of text
x = 0
y = 0
# horizontal and vertical radius of the text
hr = 0
vr = 0


def setup():
    global x, y, hr, vr
    size(640, 360)
    # Create the font
    textFont(createFont("Georgia", 36))
    textAlign(CENTER, CENTER)
    hr = textWidth(message) / 2
    vr = (textAscent() + textDescent()) / 2
    noStroke()
    x = width / 2
    y = height / 2


def draw():
    global x, y
    # Instead of clearing the background, fade it by drawing
    # a semi-transparent rectangle on top
    fill(204, 120)
    rect(0, 0, width, height)
    # If the cursor is over the text, change the position
    if abs(mouseX - x) < hr and abs(mouseY - y) < vr:
        x += random(-5, 5)
        y += random(-5, 5)
    fill(0)
    text("tickle", x, y)
