"""
Texture Sphere
by Mike 'Flux' Chang.
Based on code by Toxi.

A 3D textured sphere with simple rotation control.
Note: Controls will be inverted when sphere is upside down.
Use an "arc ball" to deal with this appropriately.
"""

thirdWidth = None
halfHeight = None
texmap = None

# Sphere detail setting.
sphereRes = 35
rotationX = 0
rotationY = 0
velocityX = 0
velocityY = 0
globeRadius = 400
pushBack = 0

# float lists
cx = []
cz = []
sphereX = []
sphereY = []
sphereZ = []
sinLUT = []
cosLUT = []

SinCosPrecision = 0.5
SinCosLength = int(360.0 / SinCosPrecision)


def setup():
    size(640, 360, P3D)
    global thirdWidth, halfHeight, texmap
    thirdWidth = width * 0.33
    halfHeight = height * 0.5
    texmap = loadImage("world32k.jpg")
    initializeSphere(sphereRes)


def draw():
    background(0)
    renderGlobe()


def renderGlobe():
    global rotationX, rotationY, velocityX, velocityY
    with pushMatrix():
        translate(thirdWidth, halfHeight, pushBack)

        with pushMatrix():
            noFill()
            stroke(255, 200)
            strokeWeight(2)
            smooth()

        lights()

        with pushMatrix():
            rotateX(radians(-rotationX))
            rotateY(radians(270 - rotationY))
            fill(200)
            noStroke()
            textureMode(IMAGE)
            texturedSphere(globeRadius, texmap)

    rotationX += velocityX
    rotationY += velocityY
    velocityX *= 0.95
    velocityY *= 0.95

    # Implements mouse control (interaction will be inverted when sphere is
    # upside down).
    if mousePressed:
        velocityX += (mouseY - pmouseY) * 0.01
        velocityY -= (mouseX - pmouseX) * 0.01


def initializeSphere(res):
    global sphereRes
    for i in range(SinCosLength):
        sinLUT.append(sin(radians(i * SinCosPrecision)))
        cosLUT.append(cos(radians(i * SinCosPrecision)))
    delta = SinCosLength / res

    # Calc unit circle in XZ plane.
    for i in range(res):
        cx.append(-cosLUT[int((i * delta) % SinCosLength)])
        cz.append(sinLUT[int((i * delta) % SinCosLength)])

    # Computing Vertex list. Vertex list starts at south pole.
    vertCount = res * (res - 1) + 2
    angle_step = (SinCosLength * 0.5) / res
    angle = angle_step

    # Step along Y axis.
    for i in range(1, res):
        curradius = sinLUT[int(angle % SinCosLength)]
        currY = -cosLUT[int(angle % SinCosLength)]
    # Init lists to store vertices.
        for j in range(res):
            sphereX.append(cx[j] * curradius)
            sphereY.append(currY)
            sphereZ.append(cz[j] * curradius)
        angle += angle_step
    sphereRes = res


# Generic routine to draw textured sphere.
def texturedSphere(radius, texmap):
    radius = (radius + 240) * 0.33

    beginShape(TRIANGLE_STRIP)
    texture(texmap)
    iu = (texmap.width - 1) / sphereRes
    iv = (texmap.height - 1) / sphereRes
    u = 0
    v = iv
    for i in range(sphereRes):
        vertex(0, -radius, 0, u, 0)
        vertex(sphereX[i] * radius,
               sphereY[i] * radius,
               sphereZ[i] * radius,
               u, v)
        u += iu
    vertex(0, -radius, 0, u, 0)
    vertex(sphereX[0] * radius,
           sphereY[0] * radius,
           sphereZ[0] * radius,
           u, v)
    endShape()

    # Middle rings.
    voff = 0
    for i in range(2, sphereRes):
        v1 = voff
        v11 = voff
        voff += sphereRes
        v2 = voff
        u = 0
        beginShape(TRIANGLE_STRIP)
        texture(texmap)
        for j in range(sphereRes):
            vertex(sphereX[v1] * radius,
                   sphereY[v1] * radius,
                   sphereZ[v1] * radius,
                   u, v)
            v1 += 1
            vertex(sphereX[v2] * radius,
                   sphereY[v2] * radius,
                   sphereZ[v2] * radius,
                   u, v + iv)
            v2 += 1
            u += iu

        # Close each ring.
        v1 = v11
        v2 = voff
        vertex(sphereX[v1] * radius,
               sphereY[v1] * radius,
               sphereZ[v1] * radius,
               u, v)
        vertex(sphereX[v2] * radius,
               sphereY[v2] * radius,
               sphereZ[v2] * radius,
               u, v + iv)
        endShape()
        v += iv
    u = 0

    # Add the northern cap.
    beginShape(TRIANGLE_STRIP)
    texture(texmap)
    for i in range(sphereRes):
        v2 = voff + i
        vertex(sphereX[v2] * radius,
               sphereY[v2] * radius,
               sphereZ[v2] * radius,
               u, v)
        vertex(0, radius, 0, u, v + iv)
        u += iu
    vertex(sphereX[voff] * radius,
           sphereY[voff] * radius,
           sphereZ[voff] * radius,
           u, v)
    endShape()
