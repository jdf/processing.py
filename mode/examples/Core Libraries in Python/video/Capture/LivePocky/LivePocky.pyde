""" 
Live Pocky
by Ben Fry. 

Unwrap each frame of live video into a single line of pixels.
"""
 
import processing.video.*
Capture video
count
writeRow
maxRows
topRow
buffer[]
def setup(): 
    size(600, 400)
    # This the default video input, see the GettingStartedCapture 
    # example if it creates an error
    video = Capture(this, 320, 240)
    
    # Start capturing the images from the camera
    video.start()
    maxRows = height * 2
    buffer = int[width * maxRows]
    writeRow = height - 1
    topRow = 0
    
    background(0)
    loadPixels()
def draw(): 
    video.loadPixels()
    arraycopy(video.pixels, 0, buffer, writeRow * width, width)
    writeRow += 1
    if writeRow == maxRows:
        writeRow = 0
    
    topRow += 1
    
    for y in range(height): 
        row = (topRow + y) % maxRows
        arraycopy(buffer, row * width, g.pixels, y*width, width)
    
    updatePixels()
def captureEvent(Capture c): 
    c.read()
