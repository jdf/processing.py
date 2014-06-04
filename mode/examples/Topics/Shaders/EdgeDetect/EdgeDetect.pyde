"""
Edge Detection

Change the default shader to apply a simple, custom edge detection filter.

Press the mouse to switch between the custom and default shader.
"""
edges = None
img = None
enabled = True


def setup():
    size(640, 360, P2D)
    img = loadImage("leaves.jpg")
    edges = loadShader("edges.glsl")


def draw():
    if enabled == True:
        shader(edges)
    image(img, 0, 0)


def mousePressed():
    enabled = not enabled
    if enabled == False:
        resetShader()

