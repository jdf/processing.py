"""
RGB Cube.

The three primary colors of the additive color model are red, green, and blue.
This RGB color cube displays smooth transitions between these colors.
"""

xmag = 0
ymag = 0


def setup():
    size(640, 360, P3D)
    noStroke()
    colorMode(RGB, 1)
    global halfWidth, halfHeight
    halfWidth = width / 2
    halfHeight = height / 2


def draw():
    global xmag, ymag
    background(0.5)

    with pushMatrix():
        translate(halfWidth, halfHeight, -30)
    
        newXmag = (mouseX / float(width)) * TAU
        newYmag = (mouseY / float(height)) * TAU
    
        diff = xmag - newXmag
        if abs(diff) > 0.01:
            xmag -= diff / 4.0
    
        diff = ymag - newYmag
        if abs(diff) > 0.01:
            ymag -= diff / 4.0
    
        rotateX(-ymag)
        rotateY(-xmag)
        scale(90)
    
        with beginShape(QUADS):
        
            fill(0, 1, 1)
            vertex(-1, 1, 1)
            fill(1, 1, 1)
            vertex(1, 1, 1)
            fill(1, 0, 1)
            vertex(1, -1, 1)
            fill(0, 0, 1)
            vertex(-1, -1, 1)
        
            fill(1, 1, 1)
            vertex(1, 1, 1)
            fill(1, 1, 0)
            vertex(1, 1, -1)
            fill(1, 0, 0)
            vertex(1, -1, -1)
            fill(1, 0, 1)
            vertex(1, -1, 1)
        
            fill(1, 1, 0)
            vertex(1, 1, -1)
            fill(0, 1, 0)
            vertex(-1, 1, -1)
            fill(0, 0, 0)
            vertex(-1, -1, -1)
            fill(1, 0, 0)
            vertex(1, -1, -1)
        
            fill(0, 1, 0)
            vertex(-1, 1, -1)
            fill(0, 1, 1)
            vertex(-1, 1, 1)
            fill(0, 0, 1)
            vertex(-1, -1, 1)
            fill(0, 0, 0)
            vertex(-1, -1, -1)
        
            fill(0, 1, 0)
            vertex(-1, 1, -1)
            fill(1, 1, 0)
            vertex(1, 1, -1)
            fill(1, 1, 1)
            vertex(1, 1, 1)
            fill(0, 1, 1)
            vertex(-1, 1, 1)
        
            fill(0, 0, 0)
            vertex(-1, -1, -1)
            fill(1, 0, 0)
            vertex(1, -1, -1)
            fill(1, 0, 1)
            vertex(1, -1, 1)
            fill(0, 0, 1)
            vertex(-1, -1, 1)
        
