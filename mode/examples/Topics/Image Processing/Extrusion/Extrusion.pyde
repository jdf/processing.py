"""
Extrusion. 

Converts a flat image into spatial data points and rotates the points
around the center.
"""
a = None
onetime = True
aPixels = None
values = None
angle = 0


def setup():
    size(640, 360, P3D)
    aPixels = [[0] * width for i in range(height)]
    values = [[0] * width for i in range(height)]
    noFill()
    # Load the image into a array
    # Extract the values and store in an array
    a = loadImage("ystone08.jpg")
    a.loadPixels()
    for i in range(a.height):
        for j in range(a.width):
            aPixels[j][i] = a.pixels[i * a.width + j]
            values[j][i] = int(blue(aPixels[j][i]))


def draw():
    background(0)
    translate(width / 2, height / 2, -height / 2)
    scale(2.0)
    # Update and constrain the angle
    angle += 0.005
    rotateY(angle)
    # Display the image mass
    for i in range(0, a.height, 4):
        for j in range(0, a.width, 4):
            stroke(values[j][i], 255)
            line(j - a.width / 2, i - a.height / 2, -
                 values[j][i], j - a.width / 2, i - a.height / 2, -values[j][i] - 10)

