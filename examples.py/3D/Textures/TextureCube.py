"""
 * TexturedCube
 * based on pde example by Dave Bollinger.
 * 
 * Drag mouse to rotate cube. Demonstrates use of u/v coords in 
 * vertex() and effect on texture().
"""
tex = loadImage("data/berlin-1.jpg")
rotx = PI / 4
roty = PI / 4
rate = 0.01

def setup(): 
    size(640, 360, OPENGL)
    textureMode(NORMAL)
    fill(255)
    stroke(color(44, 48, 32))

def draw(): 
    background(0)
    noStroke()
    translate(width / 2.0, height / 2.0, -100)
    rotateX(rotx)
    rotateY(roty)
    scale(90)
    TexturedCube()

def TexturedCube():
    beginShape(QUADS)
    texture(tex)
    # Given one texture and six faces, we can easily set up the uv coordinates
    # such that four of the faces tile "perfectly" along either u or v, but the other
    # two faces cannot be so aligned.    This code tiles "along" u, "around" the X / Z faces
    # and fudges the Y faces - the Y faces are arbitrarily aligned such that a
    # rotation along the X axis will put the "top" of either texture at the "top"
    # of the screen, but is not otherwised aligned with the X / Z faces. (This
    # just affects what type of symmetry is required if you need seamless
    # tiling all the way around the cube)
    
    # +Z "front" face
    vertex(-1, -1, 1, 0, 0)
    vertex(1, -1, 1, 1, 0)
    vertex(1, 1, 1, 1, 1)
    vertex(-1, 1, 1, 0, 1)
    # -Z "back" face
    vertex(1, -1, -1, 0, 0)
    vertex(-1, -1, -1, 1, 0)
    vertex(-1, 1, -1, 1, 1)
    vertex(1, 1, -1, 0, 1)
    # +Y "bottom" face
    vertex(-1, 1, 1, 0, 0)
    vertex(1, 1, 1, 1, 0)
    vertex(1, 1, -1, 1, 1)
    vertex(-1, 1, -1, 0, 1)
    # -Y "top" face
    vertex(-1, -1, -1, 0, 0)
    vertex(1, -1, -1, 1, 0)
    vertex(1, -1, 1, 1, 1)
    vertex(-1, -1, 1, 0, 1)
    # +X "right" face
    vertex(1, -1, 1, 0, 0)
    vertex(1, -1, -1, 1, 0)
    vertex(1, 1, -1, 1, 1)
    vertex(1, 1, 1, 0, 1)
    # -X "left" face
    vertex(-1, -1, -1, 0, 0)
    vertex(-1, -1, 1, 1, 0)
    vertex(-1, 1, 1, 1, 1)
    vertex(-1, 1, -1, 0, 1)
    endShape()
    
def mouseDragged():
    global rotx, roty
    rotx += (pmouseY - mouseY) * rate
    roty += (mouseX - pmouseX) * rate
