"""
Storing Input. 
  
Move the mouse across the screen to change the position
of the circles. The positions of the mouse are recorded
into an array and played back every frame. Between each
frame, the newest value are added to the end of each array
and the oldest value is deleted. 
"""

num = 60
mx = [0.0] * num
my = [0.0] * num


def setup():
    size(640, 360)
    noStroke()
    fill(255, 153)


def draw():
    background(51)
    which = frameCount % num
    mx[which] = mouseX
    my[which] = mouseY

    for i in xrange(0, num, 1):
        index = (which + 1 + i) % num
        ellipse(mx[index], my[index], i, i)

