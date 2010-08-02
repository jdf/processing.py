class Cube:
    def __init__(self, w, h, d):
        self.w = w
        self.h = h
        self.d = d
        (w,h,d) = (w/2, h/2, d/2)
        self.vertices = [
            # Cube composed of 6 quads
            # Front
            (-w, -h, d), (w, -h, d), (w, h, d), (-w, h, d),
            # Left
            (-w, -h, d), (-w, -h, -d), (-w, h, -d), (-w, h, d),
            # Right
            (w, -h, d), (w, -h, -d), (w, h, -d), (w, h, d),
            # Back
            (-w, -h, -d), (w, -h, -d), (w, h, -d), (-w, h, -d),
            # Top
            (-w, -h, d), (-w, -h, -d), (w, -h, -d), (w, -h, d),
            # Bottom
            (-w, h, d), (-w, h, -d), (w, h, -d), (w, h, d)
        ]

    def create(self):
        for i in range(6):
            beginShape(QUADS)
            for v in [self.vertices[x+4*i] for x in range(4)]:
                vertex(v[0], v[1], v[2])
            endShape()
