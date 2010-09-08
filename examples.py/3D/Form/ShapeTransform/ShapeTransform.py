"""
  Shape Transform
  by Ira Greenberg.
  (Rewritten in Python by Jonathan Feinberg.)

  Illustrates the geometric relationship
  between Cube, Pyramid, Cone and
  Cylinder 3D primitives.

  Instructions:
  Up Arrow - increases points
  Down Arrow - decreases points
  'p' key toggles between cube/pyramid
 """

# constants
radius = 99
cylinderLength = 95
angleInc = PI / 300.0

# globals that can be chaned by the user
pts = 12
isPyramid = False

def setup():
    size(640, 360, P3D)
    noStroke()

def draw():
    background(170, 95, 95)
    lights()
    fill(255, 200, 200)
    translate(width / 2, height / 2)
    rotateX(frameCount * angleInc)
    rotateY(frameCount * angleInc)
    rotateZ(frameCount * angleInc)

    dTheta = TWO_PI / pts
    x = lambda(j): cos(dTheta * j) * radius
    y = lambda(j): sin(dTheta * j) * radius

    # draw cylinder tube
    beginShape(QUAD_STRIP)
    for j in range(pts + 1):
        vertex(x(j), y(j), cylinderLength)
        if isPyramid:
            vertex(0, 0, -cylinderLength)
        else:
            vertex(x(j), y(j), -cylinderLength)
    endShape()
    #draw cylinder ends
    beginShape()
    for j in range(pts + 1):
        vertex(x(j), y(j), cylinderLength)
    endShape(CLOSE)
    if not isPyramid:
        beginShape()
        for j in range(pts + 1):
            vertex(x(j), y(j), -cylinderLength)
        endShape(CLOSE)

"""
 up/down arrow keys control
 polygon detail.
 """
def keyPressed():
    global pts, isPyramid
    if key == CODED:
        if keyCode == UP and pts < 90:
            pts += 1
        elif keyCode == DOWN and pts > 4:
            pts -= 1
    elif key == ord('p'):
        isPyramid = not isPyramid
