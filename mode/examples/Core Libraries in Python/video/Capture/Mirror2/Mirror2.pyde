"""
Mirror 2 
by Daniel Shiffman. 

Each pixel from the video source is drawn as a rectangle with size based on brightness.    
"""
 
import processing.video.*
# Size of each cell in the grid
cellSize = 15
# Number of columns and rows in our system
cols, rows
# Variable for capture device
Capture video
def setup(): 
    size(640, 480)
    # Set up columns and rows
    cols = width / cellSize
    rows = height / cellSize
    colorMode(RGB, 255, 255, 255, 100)
    rectMode(CENTER)
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
        
        background(0, 0, 255)
        # Begin loop for columns
        for i in range(cols): 
            # Begin loop for rows
            for j in range(rows): 
                # Where are we, pixel-wise?
                x = i * cellSize
                y = j * cellSize
                loc = (video.width - x - 1) + y*video.width# Reversing x to mirror the image
                # Each rect is colored white with a size determined by brightness
                color c = video.pixels[loc]
                sz = (brightness(c) / 255.0) * cellSize
                fill(255)
                noStroke()
                rect(x + cellSize/2, y + cellSize/2, sz, sz)
            
        
    
