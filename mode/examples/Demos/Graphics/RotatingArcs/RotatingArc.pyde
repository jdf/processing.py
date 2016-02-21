'''
 Geometry
 by Marius Watz.
 
 Using sin/cos lookup tables, blends colors, and draws a series of
 rotating arcs on the screen.
'''
# Trig lookup tables borrowed from Toxi cryptic but effective.
import math
sinLUT = []
cosLUT = []
SINCOS_PRECISION = 1.0
SINCOS_LENGTH = int((360.0 / SINCOS_PRECISION))
dosave = False
num = 0
pt = []
style = []

def setup():
    size(1024, 768, P3D)
    background(255)

    # Fill the tables
    for i in xrange(SINCOS_LENGTH):
        sinLUT.append(math.sin(i * DEG_TO_RAD * SINCOS_PRECISION))
        cosLUT.append(math.cos(i * DEG_TO_RAD * SINCOS_PRECISION))

    global style, pt, num
    num = 150
    for x in xrange(num * 2+1):
        style.append(0)

    # Set up arc shapes
    index = 0
    for i in xrange(num):
        pt.append(random(PI * 2))  # Random X axis rotation
        pt.append(random(PI * 2))  # Random Y axis rotation
        pt.append(random(60, 80))  # Short to quarter-circle arcs

        if(random(100) > 90):
            pt[index] = int(random(8, 27) * 10)
        pt.append(int(random(2, 50) * 5))  # Radius. Space them out nicely
        pt.append(random(4, 32))  # Width of band

        if(random(100) > 90):
            pt[index] = random(40, 60)  # Width of band
        pt.append(radians(random(5, 30)) / 5)  # Speed of rotation

        # get colors
        prob = random(100)
        if(prob < 30):
            style[i * 2] = colorBlended(random(1), 255, 0, 100, 255, 0, 0, 210)
        elif(prob < 70):
            style[
                i * 2] = colorBlended(random(1), 0, 153, 255, 170, 225, 255, 210)
        elif(prob < 90):
            style[
                i * 2] = colorBlended(random(1), 200, 255, 0, 150, 255, 0, 210)
        else:
            style[i * 2] = color(255, 255, 255, 220)

        if(prob < 50):
            style[
                i * 2] = colorBlended(random(1), 200, 255, 0, 50, 120, 0, 210)
        elif(prob < 90):
            style[
                i * 2] = colorBlended(random(1), 255, 100, 0, 255, 255, 0, 210)
        else:
            style[i * 2] = color(255, 255, 255, 220)

        style[i * 2 + 1] = int((random(100)) % 3)


def draw():
    background(0)
    translate(width / 2, height / 2, 0)
    rotateX(PI / 6)
    rotateY(PI / 6)
    #global index
    index=20        #getting arc at 20,80
    for i in xrange(num):
        pushMatrix()
        rotateX(pt[incre(index)])
        rotateY(pt[incre(index)])

        if(style[i * 2 + 1] == 0):
            stroke(style[i * 2])
            noFill()
            strokeWeight(1)
            arcLine(0, 0, pt[incre(index)], pt[incre(index)], pt[incre(index)])

        elif(style[i * 2 + 1] == 1):
            fill(style[i * 2])
            noStroke()
            arcLineBars(
                0, 0, pt[incre(index)], pt[incre(index)], pt[incre(index)])

        else:
            fill(style[i * 2])
            noStroke()
            arc(0, 0, pt[incre(index)], pt[incre(index)], pt[incre(index)])

        # increase rotation
        pt[index - 5] += (pt[index] / 10)
        pt[index - 4] += (pt[incre(index)] / 20)

        popMatrix()


def incre(index):
    index += 1
    return index

# Get blend of two colors
def colorBlended(fract, r, g, b, r2, g2, b2, a):
    r2 = (r2 - r)
    g2 = (g2 - g)
    b2 = (b2 - b)
    return color(r + r2 * fract, g + g2 * fract, b + b2 * fract, a)


# Draw arc line
def arcLine(x, y, deg, rad, w):
    a = int((min(deg / SINCOS_PRECISION, SINCOS_LENGTH - 1)))
    numlines = int((w / 2))

    for j in xrange(numlines):
        beginShape()
        for i in xrange(a):
            vertex(cosLUT[i] * rad + x, sinLUT[i] * rad + y)
        endShape()
        rad += 2


# Draw arc line with bars
def arcLineBars(x, y, deg, rad, w):
    a = int((min(deg / SINCOS_PRECISION, SINCOS_LENGTH - 1)))
    a /= 4

    beginShape(QUADS)
    for i in xrange(0, a, 4):
        vertex(cosLUT[i] * (rad) + x, sinLUT[i] * (rad) + y)
        vertex(cosLUT[i] * (rad + w) + x, sinLUT[i] * (rad + w) + y)
        vertex(cosLUT[i + 2] * (rad + w) + x, sinLUT[i + 2] * (rad + w) + y)
        vertex(cosLUT[i + 2] * (rad) + x, sinLUT[i + 2] * (rad) + y)

    endShape()


# Draw solid arc
def arc(x, y, deg, rad, w):
    a = int(min(deg / SINCOS_PRECISION, SINCOS_LENGTH - 1))
    beginShape(QUAD_STRIP)
    for i in xrange(a):
        vertex(cosLUT[i] * (rad) + x, sinLUT[i] * (rad) + y)
        vertex(cosLUT[i] * (rad + w) + x, sinLUT[i] * (rad + w) + y)

    endShape()
