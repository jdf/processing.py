"""
Animated Sprite (Shifty + Teddy)
by James Paterson.

Press the mouse button to change animations.
Demonstrates loading, displaying, and animating GIF images.
It would be easy to write a program to display
animated GIFs, but would not allow as much control over
the display sequence and rate of display.
"""

# From the file "animation.py" import the class "Animation"
from animation import Animation

xpos = 0
drag = 30.0


def setup():
    global animation1, animation2, ypos
    size(640, 360)
    background(255, 204, 0)
    frameRate(24)
    animation1 = Animation("PT_Shifty_", 38)
    animation2 = Animation("PT_Teddy_", 60)
    ypos = height * 0.25


def draw():
    global xpos
    dx = mouseX - xpos
    xpos = xpos + dx / drag
    # Display the sprite at the position xpos, ypos
    if mousePressed:
        background(153, 153, 0)
        animation1.display(xpos - animation1.getWidth() / 2, ypos)
    else:
        background(255, 204, 0)
        animation2.display(xpos - animation1.getWidth() / 2, ypos)

