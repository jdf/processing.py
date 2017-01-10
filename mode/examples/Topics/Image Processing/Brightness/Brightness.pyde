"""
Brightness
by Daniel Shiffman.

This program adjusts the brightness of a part of the image by
calculating the distance of each pixel to the mouse.
"""

img = loadImage("moon-wide.jpg")
total = 0
runningavg = 0

def setup():
    global img
    img = loadImage("moon-wide.jpg")
    size(640, 360)
    frameRate(30)
    img.loadPixels()
    # Only need to load the pixels[] array once, because we're only
    # manipulating pixels[] inside draw(), not drawing shapes.
    loadPixels()


def draw():
    global total, runningavg
    now = millis()
    for x in range(img.width):
        for y in range(img.height):
            # Calculate the 1D location from a 2D grid
            loc = x + y * img.width
            # Get the R,G,B values from image.
            # Note that we're only using the `r` channel here, but it's
            # entirely possible to use the `g` and `b` channels as well,
            # together or in isolation.
            r = 0
            r = red(img.pixels[loc])
            # Calculate an amount to change brightness based on proximity to
            # the mouse
            maxdist = 50  # dist(0,0,width,height)
            d = dist(x, y, mouseX, mouseY)
            adjustbrightness = 255 * (maxdist - d) / maxdist
            r += adjustbrightness
            # Constrain RGB to make sure they are within 0-255 color range
            r = constrain(r, 0, 255)
            # Make a color and set pixel in the window
            c = color(r)
            # If we were using the other two channels it would look like
            # `c = color(r, g, b)`
            pixels[y * width + x] = c
    then = millis()
    total += then - now
    runningavg += 1
    println(total / runningavg)
    updatePixels()
