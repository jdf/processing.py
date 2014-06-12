class MovingBall(object):

    # Constructor
    def __init__(self, xOffset, yOffset, x, y, speed, unit):
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.x = x
        self.y = y
        self.speed = speed
        self.unit = unit
        self.xDirection = 1
        self.yDirection = 1

    # Custom method for updating the variables
    def update(self):
        self.x += (self.speed * self.xDirection)
        if self.x >= self.unit or self.x <= 0:
            self.xDirection *= -1
            self.x += self.xDirection
            self.y += self.yDirection
        if self.y >= self.unit or self.y <= 0:
            self.yDirection *= -1
            self.y += self.yDirection

    # Custom method for drawing the object
    def draw(self):
        fill(255)
        ellipse(self.xOffset + self.x, self.yOffset + self.y, 6, 6)

