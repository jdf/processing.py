"""
Performance demo using quad rendering
"""


def setup():
    size(800, 600, P2D)
    noStroke()
    fill(0, 1)


def draw():
    background(255)
    for i in xrange(50000):
        x = random(width)
        y = random(height)
        rect(x, y, 30, 30)

    if frameCount % 10 == 0:
        print frameRate
