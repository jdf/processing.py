"""
Frames 
by Andres Colubri. 

Moves through the video one frame at the time by using the
arrow keys. It estimates the frame counts using the framerate
of the movie file, so it might not be exact in some cases.
"""
 
import processing.video.*
Movie mov
newFrame = 0
movFrameRate = 30
def setup(): 
    size(640, 360)
    background(0)
    # Load and set the video to play. Setting the video 
    # in play mode is needed so at least one frame is read
    # and we can get duration, size and other information from
    # the video stream. 
    mov = Movie(this, "transit.mov")
    
    # Pausing the video at the first frame. 
    mov.play()
    mov.jump(0)
    mov.pause()
def movieEvent(Movie m): 
    m.read()
def draw(): 
    background(0)
    image(mov, 0, 0, width, height)
    fill(255)
    text(getFrame() + " / " + (getLength() - 1), 10, 30)
def keyPressed(): 
    if key == CODED:
        if keyCode == LEFT:
            if (0 < newFrame) newFrame -= 1
        elif keyCode == RIGHT:
            if (newFrame < getLength() - 1) newFrame += 1
        
    
    setFrame(newFrame)
    
def getFrame(): 
    return ceil(mov.time() * 30) - 1
def setFrame(n): 
    mov.play()
        
    # The duration of a single frame:
    frameDuration = 1.0 / movFrameRate
        
    # We move to the middle of the frame by adding 0.5:
    where = (n + 0.5) * frameDuration
        
    # Taking into account border effects:
    diff = mov.duration() - where
    if diff < 0:
        where += diff - 0.25 * frameDuration
    
        
    mov.jump(where)
    mov.pause()
def getLength(): 
    return int(mov.duration() * movFrameRate)
