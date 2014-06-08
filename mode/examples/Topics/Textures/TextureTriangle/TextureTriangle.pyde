"""
Texture Triangle.

Using a rectangular image to map a texture onto a triangle.
"""

halfWidth = None
halfHeight = None
img = None


def setup():
    global img, halfWidth, halfHeight
    size(640, 360, P3D)
    halfWidth = width / 2.0
    halfHeight = height / 2.0
    img = loadImage("berlin-1.jpg")
    noStroke()


def draw():
    background(0)
    translate(halfWidth, halfHeight, 0)
    rotateY(map(mouseX, 0, width, -PI, PI))

    with beginShape():
        texture(img)
        vertex(-100, -100, 0, 0, 0)
        vertex(100, -40, 0, 300, 120)
        vertex(0, 100, 0, 200, 400)
