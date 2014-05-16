"""
Brightness Thresholding 
by Golan Levin. 

Determines whether a test location (such as the cursor) is contained within
the silhouette of a dark object. 
"""
import processing.video.*
color black = color(0)
color white = color(255)
numPixels
Capture video
def setup(): 
    size(640, 480)# Change size to 320 x 240 if too slow at 640 x 480
    strokeWeight(5)
    
    # This the default video input, see the GettingStartedCapture 
    # example if it creates an error
    video = Capture(this, width, height)
    
    # Start capturing the images from the camera
    video.start()
    
    numPixels = video.width * video.height
    noCursor()
    smooth()
def draw(): 
    if video.available():
        video.read()
        video.loadPixels()
        threshold = 127# Set the threshold value
        pixelBrightness# Declare variable to store a pixel's color
        # Turn each pixel in the video frame black or white depending on its brightness
        loadPixels()
        for i in range(numPixels): 
            pixelBrightness = brightness(video.pixels[i])
            if (pixelBrightness > threshold) # If the pixel is brighter than the
                pixels[i] = white# threshold value, make it white
            
            else # Otherwise,
                pixels[i] = black# make it black
            
        
        updatePixels()
        # Test a location to see where it is contained. Fetch the pixel at the test
        # location (the cursor), and compute its brightness
        testValue = get(mouseX, mouseY)
        testBrightness = brightness(testValue)
        if (testBrightness > threshold) # If the test location is brighter than
            fill(black)# the threshold set the fill to black
        
        else # Otherwise,
            fill(white)# set the fill to white
        
        ellipse(mouseX, mouseY, 20, 20)
    
