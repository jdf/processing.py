class Eye:

    def __init__(self, tx, ty, ts):
        self.x = tx
        self.y = ty
        self.size = ts
        self.angle = 0.0

    def update(self, mx,  my):
        self.angle = atan2(my - self.y, mx - self.x)

    def display(self):
        with pushMatrix():
            translate(self.x, self.y)
            fill(255)
            ellipse(0, 0, self.size, self.size)
            rotate(self.angle)
            fill(153, 204, 0)
            ellipse(self.size / 4, 0, self.size / 2, self.size / 2)

