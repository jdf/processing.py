"""
 * Shape Transform
 * by Ira Greenberg.    
 * 
 * Illustrates the geometric relationship 
 * between Cube, Pyramid, Cone and 
 * Cylinder 3D primitives.
 * 
 * Instructions:<br />
 * Up Arrow - increases points<br />
 * Down Arrow - decreases points<br />
 * 'p' key toggles between cube/pyramid<br />
 """

from processing.core import PVector

pts = 4 
radius = 99
cylinderLength = 95
isPyramid = False
angleInc = PI / 300.0

def setup():
    size(640, 360, P3D)
    noStroke()
    
def draw():
    global cylinderLength
    
    background(170, 95, 95)
    lights()
    fill(255, 200, 200)
    translate(width / 2, height / 2)
    rotateX(frameCount * angleInc)
    rotateY(frameCount * angleInc)
    rotateZ(frameCount * angleInc)
    # initialize vertex arrays
    vertices = [[PVector() for x in range(pts+1)],
                [PVector() for x in range(pts+1)]]
    # fill arrays
    for i in range(2):
        angle = 0
        for v in vertices[i]:
            if isPyramid:
                if i == 1:
                    v.x = 0
                    v.y = 0
                else:
                    v.x = cos(radians(angle)) * radius
                    v.y = sin(radians(angle)) * radius
            else:
                v.x = cos(radians(angle)) * radius
                v.y = sin(radians(angle)) * radius
            v.z = cylinderLength 
            # the .0 after the 360 is critical
            angle += 360.0 / pts
        cylinderLength *= -1
    
    # draw cylinder tube
    beginShape(QUAD_STRIP)
    for j in range(pts+1):
        vertex(vertices[0][j].x, vertices[0][j].y, vertices[0][j].z)
        vertex(vertices[1][j].x, vertices[1][j].y, vertices[1][j].z)
    endShape()
    #draw cylinder ends
    for i in range(2):
        beginShape()
        for v in vertices[i]:
            vertex(v.x, v.y, v.z)
        endShape(CLOSE)
    
"""
 up/down arrow keys control
 polygon detail.
 """
def keyPressed():
    global pts, isPyramid
    print key
    if key == CODED:
        # pts
        if keyCode == UP and pts < 90:
            pts += 1
            print pts 
        elif keyCode == DOWN and pts > 4:
            pts -= 1
    elif key == ord('p'):
        isPyramid = not isPyramid
