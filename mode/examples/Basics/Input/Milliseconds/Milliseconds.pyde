"""
Milliseconds. 

A millisecond is 1/1000 of a second. 
Processing keeps track of the number of milliseconds a program has run.
By modifying this number with the modulo(%) operator, 
different patterns in time are created.  
"""


def setup():
    global scale
    size(640, 360)
    noStroke()
    scale = width / 20


def draw():
    for i in range(0, scale, 1):
        colorMode(RGB, (i + 1) * scale * 10)
        fill(millis() % ((i + 1) * scale * 10))
        rect(i * scale, 0, scale, height)

