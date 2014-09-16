"""
Brightness 
by Rusty Robison. 

Brightness is the relative lightness or darkness of a color.
Move the cursor vertically over each bar to alter its brightness. 
"""

barWidth = 20
lastBar = -1


def setup():
    size(32 * barWidth, 360)
    colorMode(HSB, width, 100, width)
    noStroke()
    background(0)


def draw():
    global lastBar
    whichBar = mouseX / barWidth
    if whichBar != lastBar:
        barX = whichBar * barWidth
        fill(barX, 100, height - mouseY)
        rect(barX, 0, barWidth, height)
        lastBar = whichBar

