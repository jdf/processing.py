"""
Extrusion.

Converts a flat image into spatial data points and rotates the points
around the center.
"""
angle = 0


def setup():
    global img
    img = loadImage("ystone08.jpg")
    size(640, 360, P3D)
    global values
    values = [[0] * width for i in range(height)]
    noFill()
    # Load the image into a array
    # Extract the values and store in an array
    img.loadPixels()
    for i in range(img.height):
        for j in range(img.width):
            values[j][i] = int(blue(img.pixels[i * img.width + j]))


def draw():
    global angle
    background(0)
    translate(width / 2, height / 2, -height / 2)
    scale(2.0)
    # Update and constrain the angle
    angle += 0.005
    rotateY(angle)
    # Display the image mass
    for i in range(0, img.height, 4):
        for j in range(0, img.width, 4):
            stroke(values[j][i], 255)
            line(j - img.width / 2, i - img.height / 2,
                 -values[j][i], j - img.width / 2,
                 i - img.height / 2, -values[j][i] - 10)
