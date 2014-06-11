"""
PrimitivePShape. 

Using a PShape to display a primitive shape (in this case, ellipse). 
"""
# The PShape object
circle = None


def setup():
    size(640, 360, P2D)
    smooth()
    # Creating the PShape as an ellipse.
    circle = createShape(ELLIPSE, 0, 0, 100, 50)


def draw():
    background(51)
    # We can dynamically set the stroke and fill of the shape.
    circle.setStroke(color(255))
    circle.setStrokeWeight(4)
    circle.setFill(color(map(mouseX, 0, width, 0, 255)))
    # We can use translate to move the PShape.
    translate(mouseX, mouseY)
    # Drawing the PShape
    shape(circle)

