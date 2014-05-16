"""
Scratch 
by Andres Colubri. 

Move the cursor horizontally across the screen to set    
the position in the movie file.
"""
import processing.video.*
Movie mov
def setup(): 
    size(640, 360)
    background(0)
    mov = Movie(this, "transit.mov")
    # Pausing the video at the first frame. 
    mov.play()
    mov.jump(0)
    mov.pause()
def draw(): 
    if mov.available():
        mov.read()
        # A time position is calculated using the current mouse location:
        f = map(mouseX, 0, width, 0, 1)
        t = mov.duration() * f
        mov.play()
        mov.jump(t)
        mov.pause()
    
    image(mov, 0, 0)
