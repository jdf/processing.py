add_library('peasycam')

def setup():
    global cam 
    size(200, 200, P3D)
    cam = PeasyCam(this, 100)
    cam.setMinimumDistance(50)
    cam.setMaximumDistance(500)

def draw():
    rotateX(-.5)
    rotateY(-.5)
    background(0)
    fill(255, 0, 0)
    box(30)
    with pushMatrix():
        translate(0,0,20)
        fill(0,0,255)
        box(5)
