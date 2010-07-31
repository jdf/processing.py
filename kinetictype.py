"""
 Kinetic Type 
 by Zach Lieberman. 
 Adapted to Python by Jonathan Feinberg
 Using push() and pop() to define the curves of the lines of type. 
"""

words = [
          "sometimes it's like", "the lines of text", "are so happy", 
          "that they want to dance", "or leave the page or jump",
          "can you blame them?", "living on the page like that",
          "waiting to be read..."
        ]

def setup():
    size(640, 360, P3D)
    textFont(loadFont("Univers-66.vlw"), 1.0)
    fill(255)
    frameRate(1000)

def draw():
    background(0)
    pushMatrix()
    translate(-200, -50, -450)
    rotateY(0.3)
    
    # Now animate every line object & draw it...
    for i in range(len(words)):
        f1 = sin((i + 1.0) * (millis() / 10000.0) * TWO_PI)
        f2 = sin((8.0 - i) * (millis() / 10000.0) * TWO_PI)
        line = words[i]
        pushMatrix()
        translate(0.0, i*75, 0.0)
        for j in range(len(line)):
            if j != 0:
                translate(textWidth(line[j - 1]) * 75, 0.0, 0.0)
            rotateY(f1 * 0.005 * f2)
            pushMatrix()
            scale(75.0)
            text(line[j], 0.0, 0.0)
            popMatrix()
        popMatrix()
    popMatrix()
    scale(20)
    text("%d fps"%int(frameRate), .5, 1.)
