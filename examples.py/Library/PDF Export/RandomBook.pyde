"""
RandomBook
 
Creates a 768 page book of random lines.
"""

add_library('pdf')  # import processing.pdf.*

def setup():
    global pdf
    size(594, 842)
    # randomSeed(0) # Uncomment to make the same book each time
    pdf = beginRecord(PDF, "RandomBook.pdf")
    beginRecord(pdf)

def draw():
    background(255)

    for i in range(100):
        r = random(1.0)
        if r < 0.2:
            stroke(255)
        else:
            stroke(0)

        sw = pow(random(1.0), 12)
        strokeWeight(sw * 260)
        x1 = random(-200, -100)
        x2 = random(width + 100, width + 200)
        y1 = random(-100, height + 100)
        y2 = random(-100, height + 100)
        line(x1, y1, x2, y2)

    if frameCount == 768:
        endRecord()
        exit()    # Quit
    else:
        pdf.nextPage()  # Tell it to go to the next page
