"""
Brightness
by Daniel Shiffman. 

This program adjusts the brightness of a part of the image by
calculating the distance of each pixel to the mouse.
"""

img = None
runningavg = 0
total = 0


def setup():
    size(640, 360)
    frameRate(30)
    img = loadImage("moon-wide.jpg")
    img.loadPixels()
    # Only need to load the pixels[] array once, because we're only
    # manipulating pixels[] inside draw(), not drawing shapes.
    loadPixels()


def draw():
    now = millis()
    for x in range(img.width):
        for y in range(img.height):
            # Calculate the 1D location from a 2D grid
            loc = x + y * img.width
            # Get the R,G,B values from image
            r = 0
            g = 0
            b = 0
            r = red(img.pixels[loc])
            # g = green(img.pixels[loc])
            # b = blue(img.pixels[loc])
            # Calculate an amount to change brightness based on proximity to
            # the mouse
            maxdist = 50  # dist(0,0,width,height)
            d = dist(x, y, mouseX, mouseY)
            adjustbrightness = 255 * (maxdist - d) / maxdist
            r += adjustbrightness
            # g += adjustbrightness
            # b += adjustbrightness
            # Constrain RGB to make sure they are within 0-255 color range
            r = constrain(r, 0, 255)
            # g = constrain(g, 0, 255)
            # b = constrain(b, 0, 255)
            # Make a color and set pixel in the window
            # color c = color(r, g, b)
            c = color(r)
            pixels[y * width + x] = c
    then = millis()
    total += then - now
    runningavg += 1
    println(total / runningavg)
    updatePixels()

