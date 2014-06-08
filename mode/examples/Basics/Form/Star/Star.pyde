"""
Star

The star() function created for this example is capable of drawing a
wide range of different forms. Try placing different numbers into the 
star() function calls within draw() to explore. 
"""


def setup():
    size(640, 360)


def draw():
    background(102)

    with pushMatrix():
        translate(width * 0.2, height * 0.5)
        rotate(frameCount / 200.0)
        star(0, 0, 5, 70, 3)

    with pushMatrix():
        translate(width * 0.5, height * 0.5)
        rotate(frameCount / 50.0)
        star(0, 0, 80, 100, 40)

    with pushMatrix():
        translate(width * 0.8, height * 0.5)
        rotate(frameCount / -100.0)
        star(0, 0, 30, 70, 5)


def star(x, y, radius1, radius2, npoints):
    angle = TWO_PI / npoints
    halfAngle = angle / 2.0
    with beginClosedShape():
        a = 0
        while a < TWO_PI:
            sx = x + cos(a) * radius2
            sy = y + sin(a) * radius2
            vertex(sx, sy)
            sx = x + cos(a + halfAngle) * radius1
            sy = y + sin(a + halfAngle) * radius1
            vertex(sx, sy)
            a += angle

