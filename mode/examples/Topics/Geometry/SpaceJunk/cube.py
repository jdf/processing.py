class Cube(object):

    def __init__(self, w, h, d, shiftX, shiftY, shiftZ):
        self.w = w
        self.h = h
        self.d = d
        self.shiftX = shiftX
        self.shiftY = shiftY
        self.shiftZ = shiftZ
        self.minusWTwo = -self.w / 2
        self.minusHTwo = -self.h / 2
        self.minusDTwo = -self.d / 2

    # Main cube drawing method, which looks more confusing than it really is.
    # It's just a bunch of rectangles drawn for each cube face.
    def drawCube(self):
        with beginShape(QUADS):
            # Front face.
            vertex(self.minusWTwo + self.shiftX,
                   self.minusHTwo + self.shiftY,
                   self.minusDTwo + self.shiftZ)
            vertex(self.w + self.shiftX,
                   self.minusHTwo + self.shiftY,
                   self.minusDTwo + self.shiftZ)
            vertex(self.w + self.shiftX,
                   self.h + self.shiftY,
                   self.minusDTwo + self.shiftZ)
            vertex(self.minusWTwo + self.shiftX,
                   self.h + self.shiftY,
                   self.minusDTwo + self.shiftZ)
    
            # Back face.
            vertex(self.minusWTwo + self.shiftX,
                   self.minusHTwo + self.shiftY,
                   self.d + self.shiftZ)
            vertex(self.w + self.shiftX,
                   self.minusHTwo + self.shiftY,
                   self.d + self.shiftZ)
            vertex(self.w + self.shiftX,
                   self.h + self.shiftY,
                   self.d + self.shiftZ)
            vertex(self.minusWTwo + self.shiftX,
                   self.h + self.shiftY,
                   self.d + self.shiftZ)
    
            # Left face.
            vertex(self.minusWTwo + self.shiftX,
                   self.minusHTwo + self.shiftY,
                   self.minusDTwo + self.shiftZ)
            vertex(self.minusWTwo + self.shiftX,
                   self.minusHTwo + self.shiftY,
                   self.d + self.shiftZ)
            vertex(self.minusWTwo + self.shiftX,
                   self.h + self.shiftY,
                   self.d + self.shiftZ)
            vertex(self.minusWTwo + self.shiftX,
                   self.h + self.shiftY,
                   self.minusDTwo + self.shiftZ)
    
            # Right face.
            vertex(self.w + self.shiftX,
                   self.minusHTwo + self.shiftY,
                   self.minusDTwo + self.shiftZ)
            vertex(self.w + self.shiftX,
                   self.minusHTwo + self.shiftY,
                   self.d + self.shiftZ)
            vertex(self.w + self.shiftX,
                   self.h + self.shiftY,
                   self.d + self.shiftZ)
            vertex(self.w + self.shiftX,
                   self.h + self.shiftY,
                   self.minusDTwo + self.shiftZ)
    
            # Top face.
            vertex(self.minusWTwo + self.shiftX,
                   self.minusHTwo + self.shiftY,
                   self.minusDTwo + self.shiftZ)
            vertex(self.w + self.shiftX,
                   self.minusHTwo + self.shiftY,
                   self.minusDTwo + self.shiftZ)
            vertex(self.w + self.shiftX,
                   self.minusHTwo + self.shiftY,
                   self.d + self.shiftZ)
            vertex(self.minusWTwo + self.shiftX,
                   self.minusHTwo + self.shiftY,
                   self.d + self.shiftZ)
    
            # Bottom face.
            vertex(self.minusWTwo + self.shiftX,
                   self.h + self.shiftY,
                   self.minusDTwo + self.shiftZ)
            vertex(self.w + self.shiftX,
                   self.h + self.shiftY,
                   self.minusDTwo + self.shiftZ)
            vertex(self.w + self.shiftX,
                   self.h + self.shiftY,
                   self.d + self.shiftZ)
            vertex(self.minusWTwo + self.shiftX,
                   self.h + self.shiftY,
                   self.d + self.shiftZ)
    

        # Add some rotation to each box for pizazz.
        rotateY(radians(1))
        rotateX(radians(1))
        rotateZ(radians(1))
