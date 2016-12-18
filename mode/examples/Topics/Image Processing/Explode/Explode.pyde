"""
Explode
by Daniel Shiffman.

Mouse horizontal location controls breaking apart of image and
maps pixels from a 2D image into 3D space. Pixel brightness controls
translation along z axis.
"""

def setup():
    size(640, 360, P3D)
    # Number of columns and rows in our system
    global columns, rows, cellsize, img
    img = loadImage("eames.jpg")  # Load the image
    cellsize = 2  # Dimensions of each cell in the grid
    columns = img.width / cellsize  # Calculate # of columns
    rows = img.height / cellsize  # Calculate # of rows

def draw():
    background(0)
    # Begin loop for columns
    for i in range(columns):
        # Begin loop for rows
        for j in range(rows):
            x = i * cellsize + cellsize / 2  # x position
            y = j * cellsize + cellsize / 2  # y position
            loc = x + y * img.width  # Pixel array location
            c = img.pixels[loc]  # Grab the color
            # Calculate a z position as a function of mouseX and pixel
            # brightness
            z = (mouseX / float(width)) * brightness(img.pixels[loc]) - 20.0
            # Translate to the location, set fill and stroke, and draw the rect
            with pushMatrix():
                translate(x + 200, y + 100, z)
                fill(c, 204)
                noStroke()
                rectMode(CENTER)
                rect(0, 0, cellsize, cellsize)
