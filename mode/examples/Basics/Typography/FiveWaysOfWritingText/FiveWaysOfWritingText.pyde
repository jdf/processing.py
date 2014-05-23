# Demonstration of the 5 ways of calling text() in Python mode.

def setup():
    size(500, 500, P3D)

def draw():
    background(255)
    fill(0)
    noStroke()

    # text(string, x, y)
    text("Shillings", 10, 12)
    
    # text(num, x, y)
    text(12.3, 10, 24)
    
    # text(string, x, y, z)
    text("Pence", 10, 36, 100 * cos(millis() / 300.0))

    # text(num, x, y, z)
    text(PI, 10, 48, 100 * sin(millis() / 300.0))

    # text(string, left, top, right, bottom)
    text(
    "Shasta is a delicious, and sometimes underrated, "
    "soft drink. I love it, and I drink it virtually "
    "every day. Yep.\n\nIf you don't like Shasta, then "
    "I don't like you.", 10, 60, 80, 300)
    
    # Show the same box.
    stroke('#FF0000')
    noFill()
    rect(10, 60, 80, 300)
