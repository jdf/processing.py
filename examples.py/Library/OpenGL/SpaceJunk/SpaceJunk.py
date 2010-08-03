"""
 * Space Junk  
 * by Ira Greenberg. 
 * Zoom suggestion 
 * by Danny Greenberg.
 * 
 * Rotating cubes in space using a custom Cube class. 
 * Color controlled by light sources. Move the mouse left
 * and right to zoom.
"""

from Cube import Cube
# Used for oveall rotation
ang = 0.0

# Cube count-lower/raise to test P3D/OPENGL performance
limit = 500

# Array for all cubes
cubes = [Cube(int(random(-10, 10)), int(random(-10, 10)),
              int(random(-10, 10)), int(random(-140, 140)), 
              int(random(-140, 140)), int(random(-140, 140))) 
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
    global ang
    rotateY(radians(ang))
    rotateX(radians(ang))
    
    # Draw cubes
    for cube in cubes:
      cube.drawCube()
    
    # Used in rotate function calls above
    ang += 1


