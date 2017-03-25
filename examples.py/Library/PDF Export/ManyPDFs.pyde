"""
Many PDFs. 

Saves one PDF file each each frame while the mouse is pressed.
When the mouse is released, the PDF creation stops.
"""


add_library('pdf')

savePDF = False

def setup():
    size(600, 600)
    frameRate(24)

def draw():
    if savePDF:
        beginRecord(PDF, "lines%d.pdf" % (frameCount))
    
    background(255) 
    stroke(0, 20)
    strokeWeight(20.0)
    line(mouseX, 0, width-mouseY, height)

    if savePDF:
        endRecord()
    
def mousePressed():
    global savePDF
    savePDF = True

def mouseReleased():
    global savePDF
    savePDF = False