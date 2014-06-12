"""
Double Random 
by Ira Greenberg.    

Using two random() calls and the point() function 
to create an irregular sawtooth line.
"""

totalPts = 300
steps = totalPts + 1


def setup():
    size(640, 360)
    stroke(255)
    frameRate(1)


def draw():
    background(0)
    rand = 0
    for i in range(steps):
        point((width / steps) * i, (height / 2) + random(-rand, rand))
        rand += random(-5, 5)

