"""
Convolution
by Daniel Shiffman.

Applies a convolution matrix to a portion of an image. Move mouse to
apply filter to different parts of the image.
"""

w = 120
# It's possible to convolve the image with many different
# matrices to produce different effects. This is a high-pass
# filter; it accentuates the edges.
matrix = [[-1, -1, -1],
          [-1, 9, -1],
          [-1, -1, -1]]


def setup():
    size(640, 360)
    global img
    img = loadImage("moon-wide.jpg")


def draw():
    # We're only going to process a portion of the image
    # so let's set the whole image as the background first
    image(img, 0, 0)
    # Calculate the small rectangle we will process
    xstart = constrain(mouseX - w / 2, 0, img.width)
    ystart = constrain(mouseY - w / 2, 0, img.height)
    xend = constrain(mouseX + w / 2, 0, img.width)
    yend = constrain(mouseY + w / 2, 0, img.height)
    matrixsize = 3
    loadPixels()
    # Begin our loop for every pixel in the smaller image
    for x in range(xstart, xend):
        for y in range(ystart, yend):
            c = convolution(x, y, matrix, matrixsize, img)
            loc = x + y * img.width
            pixels[loc] = c
    updatePixels()


def convolution(x, y, matrix, matrixsize, img):
    rtotal = 0.0
    gtotal = 0.0
    btotal = 0.0
    offset = matrixsize / 2
    for i in range(matrixsize):
        for j in range(matrixsize):
            # What pixel are we testing
            xloc = x + i - offset
            yloc = y + j - offset
            loc = xloc + img.width * yloc
            # Make sure we haven't walked off our image, we could do better
            # here
            loc = constrain(loc, 0, len(img.pixels) - 1)
            # Calculate the convolution
            rtotal += (red(img.pixels[loc]) * matrix[i][j])
            gtotal += (green(img.pixels[loc]) * matrix[i][j])
            btotal += (blue(img.pixels[loc]) * matrix[i][j])
    # Make sure RGB is within range
    rtotal = constrain(rtotal, 0, 255)
    gtotal = constrain(gtotal, 0, 255)
    btotal = constrain(btotal, 0, 255)
    # Return the resulting color
    return color(rtotal, gtotal, btotal)
