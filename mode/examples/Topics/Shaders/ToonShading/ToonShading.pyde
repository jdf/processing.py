"""
Toon Shading.

Example showing the use of a custom lighting shader in order    
to apply a "toon" effect on the scene. Based on the glsl tutorial 
from lighthouse 3D:
http://www.lighthouse3d.com/tutorials/glsl-tutorial/toon-shader-version-ii/
"""

toon = None
shaderEnabled = True


def setup():
    global toon
    size(640, 360, P3D)
    noStroke()
    fill(204)
    toon = loadShader("ToonFrag.glsl", "ToonVert.glsl")


def draw():
    if shaderEnabled:
        shader(toon)
    noStroke()
    background(0)
    dirY = (mouseY / float(height) - 0.5) * 2
    dirX = (mouseX / float(width) - 0.5) * 2
    directionalLight(204, 204, 204, -dirX, -dirY, -1)
    translate(width / 2, height / 2)
    sphere(120)


def mousePressed():
    global shaderEnabled
    shaderEnabled = not shaderEnabled
    if not shaderEnabled:
        resetShader()
