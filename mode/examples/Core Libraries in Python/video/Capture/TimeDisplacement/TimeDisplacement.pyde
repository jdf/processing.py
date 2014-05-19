"""
Time Displacement
by David Muth 

Keeps a buffer of video frames in memory and displays pixel rows
taken from consecutive frames distributed over the y-axis 
""" 
 
import processing.video.*
Capture video
signal = 0
#the buffer for storing video frames
ArrayList frames = ArrayList()
def setup(): 
    size(640, 480)
    
    # This the default video input, see the GettingStartedCapture 
    # example if it creates an error
    video = Capture(this, width, height)
    
    # Start capturing the images from the camera
    video.start()
def captureEvent(Capture camera): 
    camera.read()
    
    # Copy the current video frame into an image, so it can be stored in the buffer
    PImage img = createImage(width, height, RGB)
    video.loadPixels()
    arrayCopy(video.pixels, img.pixels)
    
    frames.add(img)
    
    # Once there are enough frames, remove the oldest one when adding a one
    if frames.size() > height/4:
        frames.remove(0)
    
def draw(): 
 # Set the image counter to 0
 currentImage = 0
 
 loadPixels()
    
    # Begin a loop for displaying pixel rows of 4 pixels height
    for y in range(0, video.height, 4): 
        # Go through the frame buffer and pick an image, starting with the oldest one
        if currentImage < frames.size():
            PImage img = (PImage)frames.get(currentImage)
            
            if img != null:
                img.loadPixels()
                
                # Put 4 rows of pixels on the screen
                for x in range(video.width): 
                    pixels[x + y * width] = img.pixels[x + y * video.width]
                    pixels[x + (y + 1) * width] = img.pixels[x + (y + 1) * video.width]
                    pixels[x + (y + 2) * width] = img.pixels[x + (y + 2) * video.width]
                    pixels[x + (y + 3) * width] = img.pixels[x + (y + 3) * video.width]
                
            
            
            # Increase the image counter
            currentImage += 1
             
        else:
            break
        
    
    
    updatePixels()
    
    # For recording an image sequence
    #saveFrame("frame-####.jpg")
