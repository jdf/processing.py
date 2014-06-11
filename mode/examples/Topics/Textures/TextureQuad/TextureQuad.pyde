"""
Texture Quad.

Load an image and draw it onto a quad. The texture() function sets
the texture image. The vertex() function maps the image to the geometry.
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

    translate(halfWidth, halfHeight)
    rotateY(map(mouseX, 0, width, -PI, PI))
    rotateZ(PI / 6)

    with beginShape():
        texture(img)
        vertex(-100, -100, 0, 0, 0)
        vertex(100, -100, 0, img.width, 0)
        vertex(100, 100, 0, img.width, img.height)
        vertex(-100, 100, 0, 0, img.height)
