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

halfWidth = None
halfHeight = None

pts = 40
angle = 0.001
radius = 60.0

# lathe segments
segments = 60
latheRadius = 100.0

# for shaded or wireframe rendering
isWireFrame = False

# for optional helix
isHelix = False
helixOffset = 5.0

PIOneFifty = PI / 150
PIOneSeventy = PI / 170
PINinety = PI / 90


def setup():
    size(640, 360, P3D)
    halfWidth = width / 2
    halfHeight = height / 2


def draw():
    background(50, 64, 42)

    # basic lighting setup
    lights()

    # 2 rendering styles
    # wireframe or solid
    if isWireFrame:
        stroke(255, 255, 150)
        noFill()
    else:
        noStroke()
        fill(150, 195, 125)

    # center and spin toroid
    translate(halfWidth, halfHeight, -100)

    rotateX(frameCount * PIOneFifty)
    rotateY(frameCount * PIOneSeventy)
    rotateZ(frameCount * PINinety)

    vertices = [PVector() for _ in range(pts + 1)]
    vertices2 = [PVector() for _ in range(pts + 1)]

    # fill arrays
    for i in range(pts + 1):
        # vertices
        vertices[i].x = latheRadius + sin(radians(angle)) * radius
        if isHelix:
            vertices[i].z = (cos(radians(angle)) * radius -
                             (helixOffset * segments) / 2.0)
        else:
            vertices[i].z = cos(radians(angle)) * radius

        angle += 360.0 / pts

    # draw toroid
    latheAngle = 0
    for i in range(segments + 1):
        beginShape(QUAD_STRIP)
        for j in range(pts + 1):
            if i > 0:
                vertex(vertices2[j].x, vertices2[j].y, vertices2[j].z)

            vertices2[j].x = cos(radians(latheAngle)) * vertices[j].x
            vertices2[j].y = sin(radians(latheAngle)) * vertices[j].x
            vertices2[j].z = vertices[j].z
            # optional helix offset
            if isHelix:
                vertices[j].z += helixOffset

            vertex(vertices2[j].x, vertices2[j].y, vertices2[j].z)

        # create extra rotation for helix
        if isHelix:
            latheAngle += 720.0 / segments
        else:
            latheAngle += 360.0 / segments

        endShape()


"""
 left / right arrow keys control ellipse detail
 up / down arrow keys control segment detail.
 'a', 's' keys control lathe radius
 'z', 'x' keys control ellipse radius
 'w' key toggles between wireframe and solid
 'h' key toggles between toroid and helix
 """


def keyPressed():
    if key == CODED:
        # pts
        if keyCode == UP:
            if pts < 40:
                pts += 1
        elif keyCode == DOWN:
            if pts > 3:
                pts -= 1
        # extrusion length
        if keyCode == LEFT:
            if segments > 3:
                segments -= 1
        elif keyCode == RIGHT:
            if segments < 80:
                segments += 1

    # lathe radius
    if key == 'a':
        if latheRadius > 0:
            latheRadius -= 1
    elif key == 's':
        latheRadius += 1

    # ellipse radius
    if key == 'z':
        if radius > 10:
            radius -= 1
    elif key == 'x':
        radius += 1

    # wireframe
    if key == 'w':
        if isWireFrame:
            isWireFrame = False
        else:
            isWireFrame = True

    # helix
    if key == 'h':
        if isHelix:
            isHelix = False
        else:
            isHelix = True
