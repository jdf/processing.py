"""
PDF Complex by Marius Watz (workshop.evolutionzone.com).

Example using PDF to output complex 3D geometry for print.
Press "s" to save a PDF.
"""

add_library('pdf')  # import processing.pdf.*

# Trig lookup tables (sinLUT and cosLUT) borrowed from Toxi. Cryptic but
# effective
SINCOS_PRECISION = 1.0
SINCOS_LENGTH = int(360.0 / SINCOS_PRECISION)

# System data
do_save = False

def setup():
    global sinLUT, cosLUT, num, pt, style
    size(600, 600, OPENGL)
    frameRate(24)
    background(255)

    # Fill the tables
    sinLUT = [sin(i * DEG_TO_RAD * SINCOS_PRECISION)
              for i in range(SINCOS_LENGTH)]
    cosLUT = [cos(i * DEG_TO_RAD * SINCOS_PRECISION)
              for i in range(SINCOS_LENGTH)]
    num = 150
    pt = [0.0 for _ in range(6 * num)]  # rotx, roty, deg, rad, w, speed
    style = [0 for _ in range(2 * num)]  # color, render style

    # Set up arc shapes
    index = 0
    for i in range(num):
        pt[index] = random(TWO_PI)  # Random X axis rotation
        index += 1
        pt[index] = random(TWO_PI)  # Random Y axis rotation
        index += 1
        
        pt[index] = random(60, 80)  # Short to quarter-circle arcs
        if random(100) > 90: pt[index] = int(random(8, 27) * 10.0)
        index += 1  # correction on March 19th 2017 by Watz
        
        pt[index] = int(random(2, 50) * 5.0)  # Radius. Space them out nicely
        index += 1
        
        pt[index] = random(4, 32)  # Width of band
        if random(100) > 90: pt[index] = random(40, 60)  # Width of band
        index += 1  # correction on March 19th 2017 by Watz
        
        pt[index] = radians(random(5, 30)) / 5.0  # Speed of rotation
        index += 1
        
        # get colors
        prob = random(100)
        if prob < 30: style[i * 2] = rgb_blend(random(1), 255, 0, 100, 255, 0, 0, 210)
        elif prob < 70: style[i * 2] = rgb_blend(random(1), 0, 153, 255, 170, 225, 255, 210)
        elif prob < 90: style[i * 2] = rgb_blend(random(1), 200, 255, 0, 150, 255, 0, 210)
        else: style[i * 2] = color(255, 255, 255, 220)

        if prob < 50: style[i * 2] = rgb_blend(random(1), 200, 255, 0, 50, 120, 0, 210)
        elif prob < 90: style[i * 2] = rgb_blend(random(1), 255, 100, 0, 255, 255, 0, 210)
        else: style[i * 2] = color(255, 255, 255, 220)

        style[i * 2 + 1] = int(random(100)) % 3

def draw():
    global do_save
    if do_save:
        # set up PGraphicsPDF for use with beginRaw()
        pdf = beginRaw(PDF, "pdf_complex_out.pdf")
        # set default Illustrator stroke styles and paint background rect.
        pdf.strokeJoin(MITER)
        pdf.strokeCap(SQUARE)
        pdf.fill(0)
        pdf.noStroke()
        pdf.rect(0, 0, width, height)

    background(0)

    index = 0
    translate(width / 2, height / 2, 0)
    rotateX(PI / 6.0)
    rotateY(PI / 6.0)

    for i in range(num):
        pushMatrix()

        rotateX(pt[index])
        index += 1
        rotateY(pt[index])
        index += 1

        if style[i * 2 + 1] == 0:
            stroke(style[i * 2])
            noFill()
            strokeWeight(1)
            arc_line(0, 0, pt[index], pt[index + 1], pt[index + 2])
            index += 3
        elif style[i * 2 + 1] == 1:
            fill(style[i * 2])
            noStroke()
            arc_line_bars(0, 0, pt[index], pt[index + 1], pt[index +2])
            index += 3

        else:
            fill(style[i * 2])
            noStroke()
            arc(0, 0, pt[index], pt[index + 1], pt[index + 2])
            index += 3

        # increase rotation
        pt[index - 5] += pt[index] / 10.0
        pt[index - 4] += pt[index] / 20.0

        popMatrix()

    if do_save:
        endRaw()
        do_save = False

# Get blend of two colors
def rgb_blend(fract, r, g, b, r2, g2, b2, a):
    r2, g2, b2 = (r2 - r), (g2 - g), (b2 - b)
    return color(r + r2 * fract, g + g2 * fract, b + b2 * fract, a)

# Draw arc line
def arc_line(x, y, deg, rad, w):
    a = int(min(deg / SINCOS_PRECISION, SINCOS_LENGTH - 1.0))
    numlines = int(w / 2)

    for j in range(numlines):
        beginShape()
        for i in range(a):
            vertex(cosLUT[i] * rad + x,
                   sinLUT[i] * rad + y)
        endShape()
        rad += 2

# Draw arc line with bars
def arc_line_bars(x, y, deg, rad, w):
    a = int((min(deg / SINCOS_PRECISION, SINCOS_LENGTH - 1.0)))
    a /= 4

    beginShape(QUADS)
    for i in range(0, a, 4):
        vertex(cosLUT[i] * (rad) + x,
               sinLUT[i] * (rad) + y)
        vertex(cosLUT[i] * (rad + w) + x,
               sinLUT[i] * (rad + w) + y)
        vertex(cosLUT[i + 2] * (rad + w) + x,
               sinLUT[i + 2] * (rad + w) + y)
        vertex(cosLUT[i + 2] * (rad) + x,
               sinLUT[i + 2] * (rad) + y)
    endShape()

# Draw solid arc
def arc(x, y, deg, rad, w):
    a = int(min(deg / SINCOS_PRECISION, SINCOS_LENGTH - 1.0))
    beginShape(QUAD_STRIP)
    for i in range(a):
        vertex(cosLUT[i] * (rad) + x,
               sinLUT[i] * (rad) + y)
        vertex(cosLUT[i] * (rad + w) + x,
               sinLUT[i] * (rad + w) + y)
    endShape()

def keyPressed():
    if (key == 's'):
        do_save = True

def mouseReleased():
    background(255)
