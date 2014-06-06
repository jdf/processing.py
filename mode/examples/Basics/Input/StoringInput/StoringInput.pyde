"""
Storing Input. 
  
Move the mouse across the screen to change the position
of the circles. The positions of the mouse are recorded
into an array and played back every frame. Between each
frame, the newest value are added to the end of each array
and the oldest value is deleted. 
"""

import collections

num = 60
mx = collections.deque()
my = collections.deque()


def setup():
    size(640, 360)
    noStroke()
    fill(255, 153)


def draw():
    background(51)
    mx.append(mouseX)
    my.append(mouseY)
    if len(mx) > num:
        mx.popleft()
    if len(my) > num:
        my.popleft()
    for i in xrange(len(mx)):
        ellipse(mx[i], my[i], i, i)

