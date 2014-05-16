"""
Framingham
by Ben Fry.

Show subsequent frames from video input as a grid. Also fun with movie files.
"""
import processing.video.*
Capture video
column
columnCount
lastRow
# Buffer used to move all the pixels up
int[] scoot
def setup(): 
    size(640, 480)
    # This the default video input, see the GettingStartedCapture 
    # example if it creates an error
    video = Capture(this, 160, 120)
    
    # Start capturing the images from the camera
    video.start()
    
    column = 0
    columnCount = width / video.width
    rowCount = height / video.height
    lastRow = rowCount - 1
    
    scoot = int[lastRow*video.height * width]
    background(0)
def draw(): 
    # By using video.available, only the frame rate need be set inside setup()
    if video.available():
        video.read()
        video.loadPixels()
        image(video, video.width*column, video.height*lastRow)
        column += 1
        if column == columnCount:
            loadPixels()
                
            # Scoot everybody up one row
            arrayCopy(pixels, video.height*width, scoot, 0, len(scoot))
            arrayCopy(scoot, 0, pixels, 0, len(scoot))
            # Set the moved row to black
            for (i = scoot.lengthi < width*heighti += 1) 
                pixels[i] = #000000
            
            column = 0
            updatePixels()
        
    
