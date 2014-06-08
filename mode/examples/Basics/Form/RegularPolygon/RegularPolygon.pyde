"""
Regular Polygon

What is your favorite? Pentagon? Hexagon? Heptagon? 
No? What about the icosagon? The polygon() function 
created for this example is capable of drawing any 
regular polygon. Try placing different numbers into the 
polygon() function calls within draw() to explore. 
"""


def setup():
    size(640, 360)


def draw():
    background(102)

    with pushMatrix():
        translate(width * 0.2, height * 0.5)
        rotate(frameCount / 200.0)
        polygon(0, 0, 82, 3)

    with pushMatrix():
        translate(width * 0.5, height * 0.5)
        rotate(frameCount / 50.0)
        polygon(0, 0, 80, 20)

    with pushMatrix():
        translate(width * 0.8, height * 0.5)
        rotate(frameCount / -100.0)
        polygon(0, 0, 70, 7)


def polygon(x, y, radius, npoints):
    angle = TWO_PI / npoints
    with beginClosedShape():
        a = 0
        while a < TWO_PI:
            sx = x + cos(a) * radius
            sy = y + sin(a) * radius
            vertex(sx, sy)
            a += angle

