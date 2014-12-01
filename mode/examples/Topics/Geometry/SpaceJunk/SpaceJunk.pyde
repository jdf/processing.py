"""
Space Junk
by Ira Greenberg (zoom suggestion by Danny Greenberg).

Rotating cubes in space using a custom Cube class. Color controlled by light
sources. Move the mouse left and right to zoom.
"""
from cube import Cube

# Used for overall rotation.
angle = 0

# Cube count - lower / raise to test performance.
limit = 500

# Instantiate cubes, passing in random vals for size and postion.
cubes = [Cube(random(-10, 10), random(-10, 10), random(-10, 10),
              random(-140, 140), random(-140, 140), random(-140, 140))
         for _ in range(limit)]


def setup():
    size(640, 360, P3D)
    background(0)
    noStroke()
    global halfWidth, halfHeight
    halfWidth = width / 2
    halfHeight = height / 2


def draw():
    background(0)
    fill(200)

    # Set up some different colored lights
    pointLight(51, 102, 255, 65, 60, 100)
    pointLight(200, 40, 60, -65, -60, -150)

    # Raise overall light in scene
    ambientLight(70, 70, 10)

    # Center geometry in display window. Change the 3rd argument ('0.65')
    # to move the block group nearer(+) or farther(-)
    translate(halfWidth, halfHeight, -200 + mouseX * 0.65)

    # Rotate around y and x axes
    rotateY(radians(angle))
    rotateX(radians(angle))

    # Draw cubes
    for cube in cubes:
        cube.drawCube()

    # Used in rotate function calls above
    global angle
    angle += 0.2
