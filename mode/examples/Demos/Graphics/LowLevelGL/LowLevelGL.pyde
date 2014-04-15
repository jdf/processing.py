# Draws a triangle using low-level OpenGL calls.

import array

from java.nio import ByteBuffer, ByteOrder
from java.lang import Float


def allocateDirectFloatBuffer(n):
    return (ByteBuffer.allocateDirect(n * Float.SIZE / 8).
            order(ByteOrder.nativeOrder()).asFloatBuffer())

vertices = array.array('f', (0,) * 12)
vertData = allocateDirectFloatBuffer(12)
colors = array.array('f', (0,) * 12)
colorData = allocateDirectFloatBuffer(12)


def setup():
    size(640, 360, P3D)
    global sh
    # Loads a shader to render geometry w/out textures and lights.
    sh = loadShader("frag.glsl", "vert.glsl")


def draw():
    background(0)

    # The geometric transformations will be automatically passed
    # to the shader.
    rotate(frameCount * 0.01, width, height, 0)

    updateGeometry()

    pgl = g.beginPGL()
    sh.bind()

    vertLoc = pgl.getAttribLocation(sh.glProgram, "vertex")
    colorLoc = pgl.getAttribLocation(sh.glProgram, "color")

    pgl.enableVertexAttribArray(vertLoc)
    pgl.enableVertexAttribArray(colorLoc)

    pgl.vertexAttribPointer(vertLoc, 4, PGL.FLOAT, False, 0, vertData)
    pgl.vertexAttribPointer(colorLoc, 4, PGL.FLOAT, False, 0, colorData)
    pgl.drawArrays(PGL.TRIANGLES, 0, 3)
    pgl.disableVertexAttribArray(vertLoc)
    pgl.disableVertexAttribArray(colorLoc)

    sh.unbind()
    g.endPGL()


def updateGeometry():
    # Vertex 1
    vertices[0] = 0
    vertices[1] = 0
    vertices[2] = 0
    vertices[3] = 1
    colors[0] = 1
    colors[1] = 0
    colors[2] = 0
    colors[3] = 1
    # Corner 2
    vertices[4] = width / 2
    vertices[5] = height
    vertices[6] = 0
    vertices[7] = 1
    colors[4] = 0
    colors[5] = 1
    colors[6] = 0
    colors[7] = 1
    # Corner 3
    vertices[8] = width
    vertices[9] = 0
    vertices[10] = 0
    vertices[11] = 1
    colors[8] = 0
    colors[9] = 0
    colors[10] = 1
    colors[11] = 1

    vertData.rewind()
    vertData.put(vertices)
    vertData.position(0)

    colorData.rewind()
    colorData.put(colors)
    colorData.position(0)
