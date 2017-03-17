"""
Simple DXF Export by Simon Greenwold.

Press the 'R' key to export a DXF file.
"""

add_library('dxf')  # import processing.dxf.*
record = False

def setup():
    size(400, 400, P3D)
    noStroke()
    sphereDetail(12)

def draw():
    global record
    if record:
        beginRaw(DXF, "output.dxf")  # Start recording to the file
    lights()
    background(0)
    translate(width / 3, height / 3, -200)
    rotateZ(map(mouseY, 0, height, 0, PI))
    rotateY(map(mouseX, 0, width, 0, HALF_PI))
    for y in range(-2, 2):
        for x in range(-2, 2):
            for z in range(-2, 2):
                pushMatrix()
                translate(120 * x, 120 * y, -120 * z)
                sphere(30)
                popMatrix()
    if record:
        endRaw()
        record = False  # Stop recording to the file

def keyPressed():
    global record
    if key == 'R' or key == 'r':
        # Press R to save the file
        record = True
