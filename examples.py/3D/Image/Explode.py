"""
  Explode 
  by Daniel Shiffman.
  (Rewritten in Python by Jonathan Feinberg.) 
  
  Mouse horizontal location controls breaking apart of image and 
  Maps pixels from a 2D image into 3D space. Pixel brightness controls 
  translation along z axis. 
 """
 
cellsize = 2 # Dimensions of each cell in the grid
img = loadImage("eames.jpg")
columns = img.width / cellsize  # Calculate # of columns
rows = img.height / cellsize    # Calculate # of rows
def setup():
    size(640, 360, P3D) 

def draw(): 
    background(0)
    for row in range(rows):
        for col in range(columns):
            x = cellsize * col + cellsize / 2
            y = cellsize * row + cellsize / 2
            loc = x + y * img.width  # Pixel array location
            c = img.pixels[loc]      # Grab the color
            # Calculate a z position as a function of mouseX and pixel brightness
            z = (mouseX / float(width)) * brightness(img.pixels[loc]) - 20.0
            # Translate to the location, set fill and stroke, and draw the rect
            pushMatrix()
            translate(x + 200, y + 100, z)
            fill(c, 204)
            noStroke()
            rectMode(CENTER)
            rect(0, 0, cellsize, cellsize)
            popMatrix()
