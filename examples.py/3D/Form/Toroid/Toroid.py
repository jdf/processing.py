"""
 * Interactive Toroid
 * PDE by Ira Greenberg, adapted to Python by Jonathan Feinberg 
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

from processing.core import PVector

pts = 40 
radius = 60.0

# lathe segments
segments = 60
latheAngle = 0
latheRadius = 100.0

# for shaded or wireframe rendering 
isWireFrame = False

# for optional helix
isHelix = False
helixOffset = 5.0

def setup():
    size(640, 360, OPENGL)

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
    
    #center and spin toroid
    translate(width / 2, height / 2, -100)
    rotateX(frameCount * PI / 150)
    rotateY(frameCount * PI / 170)
    rotateZ(frameCount * PI / 90)
    # initialize point arrays
    vertices = [PVector() for x in range(pts + 1)]
    vertices2 = [PVector() for x in range(pts + 1)]
    # fill arrays
    angle = 0
    for v in vertices:
        v.x = latheRadius + sin(radians(angle)) * radius
        if isHelix:
            v.z = cos(radians(angle)) * radius - (helixOffset * segments) / 2
        else:
            v.z = cos(radians(angle)) * radius
        angle += 360.0 / pts
    
    # draw toroid
    latheAngle = 0
    for i in range(segments + 1):
        beginShape(QUAD_STRIP)
        for j in range(pts + 1):
            v2 = vertices2[j]
            if i > 0:
                vertex(v2.x, v2.y, v2.z)
            
            v2.x = cos(radians(latheAngle)) * vertices[j].x
            v2.y = sin(radians(latheAngle)) * vertices[j].x
            v2.z = vertices[j].z
            # optional helix offset
            if isHelix:
                vertices[j].z += helixOffset
             
            vertex(v2.x, v2.y, v2.z)
        # create extra rotation for helix
        if isHelix:
            latheAngle += 720.0 / segments
        else:
            latheAngle += 360.0 / segments
        
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
    if key == ord('a'):
        if latheRadius > 0:
            latheRadius -= 1
    elif key == ord('s'):
        latheRadius += 1
    # ellipse radius
    if key == ord('z'):
        if radius > 10:
            radius -= 1
    elif key == ord('x'):
        radius += 1
    # wireframe
    if key == ord('w'):
        isWireFrame = not isWireFrame
    # helix
    if key == ord('h'):
        isHelix = not isHelix
