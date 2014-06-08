"""
Mixture Grid    
modified from an example by Simon Greenwold. 

Display a 2D grid of boxes with three different kinds of lights. 
"""


def setup():
    size(640, 360, P3D)
    noStroke()


def draw():
    defineLights()
    background(0)

    for x in range(0, width + 1, 60):
        for y in range(0, height + 1, 60):
            with pushMatrix():
                translate(x, y)
                rotateY(map(mouseX, 0, width, 0, PI))
                rotateX(map(mouseY, 0, height, 0, PI))
                box(90)


def defineLights():
    # Orange point light on the right
    pointLight(150, 100, 0,     # Color
               200, -150, 0)    # Position
    # Blue directional light from the left
    directionalLight(0, 102, 255,  # Color
                     1, 0, 0)      # The x-, y-, z-axis direction
    # Yellow spotlight from the front
    spotLight(255, 255, 109,    # Color
              0, 40, 200,       # Position
              0, -0.5, -0.5,    # Direction
              PI / 2, 2)        # Angle, concentration

