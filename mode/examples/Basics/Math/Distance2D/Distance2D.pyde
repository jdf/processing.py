"""
Distance 2D. 

Move the mouse across the image to obscure and reveal the matrix.    
Measures the distance from the mouse to each square and sets the
size proportionally. 
"""

def setup():
    size(640, 360)
    noStroke()
    global max_distance
    max_distance = dist(0, 0, width, height)


def draw():
    background(0)
    for i in range(0, width, 20):
        for j in range(0, height, 20):
            size = dist(mouseX, mouseY, i, j)
            size = size / max_distance * 66
            ellipse(i, j, size, size)

