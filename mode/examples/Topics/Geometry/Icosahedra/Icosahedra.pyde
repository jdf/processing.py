"""
I Like Icosahedra
by Ira Greenberg.

This example plots icosahedra. The Icosahdron is a regular polyhedron composed
of twenty equalateral triangles.
Slightly simplified to reduce the complexity of the Shape3D class and remove
the unused Dimension3D class.
"""
from icosahedron import Icosahedron

# Pre-calculate some global values
ico1XRot = PI / 185
ico1YRot = PI / -200
ico2XRot = PI / 200
ico2YRot = PI / 300
icoX3Rot = PI / -200
icoY3Rot = PI / 200


def setup():
    global halfWidth, halfHeight, ico3XOffset, ico1XOffset, ico1, ico2, ico3
    size(640, 360, P3D)
    halfWidth = width / 2
    halfHeight = height / 2
    ico3XOffset = width / 3.5
    ico1XOffset = ico3XOffset * -1
    ico1 = Icosahedron(75)
    ico2 = Icosahedron(75)
    ico3 = Icosahedron(75)


def draw():
    background(0)
    lights()
    translate(halfWidth, halfHeight)

    with pushMatrix():
        translate(ico1XOffset, 0)
        rotateX(frameCount * ico1XRot)
        rotateY(frameCount * ico1YRot)
        stroke(170, 0, 0)
        noFill()
        ico1.create()

    with pushMatrix():
        rotateX(frameCount * ico2XRot)
        rotateY(frameCount * ico2YRot)
        stroke(150, 0, 180)
        fill(170, 170, 0)
        ico2.create()

    with pushMatrix():
        translate(ico3XOffset, 0)
        rotateX(frameCount * icoX3Rot)
        rotateY(frameCount * icoY3Rot)
        noStroke()
        fill(0, 0, 185)
        ico3.create()
