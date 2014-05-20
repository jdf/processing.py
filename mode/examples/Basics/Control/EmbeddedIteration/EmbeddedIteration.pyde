"""
Embedding Iteration. 

Embedding "for" structures allows repetition in two dimensions. 
"""

size(640, 360)
background(0)
noStroke()

gridSize = 40

for x in range(gridSize, width, gridSize):
    for y in range(gridSize, height, gridSize):
        noStroke()
        fill(255)
        rect(x - 1, y - 1, 3, 3)
        stroke(255, 50)
        line(x, y, width / 2, height / 2)

