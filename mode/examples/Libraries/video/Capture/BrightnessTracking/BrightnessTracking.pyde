"""
Brightness Tracking 
by Golan Levin. 

Tracks the brightest pixel in a live video signal. 
"""
import processing.video.*
Capture video
def setup(): 
    size(640, 480)
    # Uses the default video input, see the reference if this causes an error
    video = Capture(this, width, height)
    video.start()
    noStroke()
    smooth()
def draw(): 
    if video.available():
        video.read()
        image(video, 0, 0, width, height)# Draw the webcam video onto the screen
        brightestX = 0# X-coordinate of the brightest video pixel
        brightestY = 0# Y-coordinate of the brightest video pixel
        brightestValue = 0# Brightness of the brightest video pixel
        # Search for the brightest pixel: For each row of pixels in the video image and
        # for each pixel in the yth row, compute each pixel's index in the video
        video.loadPixels()
        index = 0
        for y in range(video.height): 
            for x in range(video.width): 
                # Get the color stored in the pixel
                pixelValue = video.pixels[index]
                # Determine the brightness of the pixel
                pixelBrightness = brightness(pixelValue)
                # If that value is brighter than any previous, then store the
                # brightness of that pixel, as well as its (x,y) location
                if pixelBrightness > brightestValue:
                    brightestValue = pixelBrightness
                    brightestY = y
                    brightestX = x
                
                index += 1
            
        
        # Draw a large, yellow circle at the brightest pixel
        fill(255, 204, 0, 128)
        ellipse(brightestX, brightestY, 200, 200)
    
