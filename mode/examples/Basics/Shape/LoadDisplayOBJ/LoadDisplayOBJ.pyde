"""
Load and Display an OBJ Shape. 

The loadShape() command is used to read simple SVG (Scalable Vector Graphics)
files and OBJ (Object) files into a Processing sketch. This example loads an
OBJ file of a rocket and displays it to the screen. 
"""

ry = 0


def setup():
    size(640, 360, P3D)
    global rocket
    rocket = loadShape("rocket.obj")


def draw():
    global ry
    background(0)
    lights()

    translate(width / 2, height / 2 + 100, -200)
    rotateZ(PI)
    rotateY(ry)
    shape(rocket)

    ry += 0.02

