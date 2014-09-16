"""
Rotate. 

Rotating a square around the Z axis. To get the results
you expect, send the rotate function angle parameters that are
values between 0 and PI*2 (TWO_PI which is roughly 6.28). If you prefer to 
think about angles as degrees (0-360), you can use the radians() 
method to convert your values. For example: scale(radians(90))
is identical to the statement scale(PI/2). 
"""

angle = 0
jitter = 0


def setup():
    size(640, 360)
    noStroke()
    fill(255)
    rectMode(CENTER)


def draw():
    background(51)

    global jitter
    # during even-numbered seconds (0, 2, 4, 6...)
    if second() % 2 == 0:
        jitter = random(-0.1, 0.1)

    global angle
    angle = angle + jitter
    c = cos(angle)
    translate(width / 2, height / 2)
    rotate(c)
    rect(0, 0, 180, 180)

