"""
Ortho vs Perspective.

Click to see the difference between orthographic projection
and perspective projection as applied to a simple box.
The ortho() function sets an orthographic projection and
defines a parallel clipping volume. All objects with the
same dimension appear the same size, regardless of whether
they are near or far from the camera. The parameters to this
function specify the clipping volume where left and right
are the minimum and maximum x values, top and bottom are the
minimum and maximum y values, and near and far are the minimum
and maximum z values.
"""

showPerspective = True


def setup():
    size(640, 360, P3D)
    noFill()
    fill(255)
    noStroke()


def draw():
    lights()
    background(0)
    far = map(mouseX, 0, width, 120, 400)
    if showPerspective:
        perspective(PI / 3.0, float(width) / float(height), 10, far)
    else:
        ortho(-width/2.0, width/2.0, -height/2.0, height/2.0, 10, far)
    translate(width / 2, height / 2, 0)
    rotateX(-PI / 6)
    rotateY(PI / 3)
    box(180)


def mousePressed():
    global showPerspective
    showPerspective = not showPerspective

