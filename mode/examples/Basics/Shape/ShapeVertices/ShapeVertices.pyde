"""
Shape Vertices.

How to iterate over the vertices of a shape.
When loading an obj or SVG, getVertexCount()
will typically return 0 since all the vertices
are in the child shapes.
You should iterate through the children and then
iterate through their vertices.
"""


def setup():
    size(640, 360)
    # Load the shape
    global uk
    uk = loadShape("uk.svg")


def draw():
    background(51)
    # Center where we will draw all the vertices
    translate(width / 2 - uk.width / 2, height / 2 - uk.height / 2)

    # Iterate over the children
    children = uk.getChildCount()
    for i in xrange(children):
        child = uk.getChild(i)
        total = child.getVertexCount()

        # Now we can actually get the vertices from each child
        for j in xrange(total):
            v = child.getVertex(j)
            # Cycling brightness for each vertex
            stroke((frameCount + (i + 1) * j) % 255)
            # Just a dot for each one
            point(v.x, v.y)
