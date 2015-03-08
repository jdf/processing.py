"""
Shape Transform
by Ira Greenberg.

Illustrates the geometric relationship between Cube, Pyramid, Cone and
Cylinder 3D primitives.

Instructions:
Up Arrow - increases points
Down Arrow - decreases points
'p' key toggles between cube / pyramid
"""

angleInc = PI / 300.0
pts = 4
radius = 99
isPyramid = False
cylinderLength = 95


def setup():
    global halfWidth, halfHeight
    size(640, 360, P3D)
    noStroke()
    halfWidth = width / 2
    halfHeight = height / 2


def draw():
    global cylinderLength
    background(170, 95, 95)
    lights()
    fill(255, 200, 200)
    translate(halfWidth, halfHeight)
    rotateX(frameCount * angleInc)
    rotateY(frameCount * angleInc)
    rotateZ(frameCount * angleInc)

    # Initialize vertex arrays.
    vertices = [[PVector() for _ in range(pts + 1)] for _ in range(2)]

    # Fill arrays.
    for i in range(2):
        angle = 0
        for j in range(pts + 1):
            vertices[i][j].x = cos(radians(angle)) * radius
            vertices[i][j].y = sin(radians(angle)) * radius
            vertices[i][j].z = cylinderLength
            # Make the Pyramid point.
            if isPyramid and i == 1:
                vertices[i][j].x = 0
                vertices[i][j].y = 0
            # The .0 after the 360 is critical.
            angle += 360.0 / pts
        cylinderLength *= -1

    # Draw cylinder tube.
    beginShape(QUAD_STRIP)
    for j in range(pts + 1):
        vertex(vertices[0][j].x, vertices[0][j].y, vertices[0][j].z)
        vertex(vertices[1][j].x, vertices[1][j].y, vertices[1][j].z)
    endShape()

    # Draw cylinder ends.
    for i in range(2):
        with beginClosedShape():
            for j in range(pts):
                vertex(vertices[i][j].x, vertices[i][j].y, vertices[i][j].z)


"""
 up / down arrow keys control polygon detail.
"""
def keyPressed():
    global pts, isPyramid
    if key == CODED:
        # Pts.
        if keyCode == UP and pts < 90:
            pts += 1
        elif keyCode == DOWN and pts > 4:
            pts -= 1

    if key == 'p':
        isPyramid = not isPyramid
