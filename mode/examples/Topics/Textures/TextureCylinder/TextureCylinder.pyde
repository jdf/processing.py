"""
Texture Cylinder.

Load an image and draw it onto a cylinder and a quad.
"""

halfWidth = None
halfHeight = None
tubeRes = 32
tubeX = [0.0 for _ in range(tubeRes)]
tubeY = [0.0 for _ in range(tubeRes)]
img = None


def setup():
    size(640, 360, P3D)
    global halfWidth, halfHeight, img
    halfWidth = width / 2.0
    halfHeight = height / 2.0
    img = loadImage("berlin-1.jpg")
    angle = 270.0 / tubeRes
    for i in range(tubeRes):
        tubeX[i] = cos(radians(i * angle))
        tubeY[i] = sin(radians(i * angle))
    noStroke()


def draw():
    background(0)

    translate(halfWidth, halfHeight)
    rotateX(map(mouseY, 0, height, -PI, PI))
    rotateY(map(mouseX, 0, width, -PI, PI))

    beginShape(QUAD_STRIP)
    texture(img)
    for i in range(tubeRes):
        x = tubeX[i] * 100
        z = tubeY[i] * 100
        u = img.width / tubeRes * i
        vertex(x, -100, z, u, 0)
        vertex(x, 100, z, u, img.height)
    endShape()

    with beginShape(QUADS):
        texture(img)
        vertex(0, -100, 0, 0, 0)
        vertex(100, -100, 0, 100, 0)
        vertex(100, 100, 0, 100, 100)
        vertex(0, 100, 0, 0, 100)
