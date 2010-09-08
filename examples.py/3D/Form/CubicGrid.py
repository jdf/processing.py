"""
    Cubic Grid 
    by Ira Greenberg. 

    3D translucent colored grid uses nested pushMatrix()
    and popMatrix() functions. 
"""
boxSize = 40
margin = boxSize*2
depth = 400

def setup():
    size(640, 360, P3D)
    noStroke()

def draw():
    background(255)
  
    # Center and spin grid
    translate(width/2, height/2, -depth)
    rotateY(frameCount * 0.01)
    rotateX(frameCount * 0.01)
    
    # Build grid using multiple translations
    i = -depth/2+margin
    while i <= depth/2-margin:
        pushMatrix()
        j = -height+margin
        while j <= height-margin:
            pushMatrix()
            k = -width + margin
            while k <= width-margin:
                # Base fill color on counter values, abs function 
                # ensures values stay within legal range
                boxFill = color(abs(i), abs(j), abs(k), 50)
                pushMatrix()
                translate(k, j, i)
                fill(boxFill)
                box(boxSize, boxSize, boxSize)
                popMatrix()
                k += boxSize
            popMatrix()
            j += boxSize
        popMatrix()
        i += boxSize    
