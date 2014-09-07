"""
Storing Input. 
  
Move the mouse across the screen to change the position
of the circles. The positions of the mouse are recorded
into a deque and played back every frame. Between each
frame, the newest value are added to the end of each array
and the oldest value is deleted. 
"""

from collections import deque

history = deque(maxlen=60)


def setup():
    size(640, 360)
    noStroke()
    fill(255, 153)


def draw():
    background(51)
    history.append((mouseX, mouseY))
    for i, (x, y) in enumerate(history):
        ellipse(x, y, i, i)

