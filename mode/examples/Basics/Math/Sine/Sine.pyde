"""
Sine. 

Smoothly scaling size with the sin() function. 
"""

angle = 0

def setup():
    size(640, 360)
    global diameter
    diameter = height - 10
    noStroke()
    noStroke()
    fill(255, 204, 0)


def draw():
    global angle
    background(0)
    d1 = 10 + (sin(angle) * diameter / 2) + diameter / 2
    d2 = 10 + (sin(angle + PI / 2) * diameter / 2) + diameter / 2
    d3 = 10 + (sin(angle + PI) * diameter / 2) + diameter / 2

    ellipse(0, height / 2, d1, d1)
    ellipse(width / 2, height / 2, d2, d2)
    ellipse(width, height / 2, d3, d3)

    angle += 0.02
