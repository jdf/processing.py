"""
Interactive Toroid
by Ira Greenberg.

Illustrates the geometric relationship between Toroid, Sphere, and Helix
3D primitives, as well as lathing principal.

Instructions:
UP arrow key pts++
DOWN arrow key pts--
LEFT arrow key segments--
RIGHT arrow key segments++
'a' key toroid radius--
's' key toroid radius++
'z' key initial polygon radius--
'x' key initial polygon radius++
'w' key toggle wireframe / solid shading
'h' key toggle sphere / helix
"""

pts = 40
angle = 0.001
radius = 60.0

# Lathe segments.
segments = 60
latheRadius = 100.0

# For shaded or wireframe rendering.
isWireFrame = False

# For optional helix.
isHelix = False
helixOffset = 5.0
PIOneFifty = PI / 150
PIOneSeventy = PI / 170
PINinety = PI / 90


def setup():
    size(640, 360, P3D)
    global halfWidth, halfHeight
    halfWidth = width / 2
    halfHeight = height / 2


def draw():
    background(50, 64, 42)

    # Basic lighting setup.
    lights()

    # 2 rendering styles:
    # Wireframe...
    if isWireFrame:
        stroke(255, 255, 150)
        noFill()
    # ...or solid.
    else:
        noStroke()
        fill(150, 195, 125)

    # Center and spin toroid.
    translate(halfWidth, halfHeight, -100)
    rotateX(frameCount * PIOneFifty)
    rotateY(frameCount * PIOneSeventy)
    rotateZ(frameCount * PINinety)

    vertices = [PVector() for _ in range(pts + 1)]
    vertices2 = [PVector() for _ in range(pts + 1)]

    # Fill arrays.
    global angle
    for i in range(pts + 1):
        # vertices
        vertices[i].x = latheRadius + sin(radians(angle)) * radius
        vertices[i].z = cos(radians(angle)) * radius
        if isHelix:
            vertices[i].z -= helixOffset * segments / 2.0
        angle += 360.0 / pts

    # Draw toroid.
    latheAngle = 0
    for i in range(segments + 1):
        beginShape(QUAD_STRIP)
        for j in range(pts + 1):
            if i > 0:
                vertex(vertices2[j].x, vertices2[j].y, vertices2[j].z)
            vertices2[j].x = cos(radians(latheAngle)) * vertices[j].x
            vertices2[j].y = sin(radians(latheAngle)) * vertices[j].x
            vertices2[j].z = vertices[j].z
            # Optional helix offset.
            if isHelix:
                vertices[j].z += helixOffset
            vertex(vertices2[j].x, vertices2[j].y, vertices2[j].z)
        # Create extra rotation for helix.
        if isHelix:
            latheAngle += 720.0 / segments
        else:
            latheAngle += 360.0 / segments
        endShape()


def keyPressed():
    global pts, segments, latheRadius, radius, isWireFrame, isHelix
    """
    left / right arrow keys control ellipse detail.
    up / down arrow keys control segment detail.
    'a', 's' keys control lathe radius.
    'z', 'x' keys control ellipse radius.
    'w' key toggles between wireframe and solid.
    'h' key toggles between toroid and helix.
    """
    if key == CODED:
        # Points.
        if keyCode == UP and pts < 40:
            pts += 1
        elif keyCode == DOWN and pts > 3:
            pts -= 1
        # Extrusion length.
        if keyCode == LEFT and segments > 3:
            segments -= 1
        elif keyCode == RIGHT and segments < 80:
            segments += 1

    # Lathe radius.
    if key == 'a' and latheRadius > 0:
        latheRadius -= 1
    elif key == 's':
        latheRadius += 1

    # Ellipse radius.
    if key == 'z' and radius > 10:
        radius -= 1
    elif key == 'x':
        radius += 1

    # Wireframe.
    if key == 'w':
        isWireFrame = not isWireFrame

    # Helix.
    if key == 'h':
        isHelix = not isHelix

