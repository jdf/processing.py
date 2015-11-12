"""
GroupPShape

This example shows how to group multiple PShapes into one PShape.
"""


def setup():
    size(640, 360, P2D)
    smooth()
    # Create the shape as a group.
    global group
    group = createShape(GROUP)
    # Make a polygon PShape.
    star = createShape()
    star.beginShape()
    star.noFill()
    star.stroke(255)
    star.vertex(0, -50)
    star.vertex(14, -20)
    star.vertex(47, -15)
    star.vertex(23, 7)
    star.vertex(29, 40)
    star.vertex(0, 25)
    star.vertex(-29, 40)
    star.vertex(-23, 7)
    star.vertex(-47, -15)
    star.vertex(-14, -20)
    star.endShape(CLOSE)
    # Make a path PShape.
    path = createShape()
    path.beginShape()
    path.noFill()
    path.stroke(255)
    # Note: range() only operates on integers.
    # Use a scaled temp value to increment a float.
    for t in range(int(round(-PI * 10)), 0, 1):
        ttemp = t * 0.1
        r = random(60, 70)
        path.vertex(r * cos(ttemp), r * sin(ttemp))
    path.endShape()
    # Make a primitive (Rectangle) PShape.
    rectangle = createShape(RECT, -10, -10, 20, 20)
    rectangle.setFill(False)
    rectangle.setStroke(color(255))
    # Add them all to the group
    group.addChild(star)
    group.addChild(path)
    group.addChild(rectangle)


def draw():
    # We can access them individually via the group PShape.
    rectangle = group.getChild(2)
    # Shapes can be rotated.
    rectangle.rotate(0.1)
    background(52)
    # Display the group PShape.
    translate(mouseX, mouseY)
    shape(group)
