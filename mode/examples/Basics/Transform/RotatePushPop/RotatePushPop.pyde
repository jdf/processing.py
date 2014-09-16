"""
Rotate Push Pop. 

The push() and pop() functions allow for more control over transformations.
The push function saves the current coordinate system to the stack 
and pop() restores the prior coordinate system.

If you use "with", then pop() happens for you automatically.
"""

a = 0                 # Angle of rotation
offset = PI / 24.0    # Angle offset between boxes
num = 12              # Number of boxes


def setup():
    size(640, 360, P3D)
    noStroke()


def draw():
    global a
    
    lights()

    background(0, 0, 26)
    translate(width / 2, height / 2)

    for i in range(num):
        gray = map(i, 0, num - 1, 0, 255)
        with pushMatrix():
            fill(gray)
            rotateY(a + offset * i)
            rotateX(a / 2 + offset * i)
            box(200)

    a += 0.01

