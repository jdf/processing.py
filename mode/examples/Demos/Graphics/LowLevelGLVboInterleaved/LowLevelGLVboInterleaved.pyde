# Draws a triangle using low-level OpenGL calls.

import array

from java.nio import ByteBuffer, ByteOrder, IntBuffer
from java.lang import Float

VERT_CMP_COUNT = 4  # vertex component count (x, y, z, w) -> 4
CLR_CMP_COUNT = 4  # color component count (r, g, b, a) -> 4

def allocateDirectFloatBuffer(n):
    return (ByteBuffer.allocateDirect(n * Float.SIZE / 8).
            order(ByteOrder.nativeOrder()).asFloatBuffer())

attribs = array.array('f', (0,) * 24)
attribBuffer = allocateDirectFloatBuffer(24)

def setup():
    size(640, 360, P3D)

    # Loads a shader to render geometry w/out textures and lights.
    global sh
    sh = loadShader("frag.glsl", "vert.glsl")

    with beginPGL() as pgl:
	    intBuffer = IntBuffer.allocate(1)
	    pgl.genBuffers(1, intBuffer)
	    global attribVboId
	    attribVboId = intBuffer.get(0)

def draw():
    with g.beginPGL() as pgl:
	
	    background(0)
	
	    # The geometric transformations will be automatically passed
	    # to the shader.
	    rotate(frameCount * 0.01, width, height, 0)
	
	    updateGeometry()
	
	    sh.bind()
	
	    # get "vertex" attribute location in the shader
	    vertLoc = pgl.getAttribLocation(sh.glProgram, "vertex")
	    # enable array for "vertex" attribute
	    pgl.enableVertexAttribArray(vertLoc)
	
	    # get "color" attribute location in the shader
	    colorLoc = pgl.getAttribLocation(sh.glProgram, "color")
	    # enable array for "color" attribute
	    pgl.enableVertexAttribArray(colorLoc)
	
	    # BUFFER LAYOUT from updateGeometry()
	
	    # xyzwrgbaxyzwrgbaxyzwrgba...
	    #
	    # |v1       |v2       |v3       |...
	    # |0   |4   |8   |12  |16  |20  |...
	    # |xyzw|rgba|xyzw|rgba|xyzw|rgba|...
	    #
	    # stride (values per vertex) is 8 floats
	    # vertex offset is 0 floats (starts at the beginning of each line)
	    # color offset is 4 floats (starts after vertex coords)
	    #
	    #    |0   |4   |8
	    # v1 |xyzw|rgba|
	    # v2 |xyzw|rgba|
	    # v3 |xyzw|rgba|
	    #    |...
	
	    stride = (VERT_CMP_COUNT + CLR_CMP_COUNT) * Float.BYTES
	    vertexOffset = 0 * Float.BYTES
	    colorOffset = VERT_CMP_COUNT * Float.BYTES
	
	    # bind VBO
	    pgl.bindBuffer(PGL.ARRAY_BUFFER, attribVboId)
	    # fill VBO with data
	    pgl.bufferData(
	        PGL.ARRAY_BUFFER, Float.BYTES * len(attribs), attribBuffer, PGL.DYNAMIC_DRAW)
	    # associate currently bound VBO with "vertex" shader attribute
	    pgl.vertexAttribPointer(
	        vertLoc, VERT_CMP_COUNT, PGL.FLOAT, False, stride, vertexOffset)
	    # associate currently bound VBO with "color" shader attribute
	    pgl.vertexAttribPointer(
	        colorLoc, CLR_CMP_COUNT, PGL.FLOAT, False, stride, colorOffset)
	    # unbind VBO
	    pgl.bindBuffer(PGL.ARRAY_BUFFER, 0)
	
	    pgl.drawArrays(PGL.TRIANGLES, 0, 3)
	
	    # disable arrays for attributes before unbinding the shader
	    pgl.disableVertexAttribArray(vertLoc)
	    pgl.disableVertexAttribArray(colorLoc)
	
	    sh.unbind()

def updateGeometry():
    # Vertex 1
    attribs[0] = 0
    attribs[1] = 0
    attribs[2] = 0
    attribs[3] = 1
    
    # Color 1
    attribs[4] = 1
    attribs[5] = 0
    attribs[6] = 0
    attribs[7] = 1
    
    # Vertex 2
    attribs[8] = width/2
    attribs[9] = height
    attribs[10] = 0
    attribs[11] = 1
    
    # Color 2
    attribs[12] = 0
    attribs[13] = 1
    attribs[14] = 0
    attribs[15] = 1
    
    # Vertex 3
    attribs[16] = width
    attribs[17] = 0
    attribs[18] = 0
    attribs[19] = 1
    
    # Color 3
    attribs[20] = 0
    attribs[21] = 0
    attribs[22] = 1
    attribs[23] = 1
    
    attribBuffer.rewind()
    attribBuffer.put(attribs)
    attribBuffer.rewind()
    