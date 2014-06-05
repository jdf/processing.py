"""
DomeProjection

This sketch uses use environmental mapping to render the output 
on a full spherical dome.

Based on the FullDomeTemplate code from Christopher Warnow: 
https://github.com/mphasize/FullDome
"""

import java.nio.IntBuffer
cubemapShader = None
domeSphere = None
fbo = None
rbo = None
envMapTextureID = None
envMapSize = 1024


def setup():
    size(640, 640, P3D)
    initCubeMap()


def draw():
    background(0)
    drawCubeMap()


def drawScene():
    background(0)
    stroke(255, 0, 0)
    strokeWeight(2)
    for i in range(-width, 2 * width, 50):
        line(i, -height, -100, i, 2 * height, -100)
    for i in range(height, 2 * height, 50):
        line(-width, i, -100, 2 * width, i, -100)
    lights()
    noStroke()
    translate(mouseX, mouseY, 200)
    rotateX(frameCount * 0.01)
    rotateY(frameCount * 0.01)
    box(100)


def initCubeMap():
    sphereDetail(50)
    domeSphere = createShape(SPHERE, height / 2.0)
    domeSphere.rotateX(HALF_PI)
    domeSphere.setStroke(False)
    pgl = beginPGL()
    envMapTextureID = IntBuffer.allocate(1)
    pgl.genTextures(1, envMapTextureID)
    pgl.bindTexture(PGL.TEXTURE_CUBE_MAP, envMapTextureID.get(0))
    pgl.texParameteri(
        PGL.TEXTURE_CUBE_MAP, PGL.TEXTURE_WRAP_S, PGL.CLAMP_TO_EDGE)
    pgl.texParameteri(
        PGL.TEXTURE_CUBE_MAP, PGL.TEXTURE_WRAP_T, PGL.CLAMP_TO_EDGE)
    pgl.texParameteri(
        PGL.TEXTURE_CUBE_MAP, PGL.TEXTURE_WRAP_R, PGL.CLAMP_TO_EDGE)
    pgl.texParameteri(
        PGL.TEXTURE_CUBE_MAP, PGL.TEXTURE_MIN_FILTER, PGL.NEAREST)
    pgl.texParameteri(
        PGL.TEXTURE_CUBE_MAP, PGL.TEXTURE_MAG_FILTER, PGL.NEAREST)
    for i in range(PGL.TEXTURE_CUBE_MAP_POSITIVE_X, PGL.TEXTURE_CUBE_MAP_POSITIVE_X + 6):
        pgl.texImage2D(
            i, 0, PGL.RGBA8, envMapSize, envMapSize, 0, PGL.RGBA, PGL.UNSIGNED_BYTE, null)
    # Init fbo, rbo
    fbo = IntBuffer.allocate(1)
    rbo = IntBuffer.allocate(1)
    pgl.genFramebuffers(1, fbo)
    pgl.bindFramebuffer(PGL.FRAMEBUFFER, fbo.get(0))
    pgl.framebufferTexture2D(PGL.FRAMEBUFFER, PGL.COLOR_ATTACHMENT0,
                             PGL.TEXTURE_CUBE_MAP_POSITIVE_X, envMapTextureID.get(0), 0)
    pgl.genRenderbuffers(1, rbo)
    pgl.bindRenderbuffer(PGL.RENDERBUFFER, rbo.get(0))
    pgl.renderbufferStorage(
        PGL.RENDERBUFFER, PGL.DEPTH_COMPONENT24, envMapSize, envMapSize)
    # Attach depth buffer to FBO
    pgl.framebufferRenderbuffer(
        PGL.FRAMEBUFFER, PGL.DEPTH_ATTACHMENT, PGL.RENDERBUFFER, rbo.get(0))
    endPGL()
    # Load cubemap shader.
    cubemapShader = loadShader("cubemapfrag.glsl", "cubemapvert.glsl")
    cubemapShader.set("cubemap", 1)


def drawCubeMap():
    pgl = beginPGL()
    pgl.activeTexture(PGL.TEXTURE1)
    pgl.enable(PGL.TEXTURE_CUBE_MAP)
    pgl.bindTexture(PGL.TEXTURE_CUBE_MAP, envMapTextureID.get(0))
    regenerateEnvMap(pgl)
    endPGL()
    drawDomeMaster()
    pgl.disable(PGL.TEXTURE_CUBE_MAP)
    pgl.bindTexture(PGL.TEXTURE_CUBE_MAP, 0)


def drawDomeMaster():
    camera()
    ortho(0, width, 0, height)
    resetMatrix()
    shader(cubemapShader)
    shape(domeSphere)
    resetShader()

# Called to regenerate the envmap
def regenerateEnvMap(pgl):
    # bind fbo
    pgl.bindFramebuffer(PGL.FRAMEBUFFER, fbo.get(0))
    # generate 6 views from origin(0, 0, 0)
    pgl.viewport(0, 0, envMapSize, envMapSize)
    perspective(90.0 * DEG_TO_RAD, 1.0, 1.0, 1025.0)
    for face in range(PGL.TEXTURE_CUBE_MAP_POSITIVE_X, PGL.TEXTURE_CUBE_MAP_NEGATIVE_Z):
        resetMatrix()
        if face == PGL.TEXTURE_CUBE_MAP_POSITIVE_X:
            camera(0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, -1.0, 0.0)
        elif face == PGL.TEXTURE_CUBE_MAP_NEGATIVE_X:
            camera(0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, -1.0, 0.0)
        elif face == PGL.TEXTURE_CUBE_MAP_POSITIVE_Y:
            camera(0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, -1.0)
        elif face == PGL.TEXTURE_CUBE_MAP_NEGATIVE_Y:
            camera(0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0)
        elif face == PGL.TEXTURE_CUBE_MAP_POSITIVE_Z:
            camera(0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, -1.0, 0.0)
        scale(-1, 1, -1)
        translate(-width * 0.5, -height * 0.5, -500)
        pgl.framebufferTexture2D(
            PGL.FRAMEBUFFER, PGL.COLOR_ATTACHMENT0, face, envMapTextureID.get(0), 0)
        drawScene()  # Draw objects in the scene
        # Make sure that the geometry in the scene is pushed to the GPU
        flush()
        noLights()  # Disabling lights to avoid adding many times
        pgl.framebufferTexture2D(
            PGL.FRAMEBUFFER, PGL.COLOR_ATTACHMENT0, face, 0, 0)

