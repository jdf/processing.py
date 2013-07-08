"""
 * Interactive Toroid
 * PDE by Ira Greenberg, rewritten in Python by Jonathan Feinberg
 *
 * Illustrates the geometric relationship between Toroid, Sphere, and Helix
 * 3D primitives, as well as lathing principal.
 *
 * Instructions:
 * UP arrow key pts++
 * DOWN arrow key pts--
 * LEFT arrow key segments--
 * RIGHT arrow key segments++
 * 'a' key toroid radius--
 * 's' key toroid radius++
 * 'z' key initial polygon radius--
 * 'x' key initial polygon radius++
 * 'w' key toggle wireframe/solid shading
 * 'h' key toggle sphere/helix
 """

pts = 40
radius = 60.0

# lathe segments
segments = 60
latheRadius = 100.0

# for shaded or wireframe rendering
isWireFrame = False

# for optional helix
isHelix = False
helixOffset = 5.0

# The extruded shape as a list of quad strips
strips = []

def setup():
    size(640, 360, OPENGL)

def extrude():
    dTheta = TWO_PI / pts
    helicalOffset = 0
    if isHelix:
        helicalOffset = - (helixOffset * segments) / 2
    vertices = [[latheRadius + sin(dTheta * x) * radius,
                 cos(dTheta * x) * radius + helicalOffset]
                 for x in range(pts + 1)]
    vertices2 = [[0.0, 0.0, 0.0] for x in range(pts + 1)]

    # draw toroid
    latheAngle = 0
    dTheta = TWO_PI / segments
    if isHelix:
        dTheta *= 2
    for i in range(segments + 1):
        verts = []
        for j in range(pts + 1):
            v2 = vertices2[j]
            if i > 0:
                verts.append(v2[:])

            v2[0] = cos(latheAngle) * vertices[j][0]
            v2[1] = sin(latheAngle) * vertices[j][0]
            v2[2] = vertices[j][1]
            # optional helix offset
            if isHelix:
                vertices[j][1] += helixOffset

            verts.append(v2[:])
        strips.append(verts)
        latheAngle += dTheta

def draw():
    if not len(strips):
        extrude()

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

    #center and spin toroid
    translate(width / 2, height / 2, -100)
    rotateX(frameCount * PI / 150)
    rotateY(frameCount * PI / 170)
    rotateZ(frameCount * PI / 90)

    # draw toroid
    for strip in strips:
        beginShape(QUAD_STRIP)
        for v in strip:
            vertex(v[0], v[1], v[2])
        endShape()

"""
 left/right arrow keys control ellipse detail
 up/down arrow keys control segment detail.
 'a','s' keys control lathe radius
 'z','x' keys control ellipse radius
 'w' key toggles between wireframe and solid
 'h' key toggles between toroid and helix
 """
def keyPressed():
    global pts, segments, isHelix, isWireFrame, latheRadius, radius

    # clear the list of strips, to force a re-evaluation
    del strips[:]

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
    elif key == 'a':
        if latheRadius > 0:
            latheRadius -= 1
    elif key == 's':
        latheRadius += 1
    # ellipse radius
    elif key == 'z':
        if radius > 10:
            radius -= 1
    elif key == 'x':
        radius += 1
    # wireframe
    elif key == 'w':
        isWireFrame = not isWireFrame
    # helix
    elif key == 'h':
        isHelix = not isHelix
