"""
Performance demo with line rendering
"""

def setup():
    size(800, 600, P2D)  

    
def draw():    
    background(255)
    stroke(0, 10)
    for i in xrange(50000): 
        x0 = random(width)
        y0 = random(height)
        z0 = random(-100, 100)
        x1 = random(width)
        y1 = random(height)
        z1 = random(-100, 100)    
        
        # purely 2D lines will trigger the GLU 
        # tessellator to add accurate line caps,
        # but performance will be substantially
        # lower.
        line(x0, y0, z0, x1, y1, z1)
    
    if frameCount % 10 == 0:
        print frameRate