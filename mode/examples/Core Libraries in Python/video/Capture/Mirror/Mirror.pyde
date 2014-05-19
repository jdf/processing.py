"""
Mirror 
by Daniel Shiffman.    

Each pixel from the video source is drawn as a rectangle with rotation based on brightness.     
""" 
 
import processing.video.*
# Size of each cell in the grid
cellSize = 20
# Number of columns and rows in our system
cols, rows
# Variable for capture device
Capture video
def setup(): 
    size(640, 480)
    frameRate(30)
    cols = width / cellSize
    rows = height / cellSize
    colorMode(RGB, 255, 255, 255, 100)
    # This the default video input, see the GettingStartedCapture 
    # example if it creates an error
    video = Capture(this, width, height)
    
    # Start capturing the images from the camera
    video.start()
    
    background(0)
def draw(): 
    if video.available():
        video.read()
        video.loadPixels()
    
        # Begin loop for columns
        for i in range(cols): 
            # Begin loop for rows
            for j in range(rows): 
            
                # Where are we, pixel-wise?
                x = i*cellSize
                y = j*cellSize
                loc = (video.width - x - 1) + y*video.width# Reversing x to mirror the image
            
                r = red(video.pixels[loc])
                g = green(video.pixels[loc])
                b = blue(video.pixels[loc])
                # Make a color with an alpha component
                color c = color(r, g, b, 75)
            
                # Code for drawing a single rect
                # Using translate in order for rotation to work properly
                pushMatrix()
                translate(x+cellSize/2, y+cellSize/2)
                # Rotation formula based on brightness
                rotate((2 * PI * brightness(c) / 255.0))
                rectMode(CENTER)
                fill(c)
                noStroke()
                # Rects are larger than the cell for some overlap
                rect(0, 0, cellSize+6, cellSize+6)
                popMatrix()
            
        
    
