"""
SaveFile 1

Saving files is a useful way to store data so it can be viewed after a
program has stopped running. The saveStrings() function writes an array
of strings to a file, with each string written to a new line. This file
is saved to the sketch's folder.
"""

x = []
y = []


def setup():
    size(200, 200)


def draw():
    background(204)
    stroke(0)
    noFill()
    beginShape()
    for i in xrange(len(x)):
        vertex(x[i], y[i])

    endShape()
    # Show the next segment to be added
    if (len(x) >= 1):
        stroke(255)
        line(mouseX, mouseY, x[len(x) - 1], y[len(x) - 1])


def mousePressed():  # Click to add a line segment
    x.append(mouseX)
    y.append(mouseY)


def keyPressed():  # Press a key to save the data
    lines = []
    for i in xrange(len(x)):
        lines.insert(i, str(x[i]) + "\t" + str(y[i]))

    saveStrings("lines.txt", lines)
    exit()  # Stop the program
