import processing.opengl.PGraphics3D

def setup():
    size(100, 100, P3D)

def draw():
    # check that the alias cameraMatrix->camera is working as expected
    g.camera(0, 0, -10, 0, 0, 0, 0, 1, 0)
    assert(g.cameraMatrix.m03 == 0)
    assert(g.cameraMatrix.m23 == -10)
    print 'OK'
    exit()
