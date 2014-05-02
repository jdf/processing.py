"""
Saturation. 

Saturation is the strength or purity of the color and represents the 
amount of gray in proportion to the hue. A "saturated" color is pure 
and an "unsaturated" color has a large percentage of gray. 
Move the cursor vertically over each bar to alter its saturation. 
"""

barWidth = 20


def setup():
    size(barWidth * 32, 360)
    colorMode(HSB, width, height, 100)
    noStroke()


def draw():
    whichBar = mouseX / barWidth
    barX = whichBar * barWidth
    fill(barX, mouseY, 66)
    rect(barX, 0, barWidth, height)

