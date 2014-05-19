"""
Spatiotemporal
by David Muth

Records a number of video frames into memory, then plays back the video
buffer by turning the time axis into the x-axis and vice versa
""" 
import processing.video.*
Capture video
signal = 0
#the buffer for storing video frames
ArrayList frames
#different program modes for recording and playback
mode = 0
MODE_NEWBUFFER = 0
MODE_RECORDING = 1
MODE_PLAYBACK = 2
currentX = 0
def setup(): 
    size(640, 480)
    
    # This the default video input, see the GettingStartedCapture 
    # example if it creates an error
    video = Capture(this, width, height)
    
    # Start capturing the images from the camera
    video.start()
def captureEvent(Capture c): 
    c.read()
    #create a buffer in case one is needed
    if mode == MODE_NEWBUFFER:
        frames = ArrayList()
        mode = MODE_RECORDING
    
    #record into the buffer until there are enough frames
    if mode == MODE_RECORDING:
        #copy the current video frame into an image, so it can be stored in the buffer
        PImage img = createImage(width, height, RGB)
        video.loadPixels()
        arrayCopy(video.pixels, img.pixels)
        frames.add(img)
        #in case enough frames have been recorded, switch to playback mode
        if frames.size() >= width:
            mode = MODE_PLAYBACK
        
    
def draw(): 
    loadPixels()
    #code for the recording mode 
    if mode == MODE_RECORDING:
        #set the image counter to 0
        currentImage = 0
        #begin a loop for displaying pixel columns
        for x in range(video.width): 
            #go through the frame buffer and pick an image using the image counter
            if currentImage < frames.size():
                PImage img = (PImage)frames.get(currentImage)
                
                #display a pixel column of the current image
                if img != null:
                    img.loadPixels()
                    for y in range(video.height): 
                        pixels[x + y * width] = img.pixels[x + y * video.width]
                    
                
                
                #increase the image counter
                currentImage += 1
                
            
            else:
                break
            
        
    
    #code for displaying the spatiotemporal transformation
    if mode == MODE_PLAYBACK:
        #begin a loop for displaying pixel columns
        for x in range(video.width): 
            #get an image from the buffer using loopcounter x as the index
            PImage img = (PImage)frames.get(x)
            if img != null:
                img.loadPixels()
                
                #pick the same column from each image for display, 
                #then distribute the columns over the x-axis on the screen
                for y in range(video.height): 
                    pixels[x + y * width] = img.pixels[currentX + y * video.width]
                
            
        
        #a different column shall be used next time draw() is being called
        currentX += 1
        
        #if the end of the buffer is reached
        if currentX >= video.width:
            #create a buffer when the next video frame arrives
            mode = MODE_NEWBUFFER
            #reset the column counter
            currentX = 0
        
    
    
    updatePixels()
