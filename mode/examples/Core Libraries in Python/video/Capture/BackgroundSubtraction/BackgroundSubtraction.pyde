"""
Background Subtraction 
by Golan Levin. 

Detect the presence of people and objects in the frame using a simple
background-subtraction technique. To initialize the background, press a key.
"""
import processing.video.*
numPixels
int[] backgroundPixels
Capture video
def setup(): 
    size(640, 480)
    
    # This the default video input, see the GettingStartedCapture 
    # example if it creates an error
    #video = Capture(this, 160, 120)
    video = Capture(this, width, height)
    
    # Start capturing the images from the camera
    video.start()
    
    numPixels = video.width * video.height
    # Create array to store the background image
    backgroundPixels = int[numPixels]
    # Make the pixels[] array available for direct manipulation
    loadPixels()
def draw(): 
    if video.available():
        video.read()# Read a video frame
        video.loadPixels()# Make the pixels of video available
        # Difference between the current frame and the stored background
        presenceSum = 0
        for i in range(numPixels): # For each pixel in the video frame...
            # Fetch the current color in that location, and also the color
            # of the background in that spot
            color currColor = video.pixels[i]
            color bkgdColor = backgroundPixels[i]
            # Extract the red, green, and blue components of the current pixel's color
            currR = (currColor >> 16) & 0xFF
            currG = (currColor >> 8) & 0xFF
            currB = currColor & 0xFF
            # Extract the red, green, and blue components of the background pixel's color
            bkgdR = (bkgdColor >> 16) & 0xFF
            bkgdG = (bkgdColor >> 8) & 0xFF
            bkgdB = bkgdColor & 0xFF
            # Compute the difference of the red, green, and blue values
            diffR = abs(currR - bkgdR)
            diffG = abs(currG - bkgdG)
            diffB = abs(currB - bkgdB)
            # Add these differences to the running tally
            presenceSum += diffR + diffG + diffB
            # Render the difference image to the screen
            pixels[i] = color(diffR, diffG, diffB)
            # The following line does the same thing much faster, but is more technical
            #pixels[i] = 0xFF000000 | (diffR << 16) | (diffG << 8) | diffB
        
        updatePixels()# Notify that the pixels[] array has changed
        println(presenceSum)# Print out the total amount of movement
    
# When a key is pressed, capture the background image into the backgroundPixels
# buffer, by copying each of the current frame's pixels into it.
def keyPressed(): 
    video.loadPixels()
    arraycopy(video.pixels, backgroundPixels)
