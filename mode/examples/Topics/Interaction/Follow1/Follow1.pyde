"""
Follow 1    
based on code from Keith Peters. 

A line segment is pushed and pulled by the cursor.
"""
x = 100
y = 100
angle1 = 0.0
segLength = 50


def setup():
    size(640, 360)
    strokeWeight(20.0)
    stroke(255, 100)


def draw():
    global x, y
    background(0)
    dx = mouseX - x
    dy = mouseY - y
    angle1 = atan2(dy, dx)
    x = mouseX - (cos(angle1) * segLength)
    y = mouseY - (sin(angle1) * segLength)
    segment(x, y, angle1)
    ellipse(x, y, 20, 20)


def segment(x, y, a):
    with pushMatrix():
        translate(x, y)
        rotate(a)
        line(0, 0, segLength, 0)
