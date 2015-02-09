"""
Cubes Contained Within a Cube
by Ira Greenberg.

Collision detection against all outer cube's surfaces.
"""
from cube import Cube


Bounds = 300
# 20 little internal cubes
cubes = []
for _ in range(20):
    # Cubes are randomly sized
    cubeSize = random(5, 15)
    cubes.append(Cube(cubeSize, cubeSize, cubeSize))


def setup():
    size(640, 360, P3D)
    global halfWidth, halfHeight
    halfWidth = width / 2.0
    halfHeight = height / 2.0


def draw():
    background(50)
    lights()

    # Center in display window
    translate(halfWidth, halfHeight, -130)

    # Rotate everything, including external large cube
    rotateX(frameCount * 0.001)
    rotateY(frameCount * 0.002)
    rotateZ(frameCount * 0.001)
    stroke(255)

    # Outer transparent cube, just using box() method
    noFill()
    box(Bounds)

    # Move and rotate cubes
    for cube in cubes:
        cube.update(Bounds)
        cube.display()
