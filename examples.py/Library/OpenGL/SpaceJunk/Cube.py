class Cube:

    def __init__(self, w, h, d, shiftX, shiftY, shiftZ):
        self.w = w
        self.h = h
        self.d = d
        self.shiftX = shiftX
        self.shiftY = shiftY
        self.shiftZ = shiftZ

    # Main cube drawing method, which looks 
    # more confusing than it really is. It's 
    # just a bunch of rectangles drawn for 
    # each cube face
    def drawCube(self):
        (hx, hy, hz) = (self.w / 2 + self.shiftX,
                      self.h / 2 + self.shiftY,
                      self.d / 2 + self.shiftZ)
        (x, y, z) = (self.w + self.shiftX,
                      self.h + self.shiftY,
                      self.d + self.shiftZ)
        beginShape(QUADS)
        # Front face
        vertex(-hx, -hy, -hz) 
        vertex(x, -hy, -hz) 
        vertex(x, y, -hz) 
        vertex(-hx, y, -hz) 
        
        # Back face
        vertex(-hx, -hy, z) 
        vertex(x, -hy, z) 
        vertex(x, y, z) 
        vertex(-hx, y, z)
        
        # Left face
        vertex(-hx, -hy, -hz) 
        vertex(-hx, -hy, z) 
        vertex(-hx, y, z) 
        vertex(-hx, y, -hz) 
        
        # Right face
        vertex(x, -hy, -hz) 
        vertex(x, -hy, z) 
        vertex(x, y, z) 
        vertex(x, y, -hz) 
        
        # Top face
        vertex(-hx, -hy, -hz) 
        vertex(x, -hy, -hz) 
        vertex(x, -hy, z) 
        vertex(-hx, -hy, z) 
        
        # Bottom face
        vertex(-hx, y, -hz) 
        vertex(x, y, -hz) 
        vertex(x, y, z) 
        vertex(-hx, y, z) 
        
        endShape() 
        
        # Add some rotation to each box for pizazz.
        rotateY(radians(1))
        rotateX(radians(1))
        rotateZ(radians(1))
