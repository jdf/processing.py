"""
LoadFile 1

Loads a text file that contains two numbers separated by a tab ('\t').
A new pair of numbers is loaded each frame and used to draw a point on the screen.
"""

index = 0

def setup():
    global lines
    size(200, 200)
    background(0)
    stroke(255)
    frameRate(12)
    lines = loadStrings("positions.txt")

def draw():
    global index
    if index < len(lines):
        pieces = lines[index].split('\t')
        if len(pieces) == 2:
            x, y = int(pieces[0]) * 2, int(pieces[1]) * 2
            point(x, y)
        # Go to the next line for the next run through draw()
        index = index + 1
