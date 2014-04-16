"""
 * List 2D. 
 * 
 * Demonstrates the syntax for creating a two-dimensional (2D) list,
 * which, in Python, is simply a list of lists.
 * Values in a 2D list are accessed through two index values.    
 * 2D arrays are useful for storing images. In this example, each dot 
 * is colored in relation to its distance from the center of the image. 
 """

# By convention, Python constants have UPPERCASE_NAMES.
SPACER = 10

# Start with an empty list.
distances = []


def setup():
    size(640, 360)
    maxDistance = dist(width / 2, height / 2, width, height)
    for x in range(width):
        column = []
        distances.append(column)
        for y in range(height):
            distance = dist(width / 2, height / 2, x, y)
            column.append(distance / maxDistance * 255)
    spacer = 10
    noLoop()    # Run once and stop


def draw():
    background(0)
    # This embedded loop skips over values in the arrays based on
    # the spacer variable, so there are more values in the array
    # than are drawn here. Change the value of the spacer variable
    # to change the density of the points
    for x in range(0, width, SPACER):
        for y in range(0, height, SPACER):
            stroke(distances[x][y])
            point(x + SPACER / 2, y + SPACER / 2)

