"""
Frame Differencing 
by Golan Levin. 

Quantify the amount of movement in the video frame using frame-differencing.
""" 
import processing.video.*
numPixels
int[] previousFrame
Capture video
def setup(): 
    size(640, 480)
    
    # This the default video input, see the GettingStartedCapture 
    # example if it creates an error
    video = Capture(this, width, height)
    
    # Start capturing the images from the camera
    video.start()
    
    numPixels = video.width * video.height
    # Create an array to store the previously captured frame
    previousFrame = int[numPixels]
    loadPixels()
def draw(): 
    if video.available():
        # When using video to manipulate the screen, use video.available() and
        # video.read() inside the draw() method so that it's safe to draw to the screen
        video.read()# Read the frame from the camera
        video.loadPixels()# Make its pixels[] array available
        
        movementSum = 0# Amount of movement in the frame
        for i in range(numPixels): # For each pixel in the video frame...
            color currColor = video.pixels[i]
            color prevColor = previousFrame[i]
            # Extract the red, green, and blue components from current pixel
            currR = (currColor >> 16) & 0xFF# Like red(), but faster
            currG = (currColor >> 8) & 0xFF
            currB = currColor & 0xFF
            # Extract red, green, and blue components from previous pixel
            prevR = (prevColor >> 16) & 0xFF
            prevG = (prevColor >> 8) & 0xFF
            prevB = prevColor & 0xFF
            # Compute the difference of the red, green, and blue values
            diffR = abs(currR - prevR)
            diffG = abs(currG - prevG)
            diffB = abs(currB - prevB)
            # Add these differences to the running tally
            movementSum += diffR + diffG + diffB
            # Render the difference image to the screen
            pixels[i] = color(diffR, diffG, diffB)
            # The following line is much faster, but more confusing to read
            #pixels[i] = 0xff000000 | (diffR << 16) | (diffG << 8) | diffB
            # Save the current color into the 'previous' buffer
            previousFrame[i] = currColor
        
        # To prevent flicker from frames that are all black (no movement),
        # only update the screen if the image has changed.
        if movementSum > 0:
            updatePixels()
            println(movementSum)# Print the total amount of movement to the console
        
    
