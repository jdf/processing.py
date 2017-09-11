"""
Press 'w' to start/stop wiggling, space to restore original positions.
"""

cubeSize = 320
circleRad = 100
circleRes = 40
noiseMag = 1

wiggling = False


def setup():
    size(1024, 768, P3D)
    createCube()


def draw():
    background(0)
    translate(width / 2, height / 2)
    rotateX(frameCount * 0.01)
    rotateY(frameCount * 0.01)
    shape(cube)

    if wiggling:
        pos = None
        for i in range(cube.getChildCount()):
            face = cube.getChild(i)
            for j in range(face.getVertexCount()):
                pos = face.getVertex(j, pos)
                pos.x += random(-noiseMag / 2.0, +noiseMag / 2.0)
                pos.y += random(-noiseMag / 2.0, +noiseMag / 2.0)
                pos.z += random(-noiseMag / 2.0, +noiseMag / 2.0)
                face.setVertex(j, pos.x, pos.y, pos.z)

    if frameCount % 60 == 0:
        println(frameRate)


def keyPressed():
    global wiggling
    if key == 'w':
        wiggling = not wiggling
    elif key == ' ':
        restoreCube()
    elif key == '1':
        cube.setStrokeWeight(1)
    elif key == '2':
        cube.setStrokeWeight(5)
    elif key == '3':
        cube.setStrokeWeight(10)


def createCube():
    global cube
    cube = createShape(GROUP)
    # Create all faces at front position
    for _ in range(6):
        face = createShape()
        createFaceWithHole(face)
        cube.addChild(face)
    # Rotate all the faces to their positions
    # Front face - already correct
    face = cube.getChild(0)
    # Back face
    face = cube.getChild(1)
    face.rotateY(radians(180))
    # Right face
    face = cube.getChild(2)
    face.rotateY(radians(90))
    # Left face
    face = cube.getChild(3)
    face.rotateY(radians(-90))
    # Top face
    face = cube.getChild(4)
    face.rotateX(radians(90))
    # Bottom face
    face = cube.getChild(5)
    face.rotateX(radians(-90))


def createFaceWithHole(face):
    face.beginShape(POLYGON)
    face.stroke(255, 0, 0)
    face.fill(255)
    # Draw main shape Clockwise
    face.vertex(-cubeSize / 2, -cubeSize / 2, +cubeSize / 2)
    face.vertex(+cubeSize / 2, -cubeSize / 2, +cubeSize / 2)
    face.vertex(+cubeSize / 2, +cubeSize / 2, +cubeSize / 2)
    face.vertex(-cubeSize / 2, +cubeSize / 2, +cubeSize / 2)
    # Draw contour (hole) Counter-Clockwise
    face.beginContour()
    for i in range(circleRes):
        angle = TWO_PI * i / circleRes
        x = circleRad * sin(angle)
        y = circleRad * cos(angle)
        z = +cubeSize / 2
        face.vertex(x, y, z)
    face.endContour()
    face.endShape(CLOSE)


def restoreCube():
    # Rotation of faces is preserved, we just reset them the same way
    # as the "front" face and they will stay rotated correctly.
    for i in range(6):
        face = cube.getChild(i)
        restoreFaceWithHole(face)


def restoreFaceWithHole(face):
    face.setVertex(0, -cubeSize / 2, -cubeSize / 2, +cubeSize / 2)
    face.setVertex(1, +cubeSize / 2, -cubeSize / 2, +cubeSize / 2)
    face.setVertex(2, +cubeSize / 2, +cubeSize / 2, +cubeSize / 2)
    face.setVertex(3, -cubeSize / 2, +cubeSize / 2, +cubeSize / 2)
    for i in range(circleRes):
        angle = TWO_PI * i / circleRes
        x = circleRad * sin(angle)
        y = circleRad * cos(angle)
        z = +cubeSize / 2
        face.setVertex(4 + i, x, y, z)
