"""
Random. 

Random numbers create the basis of this image. 
Each time the program is loaded the result is different. 
"""


def setup():
    size(640, 360)
    background(0)
    strokeWeight(20)
    frameRate(2)


def draw():
    for i in range(width):
        r = random(255)
        stroke(r)
        line(i, 0, i, height)

