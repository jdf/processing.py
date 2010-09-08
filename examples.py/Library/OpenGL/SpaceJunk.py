"""
 Space Junk
 by Ira Greenberg.
 Zoom suggestion
 by Danny Greenberg.
 (Rewritten in Python by Jonathan Feinberg.)

 Rotating cubes in space.
 Color controlled by light sources.
 Move the mouse left and right to zoom.
"""

# Cube count-lower/raise to test P3D/OPENGL performance
limit = 500

# List of cubes, where each cube is a tuple
# (width, height, depth, x, y, z)
cubes = [(random(-10, 10), random(-10, 10), random(-10, 10),
          random(-140, 140), random(-140, 140), random(-140, 140))
          for i in range(limit)]

def setup():
    size(1024, 768, OPENGL)
    background(0)
    noStroke()

def draw():
    background(0)
    fill(200)

    # Set up some different colored lights
    pointLight(51, 102, 255, 65, 60, 100)
    pointLight(200, 40, 60, -65, -60, -150)

    # Raise overall light in scene
    ambientLight(70, 70, 10)

    # Center geometry in display windwow.
    # you can change 3rd argument ('0')
    # to move block group closer(+)/further(-)
    translate(width / 2, height / 2, -200 + mouseX * 0.65)

    # Rotate around y and x axes
    rotateY(frameCount * .01)
    rotateX(frameCount * .01)

    # Draw cubes
    for cube in cubes:
      pushMatrix()
      translate(cube[3], cube[4], cube[5])
      box(cube[0], cube[1], cube[2])
      popMatrix()
      rotateY(.01)
      rotateX(.01)
      rotateZ(.01)
