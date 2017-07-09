class Ball():

    def __init__(self, tempX, tempY, tempW):
        self.x = tempX
        self.y = tempY
        self.w = tempW
        self.speed = 0
        self.gravity = 0.1
        self.life = 255

    def move(self):
        # Add gravity to speed
        self.speed = self.speed + self.gravity
        # Add speed to y location
        self.y = self.y + self.speed
        # If it reaches the bottom, reverse speed
        if self.y > height:
            # Dampening
            self.speed = self.speed * -0.8
            self.y = height

    def finished(self):
        # Balls fade out
        self.life -= 1
        return self.life < 0

    def display(self):
        # Dispaly the circle
        fill(0, self.life)
        # stroke(0, self.life)
        ellipse(self.x, self.y, self.w, self.w)
