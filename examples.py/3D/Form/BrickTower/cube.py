class Cube:
    def __init__(self, w, h, d):
        self.w = w
        self.h = h
        self.d = d
        self.vertices = [
            # Cube composed of 6 quads
            # Front
            (-w/2, -h/2, d/2),
            (w/2, -h/2, d/2),
            (w/2, h/2, d/2),
            (-w/2, h/2, d/2),
        
            # Left
            (-w/2, -h/2, d/2),
            (-w/2, -h/2, -d/2),
            (-w/2, h/2, -d/2),
            (-w/2, h/2, d/2),
        
            # Right
            (w/2, -h/2, d/2),
            (w/2, -h/2, -d/2),
            (w/2, h/2, -d/2),
            (w/2, h/2, d/2),
        
            # Back
            (-w/2, -h/2, -d/2),  
            (w/2, -h/2, -d/2),
            (w/2, h/2, -d/2),
            (-w/2, h/2, -d/2),
        
            # Top
            (-w/2, -h/2, d/2),
            (-w/2, -h/2, -d/2),
            (w/2, -h/2, -d/2),
            (w/2, -h/2, d/2),
        
            # Bottom
            (-w/2, h/2, d/2),
            (-w/2, h/2, -d/2),
            (w/2, h/2, -d/2),
            (w/2, h/2, d/2)
        ]

    def create(self):
        for i in range(6):
            beginShape(QUADS);
            for j in range(4):
                vertex(vertices[j+4*i][0], vertices[j+4*i][1], vertices[j+4*i][2])
            endShape()
