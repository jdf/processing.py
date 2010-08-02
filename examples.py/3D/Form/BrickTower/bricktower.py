"""
 * Brick Tower
 * by Ira Greenberg. 
 * 
 * 3D castle tower constructed out of individual bricks.
 * Uses the PVector and Cube classes. 
"""
from cube import Cube
bricksPerLayer = 16.0
brickLayers = 18.0
brickWidth = 60
brickHeight = 25
brickDepth = 25
radius = 175.0
brick = Cube(brickWidth, brickHeight, brickDepth)

def setup():
    size(640, 360, P3D)

def draw():
    background(0)
    (tempX, tempY, tempZ) = (0,0,0)
    fill(182, 62, 29)
    noStroke()
    # Add basic light setup
    lights()
    translate(width/2, height*1.2, -380)
    # Tip tower to see inside
    rotateX(radians(-45))
    # Slowly rotate tower
    rotateY(frameCount * PI/600)
    for i in range(brickLayers):
        # Increment rows
        tempY-=brickHeight
        # Alternate brick seams
        angle = 360.0 / bricksPerLayer * i/2
        for j in range(bricksPerLayer):
            tempZ = cos(radians(angle))*radius
            tempX = sin(radians(angle))*radius
            pushMatrix()
            translate(tempX, tempY, tempZ)
            rotateY(radians(angle))
            # Add crenelation
            if (i==brickLayers-1):
                if (j%2 == 0):
                    brick.create()
            else:
                # Create main tower
                brick.create()
            popMatrix()
            angle += 360.0/bricksPerLayer
